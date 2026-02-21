import abc

import pygame as pg
from pydantic import BaseModel, ConfigDict


def tower_slot_generator(tower_postions: list[tuple[int, int]]) -> list[TowerSlot]:
    return [TowerSlot(x=x, y=y) for x, y in tower_postions]


def tower_placement(tower_slots: list[TowerSlot], position: tuple[int, int]) -> None:
    for tower_slot in tower_slots:
        if pg.Rect(position[0], position[1], 1, 1) in tower_slot.rect:
            tower_slot.colour = "red"
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    place_tower(tower_slot, BasicTower)
        else:
            tower_slot.colour = "green"


def place_tower(slot: TowerSlot, tower: type[Tower]) -> None:
    slot.tower = tower()


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
    def __init__(self) -> None:
        self.range = 10
        self.damage = 10
        self.speed = 10
        self.colour = "red"
        self.level = 1

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
    def __init__(self) -> None:
        super().__init__()
        self.colour = "Red"

    def shoot(self) -> None:
        pass

    def upgrade(self) -> None:
        pass

    def kill(self) -> None:
        pass
