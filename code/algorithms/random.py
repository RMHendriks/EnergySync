import random
from typing import List
from copy import copy
from code.algorithms.algorithm import Algoritm
from code.classes.grid import Grid
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable

class Random(Algoritm):
    """ class that generates a random solution
    for the smart grid problem. """

    def __init__(self, grid: Grid) -> None:
        
        self.grid: Grid = grid

        self.non_allocated_house_list: List[House] = copy(self.grid.house_list)
        self.allocated_house_list: List[House] = []

    def calculate_solution(self) -> None:
        """ Method that calculates the results of the function. """

        cycle_counter = 1

        while(len(self.non_allocated_house_list) != len(self.allocated_house_list)):

            random.shuffle(self.non_allocated_house_list)

            for house in self.non_allocated_house_list:
                
                tmp_battery_list: List[Battery] = copy(self.grid.battery_list)

                while len(tmp_battery_list) > 0:
                    random.shuffle(tmp_battery_list)
                    battery = tmp_battery_list.pop()

                    if battery.capacity >= house.max_output:
                        battery.capacity -= house.max_output
                        battery.house_list.append(house)
                        house.battery = battery
                        self.allocated_house_list.append(house)
                        break

                if len(tmp_battery_list) == 0 and house.battery is None:
                    cycle_counter += 1
                    self.grid.clean_grid()
                    self.allocated_house_list = []
                    break

        for house in self.allocated_house_list:
            self.draw_path(house.battery, house)

        print(f"Solution found in {cycle_counter} cycle(s).")

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
