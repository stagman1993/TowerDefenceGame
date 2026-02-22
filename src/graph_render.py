import logging

import pygame as pg

from enemy.enemy import EnemyType
from map.graph import Graph, Waypoint

logger = logging.getLogger(__name__)


def get_colour(waypoint: Waypoint) -> str:
    match waypoint.index:
        case "spawn":
            colour = "red"
        case "river":
            colour = "blue"
        case "bridge":
            colour = "brown"
        case "base":
            colour = "green"
        case _:
            colour = "white"

    return colour


def main() -> None:
    pg.init()
    logger.info(pg.version.ver)
    clock = pg.time.Clock()

    res = (800, 800)
    factor = res[0] // 10
    window = pg.display.set_mode(res)
    pg.display.set_caption("Graph Render")

    graph = Graph()
    graph.add_waypoint("spawn", 0, 0)
    graph.add_waypoint("bridge", 1, 0)
    graph.add_waypoint("river", 1, 0)
    graph.add_waypoint("base", 2, 0)

    # Bridge: ground and flying only

    graph.add_edge("spawn", "river", traversable_by=EnemyType.AQUATIC)
    graph.add_edge("spawn", "bridge", traversable_by=EnemyType.GROUND | EnemyType.FLYING)
    graph.add_edge("spawn", "base", weight=0.5, traversable_by=EnemyType.FLYING)

    graph.add_edge("bridge", "base")
    graph.add_edge("river", "base")

    run = True
    while run:
        clock.tick(60)
        window.fill("black")

        for waypoint in graph:
            pg.draw.rect(
                window, get_colour(waypoint), pg.Rect(waypoint.x * factor, waypoint.y * factor, factor, factor)
            )

        for index in range(0, res[0], factor):
            pg.draw.line(window, "white", (0, index), (res[0], index))

        for index in range(0, res[1], factor):
            pg.draw.line(window, "white", (index, 0), (index, res[1]))

        pg.display.update()
        for event in pg.event.get():
            # quit program
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                logger.info(event.pos)


if __name__ == "__main__":
    main()
