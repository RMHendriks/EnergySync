from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.cell import Cell

import pygame

class Cable():
    def __init__(self, cell: Cell) -> None:

        self.cell = cell

        self.sprite = self.load_sprite()

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the cable to the screen. """

        img_center = (self.cell.x + self.cell.size // 2,
                      self.cell.y + self.cell.size // 2)
        window.blit(self.sprite, img_center)

    def load_sprite(self) -> None:
        """ Load the Cable sprite. """

        sprite = pygame.image.load("sprites/cable.png")
        return pygame.transform.scale(sprite, (self.cell.size * 1,
                                               self.cell.size * 1))