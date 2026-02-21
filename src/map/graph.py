from dataclasses import dataclass, field

from enemy.enemy import EnemyType


@dataclass
class Edge:
    target_id: str
    weight: float = 1.0
    traversable_by: EnemyType = EnemyType.ALL  # default: anyone can use it


@dataclass
class Waypoint:
    index: str
    x: float
    y: float
    edges: list[Edge] = field(default_factory=list)


class Graph:
    def __init__(self) -> None:
        self.waypoints: dict[str, Waypoint] = {}

    def add_waypoint(self, index: str, x: float, y: float) -> Waypoint:
        wp = Waypoint(index=index, x=x, y=y)
        self.waypoints[index] = wp
        return wp

    def add_edge(
        self, from_id: str, to_id: str, weight: float = 1.0, traversable_by: EnemyType = EnemyType.ALL
    ) -> None:
        edge = Edge(target_id=to_id, weight=weight, traversable_by=traversable_by)
        self.waypoints[from_id].edges.append(edge)

    def get_neighbours(self, index: str, enemy_type: EnemyType) -> list[tuple[Waypoint, float]]:
        wp = self.waypoints[index]
        return [
            (self.waypoints[e.target_id], e.weight)
            for e in wp.edges
            if enemy_type in e.traversable_by  # Flag membership check
        ]
