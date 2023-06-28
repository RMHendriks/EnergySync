from abc import ABC, abstractmethod
from code.classes.grid import Grid


class Algorithm(ABC):
    """ Abstract class used as base class for all algorithms. """

    def __init__(self, grid: Grid) -> None:
        """ Initializes an algorithm. All algorithms need a grid as argument.

        - grid as Grid object
        """

        self.grid: Grid = grid

    @abstractmethod
    def calculate_solution(self) -> None:
        pass

    @abstractmethod
    def draw_path(self) -> None:
        pass

    @classmethod
    def get_class_name(self):
        return self.__name__
