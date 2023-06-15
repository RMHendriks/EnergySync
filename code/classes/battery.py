from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.cell import Cell

import pygame
from typing import List
from code.classes.house import House

class Battery():
    def __init__(self, cell: Cell, capacity: float) -> None:

        self.cell = cell
        self.max_capacity = capacity
        self.capacity = capacity

        self.house_list: List[House] = []

        self.sprite = self.load_sprite()

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the battery to the screen. """

        x = self.cell.x
        y = self.cell.y
        window.blit(self.sprite, (x, y))

    def load_sprite(self) -> None:
        """ Load the Battery sprite. """

        sprite = pygame.image.load("sprites/battery.png")
        return pygame.transform.scale(sprite, (self.cell.size * 1,
                                               self.cell.size * 1))

    def __repr__(self) -> str:
            return f"{self.cell.x_index}, {self.cell.y_index}"