from __future__ import annotations

from typing import List
from code.classes.cell import Cell
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable

class Grid():
    def __init__(self, screen_width: int, screen_height: int, grid_size: int,
                 spacing: int, battery_list: List[Battery], house_list: List[House],
                 cable_list: List[Cable]) -> None:
        """ Initializes the grid. """

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spacing = spacing // 2

        self.cell_size = int(screen_width // grid_size)

        self.battery_list: List[Battery] = battery_list
        self.house_list: List[House] = house_list
        self.cable_list: List[Cable] = cable_list

        self.grid: List[List[Cell]] = self.make_grid()

    def make_grid(self):
        """
        Makes the grid 

        Precondition: 
        Postcondition:
        """

        return [[Cell(x, y, self.cell_size, x_index, y_index) for x_index, x in enumerate(range(self.spacing, self.screen_width + self.spacing, self.cell_size))]
                for y_index, y in enumerate(range(self.spacing, self.screen_height + self.spacing, self.cell_size))]

    def get_cell_by_index(self, x: int, y: int):
        """ Gets the index of a cell. """

        return self.grid[x][y]
    
    def clean_grid(self):
        """ Clean the grid from all house/battery assignments and cables. """

        self.cable_list = []

        for battery in self.battery_list:
            battery.house_list = []
            battery.capacity = battery.max_capacity

        for house in self.house_list:
            house.battery = None
            house.cable_list = []

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