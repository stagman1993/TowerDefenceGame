import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame as pg

    from enemy.enemy import Enemy


class Projectile(abc.ABC):
    def __init__(self, position: pg.Vector2, target: Enemy, projectiles: list[Projectile]) -> None:
        self.pos = position.copy()
        self.target = target
        self.speed = 5
        self.movement = self.target.pos - self.pos
        self.projectiles = projectiles

    @abc.abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def move(self) -> None:
        raise NotImplementedError


class BasicProjectile(Projectile):
    def __init__(self, position: pg.Vector2, target: Enemy, projectiles: list[Projectile]) -> None:
        super().__init__(position, target, projectiles)
        self.colour = "Yellow"
        self.pos = position.copy()
        self.target = target
        self.speed = 5
        self.movement = self.target.pos - self.pos
        self.damage = 1

    def update(self) -> None:
        self.move()

    def move(self) -> None:
        if self.target is None:
            if self in self.projectiles:
                self.projectiles.remove(self)
            return
        self.movement = self.target.pos - self.pos
        dist = self.movement.length()

        if dist <= self.speed:
            # Close enough: consider it a hit and despawn.
            self.pos = self.target.pos.copy()
            if self in self.projectiles:
                self.target.health -= self.damage
                self.projectiles.remove(self)
        self.pos += self.movement.normalize() * self.speed
