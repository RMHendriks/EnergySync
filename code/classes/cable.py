from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.cell import Cell
    from code.classes.battery import Battery

from code.classes.house import House


class Cable():
    """ Class that holds the logic for the cables on the grid. """

    def __init__(self, cell: Cell, battery: Battery, house: House) -> None:
        """ Initializes a cable object.

        - Needs a grid cell to locate the cable on the grid. 
        - Needs a battery to trace its origin.
        - Needs a house to trace its destination. """

        self.cell = cell

        self.battery: Battery = battery
        self.house: House = house

    def __repr__(self) -> str:
        return f"Cable: {self.cell.x_index}, {self.cell.y_index}"
