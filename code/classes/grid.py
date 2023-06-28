from __future__ import annotations

from typing import List
from copy import deepcopy, copy
from code.classes.cell import Cell
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable


class Grid():
    """ Class that holds the logic for a grid. """

    def __init__(self, screen_width: int, screen_height: int, grid_size: int,
                 vertical_spacing: int, horizontal_spacing: int) -> None:
        """ Initializes a grid object.

        - screen_width as an int.
        - screen_height as an int.
        - grid size to decide the size of the grid as an int.
        - vertical_margin to set the vertical margin of the grid as an int in
        pixels.
        - horizontal_margin to set the horizontal margin of the grid as an int
        in pixels. """

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vertical_spacing = vertical_spacing // 2
        self.horizontal_spacing = horizontal_spacing // 2

        self.cell_size = int(screen_width // grid_size)
        self.grid_size = grid_size

        self.battery_list: List[Battery] = []
        self.house_list: List[House] = []
        self.cable_list: List[Cable] = []

        self.non_allocated_house_list: List[House] = []
        self.allocated_house_list: List[House] = []

        self.grid: List[List[Cell]] = self.make_grid()

    def make_grid(self):
        """ Builds the grid and fills it with Cell objects. """

        grid: List[List[Cell]] = []

        for x_index, x in enumerate(range(self.horizontal_spacing,
                                          self.screen_width + self.horizontal_spacing,
                                          self.cell_size)):
            cell_list: List[Cell] = []
            for y_index, y in enumerate(range(self.vertical_spacing + self.screen_height,
                                              self.vertical_spacing, -self.cell_size)):
                cell_list.append(Cell(self, x, y, self.cell_size, x_index, y_index))
            grid.append(cell_list)

        return grid

    def get_cell_by_index(self, x_index: int, y_index: int) -> Cell:
        """ Gets a cell object by its index.

        - x_index as an int.
        - y_index as an int.

        Returns: the Cell object at the x_index and y_index locations in the
        grid. """

        return self.grid[x_index][y_index]

    def get_cell_by_object(self, cell: Cell) -> Cell:
        """ Gets a cell object from a cell (Used for cells that are deepcopied).

        - cell as a Cell object

        Returns: the cell coronsponding with the same cell on this grid. """

        x_index = cell.x_index
        y_index = cell.y_index

        return self.grid[x_index][y_index]

    def get_battery_by_object(self, battery: Battery) -> Battery:
        """ Gets a battery object from a battery
        (Used for batteries that are deepcopied).

        - battery as a Battery object

        Returns: the battery coronsponding with the same battery on this
        grid. """

        x_index = battery.cell.x_index
        y_index = battery.cell.y_index

        return self.grid[x_index][y_index].battery

    def get_house_by_object(self, house: House) -> House:
        """ Gets a house object from a battery
        (Used for houses that are deepcopied).

        - house as a House object

        Returns: the house coronsponding with the same house on this
        grid. """

        x_index = house.cell.x_index
        y_index = house.cell.y_index

        return self.grid[x_index][y_index].house

    def clean_grid(self) -> None:
        """ Clean the grid from all house/battery assignments and cables for
        console mode. """

        self.cable_list = []
        self.non_allocated_house_list = copy(self.house_list)
        self.allocated_house_list = []

        for battery in self.battery_list:
            battery.house_list = []
            battery.cable_list = []
            battery.capacity = battery.max_capacity

        for house in self.house_list:
            house.battery = None
            house.cable_list = []

        for row in self.grid:
            for cell in row:
                cell.cable_list = []

    def clean_grid_visualisation(self) -> None:
        """ Clean the grid from all house/battery assignments and cables for
        visualisation mode. """

        self.cable_list = []
        self.non_allocated_house_list = copy(self.house_list)
        self.allocated_house_list = []

        for battery in self.battery_list:
            battery.house_list = []
            battery.cable_list = []
            battery.capacity = battery.max_capacity

        for house in self.house_list:
            house.battery = None
            house.cable_list = []
            house.sprite = house.load_sprite()

        for row in self.grid:
            for cell in row:
                cell.cable_list = []
                cell.connections.clear_connections()
                cell.load_sprite()

    def assign_connections(self) -> None:
        """ Fill in the connections between cells
        according to the positions of the cables. Used for the drawing of
        cables in visualisation mode"""

        for house in self.house_list:
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

    def __iter__(self) -> Grid:
        """ Sets up the iterator. """

        self.index_x = 0
        self.index_y = 0

        return self

    def __next__(self) -> Cell:
        """ Returns: the next cell in the grid. """

        if (self.index_y < len(self.grid)):

            cell = self.grid[self.index_x][self.index_y]
            self.index_x += 1

            if self.index_x >= len(self.grid[self.index_y]): 
                self.index_x = 0
                self.index_y += 1

            return cell

        else:
            raise StopIteration

    def __deepcopy__(self, memo={}):
        """ Makes a deepcopy of the grid object (trimmed the amount of
        deepcopies for efficiency). """

        # create new instances of the lists and objects
        battery_list = deepcopy(self.battery_list, memo)
        house_list = deepcopy(self.house_list, memo)
        cable_list = deepcopy(self.cable_list, memo)
        
        # create a new instance of the Grid class with the copied attributes
        copied_grid = Grid(self.screen_width, self.screen_height, self.grid_size,
                           self.vertical_spacing, self.horizontal_spacing)

        # copy the remaining attributes
        copied_grid.battery_list = battery_list
        copied_grid.house_list = house_list
        copied_grid.cable_list = cable_list
        copied_grid.non_allocated_house_list = deepcopy(self.non_allocated_house_list, memo)
        copied_grid.allocated_house_list = deepcopy(self.allocated_house_list, memo)
        copied_grid.grid = deepcopy(self.grid, memo)

        return copied_grid

    def __repr__(self) -> str:
        return f"Grid with {len(self.cable_list)} cable(s)"
