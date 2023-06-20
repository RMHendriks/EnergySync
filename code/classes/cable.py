from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.cell import Cell

import pygame
from code.classes.battery import Battery
from code.classes.house import House

class Cable():
    def __init__(self, cell: Cell, battery: Battery, house: House) -> None:

        self.cell = cell

        self.battery: Battery = battery
        self.house: House = house
