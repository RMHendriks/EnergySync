from abc import ABC, abstractmethod
from copy import copy
from typing import List
from code.classes.grid import Grid
from code.classes.house import House

class Algorithm(ABC):
    
    def __init__(self, grid: Grid) -> None:
        
        self.grid: Grid = grid

        self.non_allocated_house_list: List[House] = copy(self.grid.house_list)
        self.allocated_house_list: List[House] = []

    @abstractmethod
    def calculate_solution(self) -> None:
        pass

    @abstractmethod
    def draw_path(self) -> None:
        pass

    @classmethod
    def get_class_name(self):
        return self.__name__