import logging

import pygame as pg

from enemy.enemy import BlueEnemy
from towers.tower import tower_placement, tower_slot_generator

logger = logging.Logger(__name__)

pg.init()
logger.info(pg.version.ver)
clock = pg.time.Clock()

window = pg.display.set_mode((800, 600))
pg.display.set_caption("Concept")

nodes = [
    (100, 0),
    (100, 125),
    (30, 125),
    (30, 231),
    (300, 231),
    (300, 421),
    (380, 421),
    (421, 421),
    (421, 330),
    (800, 300),
]
tower_postions = [(80, 179), (253, 280), (363, 374), (756, 361)]

tower_slots = tower_slot_generator(tower_postions)
enemy1 = BlueEnemy(nodes)

run = True
while run:
    clock.tick(60)
    window.fill("black")

    tower_placement(tower_slots)
    for tower_slot in tower_slots:
        pg.draw.rect(window, tower_slot.colour, tower_slot.rect, width=4)
        if tower_slot.tower is not None:
            pg.draw.circle(window, tower_slot.tower.colour, tower_slot.rect.center, 15)

    pg.draw.lines(window, "grey", False, nodes, 10)
    pg.draw.circle(window, enemy1.colour, enemy1.pos, 10)
    pg.display.update()

    enemy1.update()
    for event in pg.event.get():
        # quit program
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            logger.info(event.pos)

pg.quit()
