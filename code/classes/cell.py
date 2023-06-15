from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.battery import Battery
    from code.classes.house import House
    from code.classes.cable import Cable

import pygame
from typing import List, Optional, Tuple


class Cell():
    def __init__(self, x: int, y: int, size: int, x_index: int, y_index: int) -> None:

        self.x = x
        self.y = y
        self.size = size

        self.x_index = x_index
        self.y_index = y_index

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
    
    def get_index(self) -> Tuple[int, int]:
        """ Get the index of the cell. """

        return (self.x_index, self.y_index)

    def __str__(self) -> str:  
        """ Return the index of the cell. """

        return f"Cell X: {self.x_index}, Y: {self.y_index}"
