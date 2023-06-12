from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.cell import Cell

import pygame

class House():
    def __init__(self, cell: Cell, output: float) -> None:

        self.cell = cell
        self.max_output = output

        self.sprite = self.load_sprite()

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the house to the screen. """

        x = self.cell.x
        y = self.cell.y
        window.blit(self.sprite, (x, y))

    def load_sprite(self) -> None:
        """ Load the House sprite. """

        sprite = pygame.image.load("sprites/house.png")
        return pygame.transform.scale(sprite, (self.cell.size * 1,
                                               self.cell.size * 1))
