import abc
from enum import Flag, auto

import pygame as pg


class EnemyType(Flag):
    GROUND = auto()
    FLYING = auto()
    AQUATIC = auto()
    # Combinations come for free with Flag
    ALL = GROUND | FLYING | AQUATIC


class Enemy(abc.ABC):
    def __init__(self, waypoints: list, enemeies: list[Enemy]) -> None:
        self.waypoints = waypoints
        self.pos = pg.Vector2(waypoints[0])
        self.target_waypoint = 1
        self.health = 10
        self.enemies = enemeies
        self.speed = 5
        self.type = EnemyType.GROUND
        self.color = None
        self.target = None
        self.movement = None

    def update(self) -> None:
        self.move()
        self.kill()

    @abc.abstractmethod
    def kill(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def move(self) -> None:
        raise NotImplementedError


class BlueEnemy(Enemy):
    def __init__(self, waypoints: list, enemies: list[Enemy]) -> None:
        super().__init__(waypoints, enemies)
        self.colour = "Blue"

    def move(self) -> None:
        if self.target_waypoint < len(self.waypoints):
            self.target = pg.Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # enemy has reached the end of the path
            self.pos = pg.Vector2(self.waypoints[0])
            self.target_waypoint = 0
            return
        # calculate distance to target
        dist = self.movement.length()
        # check if remaining distance is greater than the enemy speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def kill(self) -> None:
        if self.health <= 0:
            self.enemies.remove(self)
