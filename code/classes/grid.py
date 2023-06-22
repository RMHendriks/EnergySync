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
        self.grid_size = grid_size

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

        grid: List[List[Cell]] = []

        for x_index, x in enumerate(range(self.spacing, self.screen_width + self.spacing, self.cell_size)):
            cell_list: List[Cell] = []
            for y_index, y in enumerate(range(self.spacing + self.screen_height, self.spacing, -self.cell_size)):
                cell_list.append(Cell(self, x, y, self.cell_size, x_index, y_index))
            grid.append(cell_list)

        return grid

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

    def assign_connections(self) -> None:
        """ Fill in the connections between cells
        according to the positions of the cables. """


        for house in self.house_list:
            print(house.cable_list)
            for index, cable in enumerate(house.cable_list):
                if index < len(house.cable_list) - 1:
                    cell_index = cable.cell.get_index()
                    next_cell_index = house.cable_list[index + 1].cell.get_index()

                    if next_cell_index[0] > cell_index[0]:
                        cable.cell.connections.right = True
                        house.cable_list[index + 1].cell.connections.left = True
                    elif next_cell_index[0] < cell_index[0]:
                        cable.cell.connections.left = True
                        house.cable_list[index + 1].cell.connections.right = True
                    elif next_cell_index[1] > cell_index[1]:
                        cable.cell.connections.top = True
                        house.cable_list[index + 1].cell.connections.bottom = True
                    elif next_cell_index[1] < cell_index[1]:
                        cable.cell.connections.bottom = True
                        house.cable_list[index + 1].cell.connections.top = True

                    print(cable.cell.connections)


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