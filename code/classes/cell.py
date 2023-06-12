from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.battery import Battery
    from code.classes.house import House
    from code.classes.cable import Cable

import pygame
from typing import List, Optional


class Cell():
    def __init__(self, x: int, y: int, size: int) -> None:
        self.x = x
        self.y = y
        self.size = size

        self.battery: Optional[Battery] = None
        self.house: Optional[House] = None
        self.cable_list: List[Cable] = []

        self.sprite = self.load_sprite()

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw cell to the screen. """

        window.blit(self.sprite, [self.x, self.y])

    def load_sprite(self) -> None:
        """ Draw cell to the screen. """

        sprite = pygame.image.load("sprites/grid.png")
        return pygame.transform.scale(sprite, (self.size, self.size))

    def __str__(self) -> str:  
        """ Return the index of the cell. """

        return f"Cell X: {self.x // self.size}, Y: {self.y // self.size}"
