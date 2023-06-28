from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.cell import Cell
    from code.classes.battery import Battery
    from code.classes.cable import Cable

import pygame
from typing import List, Optional, Dict
from copy import copy, deepcopy


class House():
    """ Class that holds the logic for the houses on the grid. """

    def __init__(self, cell: Cell, output: float) -> None:
        """ Initializes a house object. 

        - Needs a cell as a Cell object
        - Needs an output as a float. """

        self.cell = cell
        self.max_output = output

        self.battery: Optional[Battery] = None
        self.cable_list: List[Cable] = []
        self.shared_cable_list: List[Cable] = []

        self.sprite = None

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the house to the screen. 

        - Needs a window as pygame.surface.Surface object. """

        x = self.cell.x
        y = self.cell.y
        window.blit(self.sprite, (x, y))

    def load_sprite(self) -> None:
        """ Loads the house sprite. """

        sprite = pygame.image.load("sprites/house_2_black.png")
        self.sprite = pygame.transform.scale(sprite, (self.cell.size * 1,
                                             self.cell.size * 1))

    def load_sprite_connected(self) -> None:
        """ Loads the sprite when that shows that the house is connected in the
        visualisation. """

        sprite = pygame.image.load("sprites/house_2.png")
        self.sprite = pygame.transform.scale(sprite, (self.cell.size * 1,
                                             self.cell.size * 1))

    def __deepcopy__(self, memo: Dict) -> House:
        """ Makes a deepcopy of the house object (trimmed the amount of
        deepcopies for efficiency). """

        new_house = House(copy(self.cell), self.max_output)
        new_house.battery = deepcopy(self.battery)
        new_house.cable_list = copy(self.cable_list)
        self.sprite = None
        return new_house

    def __repr__(self) -> str:
        return f"House: {self.cell.x}, {self.cell.y}"
