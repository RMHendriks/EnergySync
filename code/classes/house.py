from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.cell import Cell

import pygame

class House():
    def __init__(self, cell: Cell ,output: float) -> None:

        self.cell = cell
        self.max_output = output

        self.sprite = self.load_sprite()

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw cell to the screen. """

        window.blit(self.sprite, [self.cell.x, self.cell.y])

    def load_sprite(self) -> None:
        """ Draw cell to the screen. """

        sprite = pygame.image.load("sprites/house.png")
        return pygame.transform.scale(sprite, (self.cell.size * 2,
                                               self.cell.size * 2))
