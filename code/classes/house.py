from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.cell import Cell
    from code.classes.battery import Battery
    from code.classes.cable import Cable

import pygame
from typing import List, Optional


class House():
    def __init__(self, cell: Cell, output: float) -> None:

        self.cell = cell
        self.max_output = output
        
        self.battery: Optional[Battery] = None
        self.cable_list: List[Cable] = []

        self.sprite = self.load_sprite()

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the house to the screen. """

        x = self.cell.x
        y = self.cell.y
        window.blit(self.sprite, (x, y))

    def load_sprite(self) -> pygame.surface.Surface:
        """ Load the House sprite. """

        sprite = pygame.image.load("sprites/house_2_black.png")
        return pygame.transform.scale(sprite, (self.cell.size * 1,
                                               self.cell.size * 1))
    
    def load_sprite_connected(self) -> None:
        """ Loads the sprite when the house is connected in the visualisation. """

        sprite = pygame.image.load("sprites/house_2.png")
        self.sprite = pygame.transform.scale(sprite, (self.cell.size * 1,
                                             self.cell.size * 1))

    def __repr__(self) -> str:
        return f"{self.cell.x}, {self.cell.y}"