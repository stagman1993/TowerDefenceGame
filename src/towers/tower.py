import abc
from typing import TYPE_CHECKING

import pygame as pg
from pydantic import BaseModel, ConfigDict

from projectiles.projectile import Projectile

if TYPE_CHECKING:
    from enemy.enemy import Enemy


def tower_slot_generator(tower_postions: list[tuple[int, int]]) -> list[TowerSlot]:
    return [TowerSlot(x=x, y=y) for x, y in tower_postions]


def tower_placement(tower_slots: list[TowerSlot], position: tuple[int, int], projectiles: list[Projectile]) -> None:
    for tower_slot in tower_slots:
        if pg.Rect(position[0], position[1], 1, 1) in tower_slot.rect:
            tower_slot.colour = "red"
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    place_tower(tower_slot, BasicTower, projectiles)
        else:
            tower_slot.colour = "green"


def place_tower(slot: TowerSlot, tower: type[Tower], projectiles: list[Projectile]) -> None:
    slot.tower = tower(pg.Vector2(slot.x, slot.y), projectiles)


class TowerSlot(BaseModel):
    x: int
    y: int
    size: int = 64
    rect: pg.Rect = None  # ty:ignore[invalid-assignment]
    tower: Tower = None  # ty:ignore[invalid-assignment]
    pos: tuple[int, int] | None = None
    width: int = 4
    colour: str = "green"
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def model_post_init(self, _: None) -> None:
        self.rect = pg.Rect(self.x - self.size / 2, self.y - self.size / 2, self.size, self.size)


class Tower(abc.ABC):
    def __init__(self, position: pg.Vector2, projectiles: list[Projectile]) -> None:
        self.range = 10
        self.damage = 10
        self.speed = 10
        self.counter = 0
        self.colour = "red"
        self.level = 1
        self.position = position
        self.projectiles = projectiles

    def update(self, enemies: list[Enemy]) -> None:
        self.find_valid_targets(enemies)
        self.shoot()

    @abc.abstractmethod
    def find_valid_targets(self, enemies: list[Enemy]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def shoot(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def upgrade(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def kill(self) -> None:
        raise NotImplementedError


class BasicTower(Tower):
    def __init__(self, position: pg.Vector2, projectiles: list[Projectile]) -> None:
        super().__init__(position, projectiles)
        self.colour = "Orange"
        self.range = 100

    def find_valid_targets(self, enemies: list[Enemy]) -> None:
        self.targets = [enemy for enemy in enemies if self.position.distance_to(enemy.pos) <= self.range]
        if not self.targets:
            self.colour = "Orange"
        else:
            self.colour = "red"

    def shoot(self) -> None:
        self.targets.sort(key=self._sort_distance_to)
        if len(self.targets) > 0:
            if self.counter == self.speed:
                self.counter = 0
                self.projectiles.append(Projectile(self.position, self.targets[0], self.projectiles))
            else:
                self.counter += 1
                self.colour = "Orange"

    def upgrade(self) -> None:
        pass

    def kill(self) -> None:
        pass

    def _sort_distance_to(self, _) -> float:  # noqa: ANN001
        return self.position.distance_to(_.pos)
