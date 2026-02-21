from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame as pg

    from enemy.enemy import Enemy


# TODO: Refactor this into an abstract base class
class Projectile:
    def __init__(self, position: pg.Vector2, target: Enemy, projectiles: list[Projectile]) -> None:
        self.colour = "Yellow"
        self.pos = position.copy()
        self.target = target
        self.speed = 5
        self.movement = self.target.pos - self.pos
        self.projectiles = projectiles

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
                self.projectiles.remove(self)
        self.pos += self.movement.normalize() * self.speed
