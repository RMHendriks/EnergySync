from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.cell import Cell

import pygame
from code.classes.battery import Battery
from code.classes.house import House

class Cable():
    def __init__(self, cell: Cell, battery: Battery, house: House) -> None:

        self.cell = cell

        self.battery: Battery = battery
        self.house: House = house

        self.sprite = self.load_sprite()

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the cable to the screen. """

        img_center = (self.cell.x + self.cell.size // 2,
                      self.cell.y + self.cell.size // 2)
        window.blit(self.sprite, img_center)

    def load_sprite(self) -> None:
        """ Load the Cable sprite. """

        sprite = pygame.image.load("sprites/grid_1_2_3_4.png")
        return pygame.transform.scale(sprite, (self.cell.size * 1,
                                               self.cell.size * 1))