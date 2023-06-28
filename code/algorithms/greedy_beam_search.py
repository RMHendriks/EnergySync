import random
from typing import List, Dict
from copy import copy, deepcopy
from code.algorithms.algorithm import Algorithm
from code.algorithms.greedy_shared import GreedyShared
from code.classes.grid import Grid
from code.classes.cell import Cell
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable


class GreedyBeamSearch(Algorithm):
    """ Class that implements the greedy beam search algorithm for the smart
    grid problem. The grid will be solved for an ajustable amount of houses
    by the greedy shared algorithm, everything else will be done by this
    algorithm. The algorithm uses a beam search with an ajustable beam and
    depth. Algorithm can share cables with other houses. """

    def __init__(self, grid: Grid) -> None:
        """ Initializes the greedy beam search algorithm that can share cables
        with other houses.

        - grid as Grid object. """

        self.grid: Grid = grid

        # decide how may houses (out of 150) that are being run by this algorithm
        # all houses up to this point will be allocated with a greedy algorithm
        self.total_house_algorithm = 25
        self.beam_width = 5
        self.lookahead_depth = 10

    def calculate_solution(self) -> None:
        """ Executes the random beam search algorithm to create a grid with valid
        battery and house connections by connecting houses to the closest
        available batteries. Paths can be shared with other batteries."""

        cycle_counter = 1

        while(len(self.grid.house_list) != len(self.grid.allocated_house_list)):


            starting_algoritm = GreedyShared(self.grid)
            starting_algoritm.calculate_solution(self.total_house_algorithm)

            extra_house_list = self.grid.house_list[-self.total_house_algorithm:]
            
            random.shuffle(extra_house_list)
            self.grid.non_allocated_house_list = copy(extra_house_list)

            for house in extra_house_list:
                print(f"House: {extra_house_list.index(house) + 1}")

                states: List[State] = [State(deepcopy(self.grid))]
                if self.lookahead_depth > len(self.grid.non_allocated_house_list):
                    self.lookahead_depth = len(self.grid.non_allocated_house_list)

                for depth in range(self.lookahead_depth):
                    
                    next_gen_states: List[State] = []

                    for state in states:
                        if not state.grid.non_allocated_house_list:
                            break
                        
                        lookahead_house = state.grid.non_allocated_house_list[0]
                        for battery in state.grid.battery_list:
                            if battery.capacity > lookahead_house.max_output:
                                child_state = State(deepcopy(state.grid), depth + 1,
                                                    copy(state.battery_history_dict),
                                                    copy(state.end_cell_history_dict))

                                child_battery = child_state.grid.get_battery_by_object(battery)
                                child_house = child_state.grid.get_house_by_object(lookahead_house)

                                # get the shortest cable connection (use battery as base distance)
                                shortest_distance = self.calculate_distance(child_house.cell,
                                                                            child_battery.cell)
                                shortest_distance_cell = child_battery.cell
                                for cable in child_battery.cable_list:
                                    distance = self.calculate_distance(child_house.cell,
                                                                       cable.cell)
                                    if distance < shortest_distance:
                                        shortest_distance = distance
                                        shortest_distance_cell = cable.cell

                                self.create_connection(child_state.grid,
                                                       child_battery,
                                                       child_house,
                                                       shortest_distance_cell)

                                # add battery to the state history and append
                                # the state the the next gen state list
                                child_state.add_battery(depth + 1, battery)
                                child_state.add_cell(depth + 1, shortest_distance_cell)
                                child_state.update()
                                next_gen_states.append(child_state)

                    # prune the results to match the beam size
                    if len(next_gen_states) > self.beam_width:
                        next_gen_states.sort(key=lambda x: x.total_cables)
                        next_gen_states = next_gen_states[:self.beam_width]

                    states = next_gen_states

                # choose the battery with the best future outlook
                if len(states) > 0:
                    best_state = min(states, key=lambda x: x.total_cables)
                    battery = self.grid.get_battery_by_object(best_state.battery_history_dict[1])
                    end_cell = self.grid.get_cell_by_object(best_state.end_cell_history_dict[1])
                    house.cable_list = []
                    self.create_connection(self.grid, battery, house, end_cell)
                else:
                    cycle_counter += 1
                    self.grid.clean_grid()
                    break

        print(f"Solution found in {cycle_counter} cycle(s).")

    def create_connection(self, grid: Grid, battery: Battery, house: House,
                          end_cell: Cell) -> None:
        """ Create a connection between the house and battery. """

        # adds link between house and battery
        battery.capacity -= house.max_output
        battery.house_list.append(house)
        house.battery = battery

        # move the house to the assigned house list
        grid.allocated_house_list.append(house)
        grid.non_allocated_house_list.pop(0)

        # draw the path between the house and battery
        self.draw_path(grid, house.cell, end_cell, battery, house)

    def draw_path(self, grid: Grid, start_cell: Cell, end_cell: Cell,
                  battery: Battery, house: House) -> None:
        """ Method that draws a path between a start cell and end cell.
        Can connect to other cables and stores the rest of the cable between
        the connection and the battery in the house shared_cable_list.

        - start_cell as a Cell object as start of the cable
        - end_cell as a Cell object as end of the cable
        - battery as a battery object for the battery connection
        - house as the house connection for the house connection. """

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
            cell = grid.grid[x][start_index[1]]
            cable = Cable(cell, battery, house)

            # creates refrences to multiple lists
            cell.cable_list.append(cable)
            house.cable_list.append(cable)
            battery.cable_list.append(cable)
            grid.cable_list.append(cable)

        # draw a cable towards the y position of the end_cell
        for y in range(start_index[1] + incerement_y,
                       end_index[1] + incerement_y, incerement_y):
            cell = grid.grid[end_index[0]][y]
            cable = Cable(cell, battery, house)

            # creates refrences to multiple lists
            cell.cable_list.append(cable)
            house.cable_list.append(cable)
            battery.cable_list.append(cable)
            grid.cable_list.append(cable)

        if (end_index[0] != house.cable_list[-1].cell.x_index or
            end_index[1] != house.cable_list[-1].cell.y_index):
            Exception("Cables are not connected to the" + 
                      " battery or an other cable") 

    def calculate_distance(self, start_cell: Cell, end_cell: Cell) -> int:
        """ Calculates the distance between two cells. 
        Distance is in cells.

        - start_cell as Cell object.
        - end_cell as Cell object.

        Returns: the distance between the two cells in grid cells
        as an int. """

        x_distance = abs(start_cell.x_index - end_cell.x_index)
        y_distance = abs(start_cell.y_index - end_cell.y_index)

        return x_distance + y_distance
    
    def get_shared_cable(self, connected_cable_cell: Cell,
                         battery: Battery) -> List[Cable]:
        """ Gets the rest of the cable between the shared connection and the
        battery. Needs a cell of the connected cable location and the battery
        to connect to.
        
        - connected_cable_cell as a Cell object
        - battery as a Battery object
        
        Returns: a list of Cable objects that are shared with
        another house. """

        for cable in connected_cable_cell.cable_list:
            if cable.battery is battery:
                cable_index = cable.house.cable_list.index(cable)
                return cable.house.cable_list[cable_index + 1:]
            
        Exception("Could not find a valid connection")


