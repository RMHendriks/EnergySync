import random
from copy import deepcopy
from code.classes.grid import Grid
from code.classes.cell import Cell
from code.algorithms.greedy_shared import GreedyShared


class MoveBatteriesSimulatedAnnealing():
    """ Class that holds the algorithm to move batteries to a better location.
    Base on Simulated Annealing. """

    def __init__(self, grid: Grid) -> None:
        """ Initializes the MoveBatteriesSimulatedAnnealing algorithm.

        - grid as Grid object. """

        self.grid = grid
        self.initial_temperature = 100
        self.max_iterations = 500

        # used for linear cooling
        self.cooling_rate = self.initial_temperature / self.max_iterations

    def calculate_solution(self) -> Grid:
        """ Executes the Simulated Annealing algorithm to get a better
        distribution of batteries on the grid.
        
        Returns: a new grid Object with the batteries at their
        new locations. """

        current_best_state = deepcopy(self.grid)
        self.fill_grid(current_best_state)

        current_temperature = self.initial_temperature
        iterations = 1

        while current_temperature > 0 and iterations <= self.max_iterations:

            child_state: Grid = deepcopy(current_best_state)
            child_state.clean_grid()

            battery = random.choice(child_state.battery_list)
            battery.cell.battery = None
            cell = self.get_random_empty_cell(child_state)
            cell.battery = battery
            battery.cell = cell
            self.fill_grid(child_state)

            cost_difference = (self.calculate_cost(current_best_state) - 
                               self.calculate_cost(child_state))

            if (random.random() < self.acceptance_probability(cost_difference,
                                                                   current_temperature)):
                print(iterations, cost_difference, self.calculate_cost(child_state))
                current_best_state = child_state

            iterations += 1
            current_temperature = self.initial_temperature * 0.99 ** iterations

        self.grid = current_best_state
        self.grid.clean_grid()

        return self.grid

    def acceptance_probability(self, cost_difference: float, temperature: float) -> float:
        """ Get the current acceptance probability of the algorithm. 

        - cost_diffrence as a float.
        - temprature as a float.

        Returns: a float as the acceptance probability. """

        return 2 ** (cost_difference / temperature)

    def get_random_empty_cell(self, grid: Grid) -> Cell:
        """ Get a random cell from the grid without a battery or a house.

        - grid as Grid object.

        Return: a Cell object from the grid. """

        while True:
            x_index = random.randrange(len(self.grid.grid))
            y_index = random.randrange(len(self.grid.grid))

            cell = grid.grid[x_index][y_index]

            if cell.battery is None and cell.house is None:
                return cell

    def fill_grid(self, grid: Grid) -> None:
        """ Fills the grid with connections between houses and batteries using
        the greedy algorithm. 
        
        - grid as Grid object. """

        algorithm = GreedyShared(grid)
        algorithm.calculate_solution(use_print_statements=False)

    def calculate_cost(self, gird: Grid) -> int:
        """ Gets the amount of cables on the grid.
         
          - grid as Grid object.
           
        Returns: an int of the amount of cables. """
        
        return len(gird.cable_list)
