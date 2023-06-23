from abc import ABC, abstractmethod

class Algoritm(ABC):
    
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def calculate_solution(self) -> None:
        pass

    @abstractmethod
    def draw_path(self) -> None:
        pass

    @classmethod
    def get_class_name(self):
        return self.__name__