from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.grid import Grid
    from code.classes.battery import Battery
    from code.classes.house import House
    from code.classes.cable import Cable

import pygame
from typing import List, Optional, Tuple
from code.classes.connection import Connection


class Cell():
    """ Class that holds all the information of a grid cell.
    This includes cables, houses, batteries. """

    def __init__(self, grid: Grid, x: int, y: int, size: int, x_index: int, y_index: int) -> None:

        self.grid = grid
        self.connections = Connection()

        self.x = x
        self.y = y
        self.size = size

        self.x_index = x_index
        self.y_index = y_index

        self.battery: Optional[Battery] = None
        self.house: Optional[House] = None
        self.cable_list: List[Cable] = []

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw cell to the screen. """

        window.blit(self.sprite, [self.x, self.y])

    def load_sprite(self) -> None:
        """ Draw cell to the screen. """

        sprite = pygame.image.load(self.connections.load_sprite())

        self.sprite = pygame.transform.scale(sprite, (self.size, self.size))

    def get_index(self) -> Tuple[int, int]:
        """ Get the index of the cell. """

        return (self.x_index, self.y_index)

    def __str__(self) -> str:  
        """ Return the index of the cell. """

        return f"Cell X: {self.x_index}, Y: {self.y_index}"
