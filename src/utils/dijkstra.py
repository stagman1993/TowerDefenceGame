import heapq
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enemy.enemy import EnemyType
    from map.graph import Graph


def dijkstra(graph: Graph, start_id: str, end_id: str, enemy_type: EnemyType) -> list[str]:
    dist = {start_id: 0.0}
    prev = {}
    pq = [(0.0, start_id)]

    while pq:
        cost, current = heapq.heappop(pq)
        if current == end_id:
            break
        for neighbour, weight in graph.get_neighbours(current, enemy_type):
            new_cost = cost + weight
            if new_cost < dist.get(neighbour.index, float("inf")):
                dist[neighbour.index] = new_cost
                prev[neighbour.index] = current
                heapq.heappush(pq, (new_cost, neighbour.index))

    # Reconstruct path
    path, node = [], end_id
    while node in prev:
        path.append(node)
        node = prev[node]
    path.append(start_id)
    return list(reversed(path))
