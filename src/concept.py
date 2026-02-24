import logging
import random

import pygame as pg

from enemy.enemy import BlueEnemy
from towers.tower import tower_placement, tower_slot_generator

"""
Initialize Pygame
"""
pg.init()
clock = pg.time.Clock()
window = pg.display.set_mode((800, 600))
pg.display.set_caption("Concept")
logger = logging.Logger(__name__)
logger.info(pg.version.ver)
logger.info("Initialization Complete")


"""
Debug to Generate Nodes
"""
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
"""
Debug to Generate Tower Slots
"""
tower_postions = [(80, 179), (253, 280), (363, 374), (756, 361)]
tower_slots = tower_slot_generator(tower_postions)

"""
Debug to spawn Enemies
"""
enemies = []
for _i in range(10):
    enemy = BlueEnemy(nodes, enemies)
    enemy.speed = random.randint(1, 8)  # noqa: S311
    enemies.append(enemy)

"""
Global Vars
"""
projectiles = []
run = True

"""
Game Loop
"""
while run:
    clock.tick(60)
    window.fill("black")

    tower_placement(tower_slots, pg.mouse.get_pos(), projectiles)

    pg.draw.lines(window, "grey", False, nodes, 10)
    for tower_slot in tower_slots:
        pg.draw.rect(window, tower_slot.colour, tower_slot.rect, width=tower_slot.width)
        if tower_slot.tower is not None:
            pg.draw.circle(window, tower_slot.tower.colour, tower_slot.rect.center, 15)
            pg.draw.circle(window, "pink", tower_slot.rect.center, tower_slot.tower.range, width=2)
            tower_slot.tower.update(enemies)

    for enemy in enemies:
        pg.draw.circle(window, enemy.colour, enemy.pos, 10)
        enemy.update()

    for projectile in projectiles:
        pg.draw.circle(window, projectile.colour, projectile.pos, 4)
        projectile.update()
    pg.display.update()

    for event in pg.event.get():
        # quit program
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            logger.info(event.pos)

pg.quit()
