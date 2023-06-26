import random
from copy import deepcopy
from typing import List, Dict
from copy import copy
from code.classes.grid import Grid
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable


class Evolution():
    """ Class that implements the Evolution algorithm
    for the smart grid problem. """

    def __init__(self, grid: Grid) -> None:
        
        self.grid: Grid = grid

        self.non_allocated_house_list: List[House] = copy(self.grid.house_list)
        self.allocated_house_list: List[House] = []
        
    def generate_solution(self) -> None:
        """ Method that generates a random valid solution to the grid. """

    def generate_population(self) -> None:
        """ Method that generates a random population of solutions. """

    def fitness(self) -> None:
        """ Method that takes a solution and calculates how well it performs. """
    
    def draw_path(self, battery: Battery, house: House) -> None:
        """ Method that draws a path between the house and battery. """

        if battery is None:
            Exception("House misses a battery connection.")

        house_index = house.cell.get_index()
        battery_index = battery.cell.get_index()

        delta = (battery_index[0] - house_index[0], battery_index[1] - house_index[1])
        incerement_x = 1 if delta[0] > 0 else -1
        incerement_y = 1 if delta[1] > 0 else -1

        for x in range(house_index[0], battery_index[0] + incerement_x, incerement_x):
            cell = self.grid.grid[x][house_index[1]]
            cable = Cable(cell, battery, house)
            cell.cable_list.append(cable)
            house.cable_list.append(cable)
            self.grid.cable_list.append(cable)

        for y in range(house_index[1] + incerement_y, battery_index[1] + incerement_y, incerement_y):
            cell = self.grid.grid[battery_index[0]][y]
            cable = Cable(cell, battery, house)
            cell.cable_list.append(cable)
            house.cable_list.append(cable)
            self.grid.cable_list.append(cable)

        if (battery_index[0] != house.cable_list[-1].cell.x_index or
            battery_index[1] != house.cable_list[-1].cell.y_index):
            Exception("Cables are not connected to the battery") 

    def calculate_distance(self, battery: Battery, house: House) -> int:
        """ Calculates the distance between a house and a battery. 
        Distance is in cells. """

        x_distance = abs(battery.cell.x_index - house.cell.x_index)
        y_distance = abs(battery.cell.y_index - house.cell.y_index)

        return x_distance + y_distance
    