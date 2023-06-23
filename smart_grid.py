import pygame
import csv
import json
import time
from typing import List
from statistics import mean, median
from code.classes.program import Program
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable
from code.classes.grid import Grid
from code.classes.user_interface import UserInterface
from code.algorithms.algorithm import Algoritm
from code.algorithms.random import Random
from code.algorithms.greedy import Greedy
from code.algorithms.greedier import Greedier

VISUALISATION_MODE = True

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 1020
VERTICAL_MARGIN = 50
HORIZONTAL_MARGIN = 500
GRID_SIZE = 51
NEIGHBOURHOOD = "1"
ITERATIONS = 100

BATTERY_COST = 5000
CABLE_COST = 9

ALGORITHM_LIST: List[Algoritm] = [Random, Greedy, Greedier]
ALGORITHM: Algoritm = Random


def main() -> None:
    """ Entry point of the program. """

    program = Program(VISUALISATION_MODE, SCREEN_WIDTH, SCREEN_HEIGHT,
                      VERTICAL_MARGIN, HORIZONTAL_MARGIN, GRID_SIZE,
                      NEIGHBOURHOOD, ITERATIONS, BATTERY_COST, CABLE_COST,
                      ALGORITHM)
    program.run()

if __name__ == "__main__":
    main()
