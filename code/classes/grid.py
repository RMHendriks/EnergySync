from __future__ import annotations

from typing import List
from code.classes.cell import Cell

class Grid():
    def __init__(self, screen_width: int, screen_height: int, grid_size: int, spacing: int) -> None:
        """ Initializes the grid. """

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spacing = spacing // 2

        self.cell_size = int(screen_width // grid_size)

        self.grid: List[List[Cell]] = self.make_grid()

    def make_grid(self):
        """
        Makes the grid 

        Precondition: 
        Postcondition:
        """

        return [[Cell(x, y, self.cell_size) for x in range(self.spacing, self.screen_width + self.spacing, self.cell_size)]
                for y in range(self.spacing, self.screen_height + self.spacing, self.cell_size)]

    def get_cell_by_index(self, x: int, y: int):
        """ Gets the index of a cell. """

        return self.grid[x][y]

    def __iter__(self) -> Grid:
        """ Sets up the iterator. """

        self.index_x = 0
        self.index_y = 0
        return self
    
    def __next__(self) -> Cell:
        """ Returns the next cell in the grid. """

        if (self.index_y < len(self.grid)):

            cell = self.grid[self.index_x][self.index_y]
            self.index_x += 1

            if self.index_x >= len(self.grid[self.index_y]): 
                self.index_x = 0
                self.index_y += 1

            return cell

        else:
            raise StopIteration