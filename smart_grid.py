import sys
from typing import List
from code.classes.program import Program
from code.algorithms.algorithm import Algorithm
from code.algorithms.random import Random
from code.algorithms.greedy import Greedy
from code.algorithms.greediest import Greediest
from code.algorithms.greedy_shared import GreedyShared
from code.algorithms.greedy_beam_search import GreedyBeamSearch
from code.algorithms.evolution import Evolution
from code.algorithms.move_batteries_simulated_annealing import MoveBatteriesSimulatedAnnealing


# visualisation mode settings
SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 1020
VERTICAL_MARGIN = 50
HORIZONTAL_MARGIN = 500
ALGORITHM_LIST: List[Algorithm] = [Random, Greedy, Greediest, GreedyShared,
                                   GreedyBeamSearch, Evolution]
NEIGHBOURHOOD_LIST: List[str] = ["1", "2", "3"]

# console mode settings
ITERATIONS = 1

# shared settings
GRID_SIZE = 51
BATTERY_COST = 5000
CABLE_COST = 9
ALGORITHM: Algorithm = Random
NEIGHBOURHOOD = "1"

def main() -> None:
    """ Program entry point. """
    visualisation_mode = True
    if sys.argv and "--console" in sys.argv:
        visualisation_mode = False

    program = Program(NEIGHBOURHOOD, ALGORITHM, ITERATIONS, visualisation_mode,
                      SCREEN_WIDTH, SCREEN_HEIGHT, VERTICAL_MARGIN,
                      HORIZONTAL_MARGIN, GRID_SIZE, NEIGHBOURHOOD_LIST,
                      BATTERY_COST, CABLE_COST, ALGORITHM_LIST)
    program.run()

if __name__ == "__main__":
    main()
