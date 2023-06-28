from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.grid import Grid
    from code.classes.battery import Battery
    from code.classes.house import House
    from code.classes.cable import Cable

import pygame
from typing import List, Optional, Tuple, Dict
from copy import copy, deepcopy
from code.classes.connection import Connection


class Cell():
    """ Class that holds all the information of a grid cell.
    This includes cables, houses, batteries. """

    def __init__(self, grid: Grid, x: int, y: int, size: int, x_index: int,
                 y_index: int) -> None:
        """ Initializes a grid cell object.

        - grid as a Grid object.
        - x as an int for the pixel position on the screen (Used for pygame).
        - y as an int for the pixel position on the screen (Used for pygame).
        - size as an int for the size of the cell.
        - x_index as an int for the index in the grid.
        - y_index as an int for the index in the grid. """

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

        self.sprite: Optional[pygame.surface.Surface] = None

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw cell to the screen.

        - Needs a window as pygame.surface.Surface object. """

        if self.sprite is not None:
            window.blit(self.sprite, [self.x, self.y])

    def load_sprite(self, highlight_sprite=False) -> None:
        """ Draw cell to the screen. """

        if highlight_sprite:
            sprite = pygame.image.load(self.connections.load_sprite(highlight_sprite=True))
        else:
            sprite = pygame.image.load(self.connections.load_sprite())

        self.sprite = pygame.transform.scale(sprite, (self.size, self.size))

    def get_index(self) -> Tuple[int, int]:
        """ Get the index of the cell.

        Returns: tuple[self.x_index, self.y_index]"""

        return (self.x_index, self.y_index)

    def assign_connection(self, next_cable: Cable) -> None:
        """ Assigns the connections the cell has for the visualisation mode.
        
        - next_cable as a Cable object. """

        cell_index = self.get_index()
        next_cell_index = next_cable.cell.get_index()

        if next_cell_index[0] > cell_index[0]:
            self.connections.right = True
            next_cable.cell.connections.left = True
        elif next_cell_index[0] < cell_index[0]:
            self.connections.left = True
            next_cable.cell.connections.right = True
        elif next_cell_index[1] > cell_index[1]:
            self.connections.top = True
            next_cable.cell.connections.bottom = True
        elif next_cell_index[1] < cell_index[1]:
            self.connections.bottom = True
            next_cable.cell.connections.top = True

    def __deepcopy__(self, memo: Dict) -> Cell:
        """ Makes a deepcopy of the cell object (trimmed the amount of
        deepcopies for efficiency). """

        new_cell = Cell(self.grid, self.x, self.y, self.size, self.x_index,
                        self.y_index)
        new_cell.cable_list = copy(self.cable_list)
        new_cell.house = copy(self.house)
        new_cell.battery = deepcopy(self.battery)

        return new_cell

    def __repr__(self) -> str:  
        return f"Cell X: {self.x_index}, Y: {self.y_index}"
