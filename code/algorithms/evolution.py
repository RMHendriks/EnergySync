import random
from copy import deepcopy
from typing import List, Tuple, Dict
from copy import copy
from code.algorithms.algorithm import Algorithm
from code.classes.grid import Grid
from code.classes.cell import Cell
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable


class Evolution(Algorithm):
    """ Class that implements the Evolution algorithm
    for the smart grid problem. """

    def __init__(self, grid: Grid) -> None:
        
        self.grid: Grid = grid

        self.fitness_threshold = 900
        self.population: List[Tuple[int, Grid]] = [] # population of solutions with corresponding fitness
        self.max_population: int = 10 # Population size
        self.total_houses = len(self.grid.non_allocated_house_list)
        
    def generate_solution(self) -> Grid:
        """ Method that calculates the results of the function. """

        self.grid.clean_grid()
        self.grid.allocated_house_list = []
        self.generate_greedy_solution(self.grid)
        return deepcopy(self.grid)
    

    def generate_population(self) -> None:
        """ Method that generates a random population of solutions. """
        # Check if population exists
        if not self.population:
            # Generate 10 solutions
            for _ in range(self.max_population):
                solution = self.generate_solution()
                # print(solution)
                fitness = self.fitness(solution)
                print(fitness * 9 + 25000)
                self.population.append((fitness, solution))

        else:
            # Keep the best solution
            self.population.sort(key=lambda x: x[0], reverse=False) # Sort by fitness, high to low
            best_solution = self.population[0]
            self.population = [best_solution]

            # Mutate best solution 8 times and add new solutions to the population
            for _ in range(8):
                mutated_solution = self.mutate(deepcopy(best_solution[1]))
                print("MUTATED SOLUTION: ", mutated_solution)
                fitness = self.fitness(mutated_solution)
                print(fitness)
                self.population.append((fitness, mutated_solution))

            # Generate 2 new random solutions
            for _ in range(2):
                solution = self.generate_solution()
                print("RANDOM SOLUTION: ", solution)
                fitness = self.fitness(solution)
                print(fitness)
                self.population.append((fitness, solution))

    def fitness(self, grid: Grid) -> int:
        """ Method that takes a solution and calculates how well it performs. """
        # The fitness is determined by the inverse of the number of cables
        return len(grid.cable_list)
    
    def mutate(self, grid: Grid) -> Grid:
        """ Method that takes a solution and alters it"""
        houses = random.sample(grid.house_list, len(grid.house_list) // 2) # Select half of houses
        print(len(houses))
        print(len(grid.house_list))
        for house in houses:
            # Remove the house-battery connection
            for cable in house.cable_list:
                self.remove_cable(cable)
            house.cell.battery = None
            house.battery.capacity += house.max_output
            house.battery = None

        return grid


    def calculate_solution(self) -> None:
        """ Method that runs the algorithm"""
        # Define a threshold for fitness level
        while True:
            self.generate_population()
            # Check if we have a solution with high enough fitness
            self.population.sort(key=lambda x: x[0], reverse=False) # Sort by fitness, high to low
            # print(self.population[0][0])
            if self.population[0][0] < self.fitness_threshold:
                break
        return self.population[0][1]

        

    def draw_path(self, start_cell: Cell, end_cell: Cell, battery: Battery,
                  house: House) -> None:
        """ Method that draws a path between the house and battery. """

        if house.cell.battery is None:
            Exception("House misses a battery connection.")

        # if the cable doesn't connect directly to the battery, get the rest of
        # the cable as a connected cable
        if end_cell.battery != battery:
            house.shared_cable_list = self.get_shared_cable(end_cell, battery)

        start_index = start_cell.get_index()
        end_index = end_cell.get_index()

        delta = (end_index[0] - start_index[0], end_index[1] - start_index[1])
        incerement_x = 1 if delta[0] > 0 else -1
        incerement_y = 1 if delta[1] > 0 else -1

        # draw a cable towards the x position of the end_cell
        for x in range(start_index[0], end_index[0] + incerement_x,
                       incerement_x):
            cell = self.grid.grid[x][start_index[1]]
            cable = Cable(cell, battery, house)

            # creates refrences to multiple lists
            cell.cable_list.append(cable)
            house.cable_list.append(cable)
            battery.cable_list.append(cable)
            self.grid.cable_list.append(cable)

        # draw a cable towards the y position of the end_cell
        for y in range(start_index[1] + incerement_y,
                       end_index[1] + incerement_y, incerement_y):
            cell = self.grid.grid[end_index[0]][y]
            cable = Cable(cell, battery, house)

            # creates refrences to multiple lists
            cell.cable_list.append(cable)
            house.cable_list.append(cable)
            battery.cable_list.append(cable)
            self.grid.cable_list.append(cable)

        if (end_index[0] != house.cable_list[-1].cell.x_index or
            end_index[1] != house.cable_list[-1].cell.y_index):
            Exception("Cables are not connected to the" + 
                      " battery or an other cable") 

    def calculate_distance(self, start_cell: Cell, end_cell: Cell) -> int:
        """ Calculates the distance between two cells. 
        Distance is in cells. """

        x_distance = abs(start_cell.x_index - end_cell.x_index)
        y_distance = abs(start_cell.y_index - end_cell.y_index)

        return x_distance + y_distance

    def get_shared_cable(self, connected_cable_cell: Cell,
                         battery: Battery) -> List[Cable]:
        """ Gets the rest of the cable between the shared connection and the
        battery. Needs a cell of the connected cable location and the battery
        to connect to. """

        for cable in connected_cable_cell.cable_list:
            if cable.battery is battery:
                cable_index = cable.house.cable_list.index(cable)
                return cable.house.cable_list[cable_index + 1:]
            
        Exception("Could not find a valid connection")

    
    def generate_greedy_solution(self, grid: Grid):
        """ Method that generates a random solution based ont the Greedy algorithm"""
        
        cycle_counter = 1

        while(self.total_houses != len(grid.allocated_house_list)):

            random.shuffle(grid.non_allocated_house_list)

            for house in grid.non_allocated_house_list:

                battery_dict: Dict[Battery, int] = {}
                cable_dict: Dict[Cable, int] = {}

                # fill the dicts with possible connections and their distance
                for battery in grid.battery_list:
                    if battery.capacity >= house.max_output:
                        distance = self.calculate_distance(house.cell,
                                                           battery.cell)
                        battery_dict[battery] = distance

                        for cable in battery.cable_list:
                            distance = self.calculate_distance(house.cell,
                                                               cable.cell)
                            cable_dict[cable] = distance
                
                # if there are valid batteries and cables, get the shortest
                # connection of both
                if battery_dict and cable_dict:
                    battery_min_distance = min(battery_dict.values())
                    cable_min_dinstance = min(cable_dict.values())

                # connect the cable based on the shortest distance to a cable
                # or directly to a battery
                if (cable_dict and battery_dict and
                   cable_min_dinstance < battery_min_distance):
                    cable: Cable = min(cable_dict, key=cable_dict.get)
                    cable.battery.capacity -= house.max_output
                    cable.battery.house_list.append(house)
                    house.battery = cable.battery
                    grid.allocated_house_list.append(house)
                    self.draw_path(house.cell, cable.cell, cable.battery, house)
                elif battery_dict:
                    battery: Battery = min(battery_dict, key=battery_dict.get)
                    battery.capacity -= house.max_output
                    battery.house_list.append(house)
                    house.battery = battery
                    grid.allocated_house_list.append(house)
                    self.draw_path(battery.cell, house.cell, battery, house)
                else:
                    cycle_counter += 1
                    grid.clean_grid()
                    grid.allocated_house_list = []                    
                    break

        print(f"Solution found in {cycle_counter} cycle(s).")


    def remove_cable(self, cable: Cable) -> None:
        """ Removes a given cable from all related lists """
        try:
            cable.cell.cable_list.remove(cable)
        except ValueError:
            pass
        try:
            cable.house.cable_list.remove(cable)
        except ValueError:
            pass
        try:
            cable.battery.cable_list.remove(cable)
        except ValueError:
            pass
        try:
            self.grid.cable_list.remove(cable)
        except ValueError:
            pass


