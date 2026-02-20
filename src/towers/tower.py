import pygame as pg


def tower_slot_generator(tower_postions: list[tuple[int, int]]) -> list[TowerSlot]:
    return [TowerSlot(x, y) for x, y in tower_postions]


def tower_placement(tower_slots: list[TowerSlot]) -> None:
    mouse_pos = pg.mouse.get_pos()
    for tower_slot in tower_slots:
        if pg.Rect(mouse_pos[0], mouse_pos[1], 1, 1) in tower_slot.rect:
            tower_slot.colour = "red"
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    place_tower(tower_slot, BasicTower)
        else:
            tower_slot.colour = "green"


def place_tower(slot: TowerSlot, tower: type[Tower]) -> None:
    slot.tower = tower()


class TowerSlot:
    def __init__(self, x: int, y: int) -> None:
        self.size = 64
        self.rect = pg.Rect(x - self.size / 2, y - self.size / 2, self.size, self.size)
        self.tower = None
        self.pos = None
        self.width = 4
        self.colour = "green"


class Tower:
    def __init__(self) -> None:
        self.range = 10
        self.damage = 10
        self.speed = 10
        self.colour = None
        self.level = 1

    def shoot(self) -> None:
        pass

    def upgrade(self) -> None:
        pass

    def kill(self) -> None:
        pass


class BasicTower(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.colour = "Red"
