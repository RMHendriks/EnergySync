from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.program import Program

import pygame
from typing import List, Dict
from code.algorithms.algorithm import Algoritm
from code.classes.grid import Grid
from code.classes.button import Button
from code.classes.text import Text

class UserInterface():

    def __init__(self, program: Program, algoritm_list: List[Algoritm],
                 grid_size: int, vertical_margin: int,
                 horizontal_margin: int) -> None:
        
        self.program = program

        self.algorithm_list: List[Algoritm] = algoritm_list

        self.grid_size = grid_size
        self.vertical_margin = vertical_margin // 2
        self.horizontal_margin = horizontal_margin // 2
        
        self.button_dict: Dict[str, Button] = {"execute_algoritm": 
                                               Button(125, self.vertical_margin + 210,
                                                      self.run_algorithm, text="Execute Algorithm!"),
                                               "decrement_delay_timer":
                                               Button(60, self.vertical_margin + 400,  
                                                      self.decrement_timer, text="<<",
                                                      width=75),
                                               "increment_delay_timer":
                                               Button(190, self.vertical_margin + 400,
                                                      self.increment_timer, text=">>",
                                                      width=75),
                                               "decrement_algorithm_list":
                                               Button(75, self.vertical_margin + 125,  
                                                      self.decrement_algoritm_list, text="<<",
                                                      width=100),
                                               "increment_algorithm_list":
                                               Button(175, self.vertical_margin + 125,
                                                      self.increment_algoritm_list, text=">>",
                                                      width=100)}

        self.text_dict: Dict[str, Text] = {"total_cost":
                                           Text(self.horizontal_margin + self.grid_size + 30,
                                                self.vertical_margin + 25, "Total Cost:",
                                                center_text=True),
                                           "total_cables":
                                           Text(self.horizontal_margin + self.grid_size + 30,
                                                self.vertical_margin + 55, "Total Cables:",
                                                center_text=True),
                                           "selected_algoritm":
                                           Text(125, self.vertical_margin + 50, "Selected Algoritm"),
                                           "cable_speed_label":
                                           Text(125, self.vertical_margin + 335, "Cable draw speed (ms):"),
                                           "delay_timer":
                                           Text(125, self.vertical_margin + 400, "Timer in ms",
                                                center_text=False)}

    def draw(self, window: pygame.surface.Surface) -> None:

        for button in self.button_dict.values():
            button.draw(window)

        for text in self.text_dict.values():
            text.draw(window)

    def update(self) -> None:
        """ Update UI elements. """

        self.text_dict["total_cost"].text = f"Total Cost:    {self.program.calculate_total_cost():,}"
        self.text_dict["total_cables"].text = f"Total Cables:  {len(self.program.grid.cable_list):,}"
        self.text_dict["delay_timer"].text = f"{round(self.program.delay_timer_ms, 2)}"
        self.text_dict["selected_algoritm"].text = self.program.algorithm.get_class_name()

    def run_algorithm(self) -> None:

        if self.program.grid.cable_list:
            self.program.grid.clean_grid()

        self.program.execute_algoritm()

    def increment_algoritm_list(self) -> None:

        index = self.algorithm_list.index(self.program.algorithm)

        if index >= len(self.algorithm_list) - 1:
            self.program.algorithm = self.algorithm_list[0]
        else:
            self.program.algorithm = self.algorithm_list[index + 1]

    def decrement_algoritm_list(self) -> None:

        index = self.algorithm_list.index(self.program.algorithm)

        if index == 0:
            self.program.algorithm = self.algorithm_list[-1]
        else:
            self.program.algorithm = self.algorithm_list[index - 1]

    def increment_timer(self) -> None:

        self.program.delay_timer_ms += 10

    def decrement_timer(self) -> None:

        if self.program.delay_timer_ms >= 10:
            self.program.delay_timer_ms -= 10
        else:
            self.program.delay_timer_ms = 0