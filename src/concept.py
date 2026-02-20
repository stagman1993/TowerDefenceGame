import logging

import pygame as pg

from enemy.enemy import BlueEnemy

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

enemy1 = BlueEnemy(nodes)
run = True
while run:
    clock.tick(60)
    window.fill("black")

    pg.draw.lines(window, "grey", False, nodes, 10)
    pg.draw.circle(window, enemy1.colour, enemy1.pos, 10)
    pg.display.update()

    enemy1.update()
    for event in pg.event.get():
        # quit program
        if event.type == pg.QUIT:
            run = False

pg.quit()
