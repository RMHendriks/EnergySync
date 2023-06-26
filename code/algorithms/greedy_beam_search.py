import random
from queue import Queue
from typing import List, Dict
from copy import copy, deepcopy
from code.algorithms.algorithm import Algorithm
from code.classes.grid import Grid
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable


class GreedyBeamSearch(Algorithm):
    """ Class that implements the greedy algorithm
    for the smart grid problem. """

    def __init__(self, grid: Grid) -> None:
        
        self.grid: Grid = grid

    def calculate_solution(self) -> None:
        """ Method that calculates the results of the function. """

        cycle_counter = 1
        beam_width = 1
        lookahead_depth = 1

        while(len(self.grid.house_list) != len(self.grid.allocated_house_list)):

            random.shuffle(self.grid.house_list)

            for house in self.grid.house_list:
                print(f"House: {self.grid.house_list.index(house)}")
                print(len(self.grid.cable_list))

                states: List[Grid] = [deepcopy(self.grid)]
                
                for _ in range(lookahead_depth):
                    
                    next_gen_states: List[Grid] = []

                    for state in states:
                        
                        if not state.non_allocated_house_list:
                            break

                        lookahead_house = state.non_allocated_house_list[0]

                        for battery in state.battery_list:
                            if battery.capacity > lookahead_house.max_output:
                                child_grid = deepcopy(state)

                                battery.capacity -= lookahead_house.max_output
                                battery.house_list.append(lookahead_house)
                                lookahead_house.battery = battery
                                child_grid.lookahead_battery_list += state.lookahead_battery_list
                                child_grid.lookahead_battery_list.append(battery)
                                child_grid.allocated_house_list.append(lookahead_house)
                                child_grid.non_allocated_house_list.pop(0)
                                self.draw_path(child_grid, battery, house)
                                next_gen_states.append(child_grid)

                    # Prune the results to match the beam size
                    if len(next_gen_states) > beam_width:
                        next_gen_states.sort(key=lambda x: len(x.cable_list))
                        next_gen_states = next_gen_states[:beam_width]
                    states = next_gen_states
                
                if len(states) > 0:
                    best_state = min(states, key=lambda x: len(x.cable_list))
                    battery = best_state.lookahead_battery_list[0]                    
                    battery = self.grid.get_battery_by_index(battery.cell.x_index, battery.cell.y_index)
                    battery.capacity -= house.max_output
                    battery.house_list.append(house)
                    house.battery = battery
                    self.grid.allocated_house_list.append(house)
                    self.grid.non_allocated_house_list.pop(self.grid.non_allocated_house_list.index(house))
                    self.draw_path(self.grid, battery, house)
                else:
                    cycle_counter += 1
                    self.grid.clean_grid()
                    break

                for battery in self.grid.battery_list:
                    print(f"{battery}: {battery.capacity}")
        print(f"Solution found in {cycle_counter} cycle(s).")

    def draw_path(self, grid: Grid, battery: Battery, house: House) -> None:
        """ Method that draws a path between the house and battery. """

        if battery is None:
            Exception("House misses a battery connection.")

        house_index = house.cell.get_index()
        battery_index = battery.cell.get_index()

        delta = (battery_index[0] - house_index[0], battery_index[1] - house_index[1])
        incerement_x = 1 if delta[0] > 0 else -1
        incerement_y = 1 if delta[1] > 0 else -1

        for x in range(house_index[0], battery_index[0] + incerement_x, incerement_x):
            cell = grid.grid[x][house_index[1]]
            cable = Cable(cell, battery, house)
            cell.cable_list.append(cable)
            house.cable_list.append(cable)
            grid.cable_list.append(cable)

        for y in range(house_index[1] + incerement_y, battery_index[1] + incerement_y, incerement_y):
            cell = grid.grid[battery_index[0]][y]
            cable = Cable(cell, battery, house)
            cell.cable_list.append(cable)
            house.cable_list.append(cable)
            grid.cable_list.append(cable)

        if (battery_index[0] != house.cable_list[-1].cell.x_index or
            battery_index[1] != house.cable_list[-1].cell.y_index):
            Exception("Cables are not connected to the battery") 

    def calculate_distance(self, battery: Battery, house: House) -> int:
        """ Calculates the distance between a house and a battery. 
        Distance is in cells. """

        x_distance = abs(battery.cell.x_index - house.cell.x_index)
        y_distance = abs(battery.cell.y_index - house.cell.y_index)

        return x_distance + y_distance