class State():
    """ Class used for the storage of a grid state and extra info about
    the state. """

    def __init__(self, grid: Grid, grid_gen=0,
                 battery_dict: Dict[int, Battery]={},
                 end_cell_dict: Dict[int, Cell]={}) -> None:
        """ Initializes a State object used to store the state of a grid.
        
        - grid as Grid object
        
        Optional parameters:
        - grid_gen as an int to indicate the genaration of the state
        (Default = 0).
        - battery_dict as a list of Battery objects used to track the
        previous battery choices.
        end_cell_dict as a lsit of Cell objects used to track the cable
        connection points or battery connection points of previous generation
        choices. """
        
        self.grid: Grid = grid

        self.grid_gen = grid_gen
        self.battery_history_dict: Dict[int, Battery] = battery_dict
        self.end_cell_history_dict: Dict[int, Battery] = end_cell_dict
        self.total_cables = len(grid.cable_list)
        self.total_assigned_houses = len(grid.allocated_house_list)
        self.total_non_assigned_houses = len(grid.non_allocated_house_list)

    def update(self) -> None:
        """ Update the stats of the instance acording to the grid. """

        self.total_cables = len(self.grid.cable_list)
        self.total_assigned_houses = len(self.grid.allocated_house_list)
        self.total_non_assigned_houses = len(self.grid.non_allocated_house_list)

    def add_battery(self, depth: int, battery: Battery) -> None:
        """ Adds a battery to the battery history dict.
        
        - depth as an int
        - battery as a Battery object.
        """

        self.battery_history_dict[depth] = battery

    def add_cell(self, depth: int, cell: Cell) -> None:
        """ Adds a cell to the cell history dict.
        - depth as an int
        - battery as a Battery object.
        """

        self.end_cell_history_dict[depth] = cell

    def __repr__(self) -> str:
        return (f"Grid gen:                {self.grid_gen}\n" +
                f"Battery dict:            {self.battery_history_dict}\n" + 
                f"End Cell dict:           {self.end_cell_history_dict}\n" +
                f"Total cables:            {self.total_cables}\n" +
                f"Total assigned houses:   {self.total_assigned_houses}\n" +
                f"Total unassigned houses: {self.total_non_assigned_houses}\n")
