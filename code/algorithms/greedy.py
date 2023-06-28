import random
from typing import Dict
from code.algorithms.algorithm import Algorithm
from code.classes.grid import Grid
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable


class Greedy(Algorithm):
    """ Class that implements the greedy algorithm
    for the smart grid problem. """

    def __init__(self, grid: Grid) -> None:
        """ Initializes the greedy algorithm.
        
        - grid as Grid object. """

        self.grid: Grid = grid

    def calculate_solution(self) -> None:
        """ Executes the random algorithm to create a grid with valid
        battery and house connections by connecting houses to the closest
        available batteries. All paths are directly connected to the
        battery. """

        cycle_counter = 1

        while(len(self.grid.non_allocated_house_list) != len(self.grid.allocated_house_list)):

            random.shuffle(self.grid.non_allocated_house_list)

            for house in self.grid.non_allocated_house_list:
                
                battery_dict: Dict[Battery, int] = {}

                for battery in self.grid.battery_list:
                    if battery.capacity >= house.max_output:
                        distance = self.calculate_distance(battery, house)

                        battery_dict[battery] = distance

                if len(battery_dict) > 0:
                    battery: Battery = min(battery_dict, key=battery_dict.get)
                    battery.capacity -= house.max_output
                    battery.house_list.append(house)
                    house.battery = battery
                    self.grid.allocated_house_list.append(house)
                else:
                    cycle_counter += 1
                    self.grid.clean_grid()
                    self.grid.allocated_house_list = []
                    break

        for house in self.grid.allocated_house_list:
            self.draw_path(house.battery, house)

        print(f"Solution found in {cycle_counter} cycle(s).")

    def draw_path(self, battery: Battery, house: House) -> None:
        """ Method that draws a path between the house and battery.

        - battery as a battery object for the battery connection
        - house as the house connection for the house connection. """

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
        Distance is in cells.
        
        - battery as Battery object.
        - house as House object.
        
        Returns: the distance between the the house and battery in grid cells
        as an int. """

        x_distance = abs(battery.cell.x_index - house.cell.x_index)
        y_distance = abs(battery.cell.y_index - house.cell.y_index)

        return x_distance + y_distance
