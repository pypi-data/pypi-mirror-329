from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Type

from pydantic import BaseModel, Field, field_validator, model_validator

from trano import elements
from trano.elements.types import ConnectionView, Flow, PartialConnection
from trano.exceptions import IncompatiblePortsError

if TYPE_CHECKING:
    from trano.elements import BaseElement

INCOMPATIBLE_PORTS = [sorted(["dataBus", "y"])]


class Connection(BaseModel):
    right: PartialConnection
    left: PartialConnection
    connection_view: ConnectionView = Field(default=ConnectionView())

    @model_validator(mode="after")
    def _connection_validator(self) -> "Connection":
        if (
            sorted(
                [
                    part.split(".")[-1]
                    for part in [self.right.equation, self.left.equation]
                ]
            )
            in INCOMPATIBLE_PORTS
        ):
            raise IncompatiblePortsError(
                f"Incompatible ports {self.right.equation} and {self.left.equation}."
            )
        return self

    @property
    def path(self) -> List[List[float] | Tuple[float, float]]:
        if self.left.position[0] < self.right.position[0]:
            mid_path = (self.right.position[0] - self.left.position[0]) / 2
            return [
                self.left.position,
                (self.left.position[0] + mid_path, self.left.position[1]),
                (self.right.position[0] - mid_path, self.right.position[1]),
                self.right.position,
            ]

        else:
            mid_path = (self.left.position[0] - self.right.position[0]) / 2
            return [
                self.left.position,
                (self.left.position[0] - mid_path, self.left.position[1]),
                (self.right.position[0] + mid_path, self.right.position[1]),
                self.right.position,
            ]


class Port(BaseModel):
    names: list[str]
    targets: Optional[List[Any]] = None
    available: bool = True
    flow: Flow = Field(default=Flow.undirected)
    multi_connection: bool = False
    multi_object: bool = False
    bus_connection: bool = False
    use_counter: bool = True
    counter: int = Field(default=1)

    @field_validator("targets")
    @classmethod
    def validate_targets(cls, values: List[str]) -> List[Type["BaseElement"]]:
        from trano.elements import BaseElement

        targets: List[Type[BaseElement]] = []
        for value in values:
            if isinstance(value, str):
                if hasattr(elements, value):
                    targets.append(getattr(elements, value))
                else:
                    raise ValueError(f"Target {value} not found")
            else:
                targets.append(value)
        return targets

    def is_available(self) -> bool:
        return self.multi_connection or self.available

    def is_controllable(self) -> bool:
        from trano.elements.base import Control

        return self.targets is not None and any(
            target == Control for target in self.targets
        )

    def link(
        self, node: "BaseElement", connected_node: "BaseElement"
    ) -> list[PartialConnection]:

        from trano.elements.envelope import MergedBaseWall

        self.available = False
        partial_connections = []
        merged_number = 1
        if isinstance(node, MergedBaseWall):
            merged_number = len(node.surfaces)

        if isinstance(connected_node, MergedBaseWall):
            merged_number = len(connected_node.surfaces)
        for name in self.names:
            if self.multi_connection and self.bus_connection:
                first_counter = self.counter
                last_counter = self.counter + merged_number - 1
                counter = (
                    f"{first_counter}"
                    if first_counter == last_counter
                    else f"{first_counter}:{last_counter}"
                )
                equation = (
                    f"{node.name}[{counter}].{name}"
                    if self.multi_object
                    else f"{node.name}.{name}[{counter}]"
                )
                self.counter = last_counter + 1
            elif self.multi_connection and self.use_counter:
                equation = f"{node.name}.{name}[{self.counter}]"
                self.counter += 1
            else:
                equation = f"{node.name}.{name}"

            partial_connections.append(
                PartialConnection(equation=equation, position=node.position)
            )

        return partial_connections


def connection_color(edge: Tuple["BaseElement", "BaseElement"]) -> ConnectionView:
    from trano.elements.bus import DataBus
    from trano.elements.envelope import BaseSimpleWall
    from trano.elements.system import Weather

    if any(isinstance(e, BaseSimpleWall) for e in edge):
        return ConnectionView(color="{191,0,0}", thickness=0.1)
    if any(isinstance(e, DataBus) for e in edge):
        return ConnectionView(color=None, thickness=0.05)
    if any(isinstance(e, Weather) for e in edge):
        return ConnectionView(color=None, thickness=0.05)
    return ConnectionView()


def connect(edge: Tuple["BaseElement", "BaseElement"]) -> list[Connection]:
    connections = []
    edge_first = edge[0]
    edge_second = edge[1]
    edge_first_ports_to_skip: List[Port] = []
    edge_second_ports_to_skip: List[Port] = []
    while True:
        current_port = edge_first._get_target_compatible_port(
            edge_second, Flow.outlet, ports_to_skip=edge_first_ports_to_skip
        )
        other_port = edge_second._get_target_compatible_port(
            edge_first, Flow.inlet, ports_to_skip=edge_second_ports_to_skip
        )
        if any(port is None for port in [current_port, other_port]):
            break
        for left, right in zip(
            current_port.link(edge_first, edge_second),  # type: ignore
            other_port.link(edge_second, edge_first),  # type: ignore
        ):
            connections.append(
                Connection(
                    left=left, right=right, connection_view=connection_color(edge)
                )
            )
        edge_first_ports_to_skip.append(current_port)  # type: ignore
        edge_second_ports_to_skip.append(other_port)  # type: ignore
    return connections


def _has_inlet_or_outlet(target: "BaseElement") -> bool:
    return bool([port for port in target.ports if port.flow == Flow.inlet_or_outlet])


def _is_inlet_or_outlet(target: "BaseElement") -> bool:
    return bool(
        [port for port in target.ports if port.flow in [Flow.inlet, Flow.outlet]]
    )
