import random
from typing import List
from copy import copy
from code.algorithms.algorithm import Algorithm
from code.classes.grid import Grid
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable

class Greediest(Algorithm):
    """ Class that implements the greediest algorithm
    for the smart grid problem."""

    def __init__(self, grid: Grid) -> None:
        """ Initializes the greediest algorithm.
        
        - grid as Grid object. """

        self.grid: Grid = grid
        total_houses = len(self.grid.non_allocated_house_list)   
        self.threshold = total_houses * 0.72 # 90% self.threshold

    def calculate_solution(self) -> None:
        """ Executes the greedy algorithm in combination with the random
        algorithm to create a grid with valid battery and house connections
        by connecting houses to the closest available batteries and randomly.
        All paths are directly connected to the battery. """

        cycle_counter = 1

        total_houses = len(self.grid.non_allocated_house_list)   

        distance_list = []
        for house in self.grid.non_allocated_house_list:
            for battery in self.grid.battery_list:
                distance = self.calculate_distance(battery, house)
                distance_list.append((distance, house, battery))
        
        # Sort the list by distance
        distance_list.sort(key=lambda x: x[0])

        while len(self.grid.allocated_house_list) != total_houses:

            non_allocated_houses = copy(self.grid.non_allocated_house_list)
            # Iterate over sorted list and make connections
            for distance, house, battery in distance_list:
                if (battery.capacity >= house.max_output and house
                    not in self.grid.allocated_house_list and
                    len(self.grid.allocated_house_list) < self.threshold):
                    battery.capacity -= house.max_output
                    battery.house_list.append(house)
                    house.battery = battery
                    self.grid.allocated_house_list.append(house)
                    non_allocated_houses.remove(house)

            random.shuffle(non_allocated_houses)

            for house in non_allocated_houses:
                
                tmp_battery_list: List[Battery] = copy(self.grid.battery_list)

                while len(tmp_battery_list) > 0:
                    random.shuffle(tmp_battery_list)
                    battery = tmp_battery_list.pop()

                    if battery.capacity >= house.max_output:
                        battery.capacity -= house.max_output
                        battery.house_list.append(house)
                        house.battery = battery
                        self.grid.allocated_house_list.append(house)
                        break

                if len(tmp_battery_list) == 0 and house.battery is None:
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

        delta = (battery_index[0] - house_index[0],
                 battery_index[1] - house_index[1])
        incerement_x = 1 if delta[0] > 0 else -1
        incerement_y = 1 if delta[1] > 0 else -1

        for x in range(house_index[0], battery_index[0] + incerement_x,
                       incerement_x):
            cell = self.grid.grid[x][house_index[1]]
            cable = Cable(cell, battery, house)
            cell.cable_list.append(cable)
            house.cable_list.append(cable)
            self.grid.cable_list.append(cable)

        for y in range(house_index[1] + incerement_y,
                       battery_index[1] + incerement_y, incerement_y):
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
