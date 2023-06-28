from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.cell import Cell

import pygame
from typing import List, Dict
from copy import copy
from code.classes.house import House
from code.classes.cable import Cable


class Battery():
    """ Class that holds the logic for the batteries on the grid. """


    def __init__(self, cell: Cell, capacity: float) -> None:
        """ Initializes a battery object. 
        
        - Needs a cell as a Cell object
        - Needs a capacity as a float. """

        self.cell = cell
        self.max_capacity = capacity
        self.capacity = capacity

        self.house_list: List[House] = []
        self.cable_list: List[Cable] = []

        self.sprite = None

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draws the battery to the screen.

        - Needs a window as pygame.surface.Surface object. """

        x = self.cell.x
        y = self.cell.y
        window.blit(self.sprite, (x, y))

    def load_sprite(self) -> None:
        """ Loads the Battery sprite. """

        sprite = pygame.image.load("sprites/battery_2.png")
        self.sprite = pygame.transform.scale(sprite, (self.cell.size * 1,
                                             self.cell.size * 1))
    
    def __deepcopy__(self, memo: Dict) -> Battery:
        """ Makes a deepcopy of the battery object (trimmed the amount of
        deepcopies for efficiency). """

        new_cell = copy(self.cell)
        new_battery = Battery(new_cell, self.max_capacity)
        new_battery.capacity = self.capacity
        new_battery.house_list = copy(self.house_list)
        new_battery.cable_list = copy(self.cable_list)
        return new_battery

    def __repr__(self) -> str:
            return f"Battery: [{self.cell.x_index}, {self.cell.y_index}]"