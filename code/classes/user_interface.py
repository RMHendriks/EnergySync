from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from code.classes.program import Program

import pygame
from typing import Dict
from code.classes.button import Button
from code.classes.text import Text


class UserInterface():
    """ Class that holds all the logic for the UI buttons,
    text and button events. """

    def __init__(self, program: Program, grid_size: int, vertical_margin: int,
                 horizontal_margin: int) -> None:
        """ Initializes the UI object for the visualisation mode.
        
        - program as a Program object.
        - grid_size as an int
        - vertical_margin to set the vertical margin of the grid as an int
        in pixels.
        - horizontal_margin to set the horizontal margin of the grid as an int
        in pixels. """

        self.program = program

        self.grid_size = grid_size
        self.vertical_margin = vertical_margin // 2
        self.horizontal_margin = horizontal_margin // 2

        self.button_dict: Dict[str, Button] = {
            "execute_algoritm":
            Button(125, self.vertical_margin + 210,
                    self.event_run_algorithm, text="Execute Algorithm!"),
            "decrement_delay_timer":
            Button(60, self.vertical_margin + 400,
                    self.event_decrement_timer, text="<<",
                    width=75),
            "increment_delay_timer":
            Button(190, self.vertical_margin + 400,
                    self.event_increment_timer, text=">>",
                    width=75),
            "decrement_algorithm_list":
            Button(75, self.vertical_margin + 125,
                    self.event_decrement_algoritm_list, text="<<",
                    width=100),
            "increment_algorithm_list":
            Button(175, self.vertical_margin + 125,
                    self.event_increment_algoritm_list, text=">>",
                    width=100),
            "pause_button":
            Button(125, self.vertical_margin + 485,
                   self.event_toggle_pause, font="segoeuisymbol", font_size=40,
                   text="⏸︎"),
            "decrement_neighbourhood_list":
            Button(60, self.vertical_margin + 635,
                    self.event_decrement_neighhourhood_list, text="<<",
                    width=75),
            "increment_neighbourhood_list":
            Button(190, self.vertical_margin + 635,
                    self.event_increment_neighhourhood_list, text=">>",
                    width=75),
            "change_neighbourhood":
            Button(125, self.vertical_margin + 720,
                    self.event_change_neighbourhood,
                    text="Change Neighbourhood!"),
            "battery_algorithm":
            Button(self.horizontal_margin + self.grid_size + 125 ,
                   self.vertical_margin + 720,
                   self.event_execute_battery_algorithm,
                   text="Improve Battery Position!")}

        self.text_dict: Dict[str, Text] = {
            "total_cost":
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
                center_text=False),
            "neighbourhood_label":
            Text(125, vertical_margin + 550, "Select Neighbourhood:"),
            "neighboorhood_selector":
            Text(125, self.vertical_margin + 635, "Neighbourhood",
                center_text=False)}

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the UI to the screen. 

        - Needs a window as pygame.surface.Surface object. """

        for button in self.button_dict.values():
            button.draw(window)

        for text in self.text_dict.values():
            text.draw(window)

    def update_ui(self) -> None:
        """ Update UI elements. """

        self.text_dict["total_cost"].text = f"Total Cost:    {self.program.calculate_total_cost():,}"
        self.text_dict["total_cables"].text = f"Total Cables:  {len(self.program.grid.cable_list):,}"
        self.text_dict["delay_timer"].text = f"{round(self.program.delay_timer_ms, 2)}"
        self.text_dict["selected_algoritm"].text = self.program.algorithm.get_class_name()
        self.text_dict["neighboorhood_selector"].text = self.program.neighhourhood

    def event_run_algorithm(self) -> None:
        """ Runs the current selected algorithm when the user presses the
        button. """

        if self.program.grid.cable_list:
            self.program.grid.clean_grid_visualisation()

        if self.program.pause:
            self.event_toggle_pause()

        self.program.execute_algoritm()

    def event_increment_algoritm_list(self) -> None:
        """ Selects the next algorithm in the program.algorithm_list. """

        index = self.program.algorithm_list.index(self.program.algorithm)

        if index >= len(self.program.algorithm_list) - 1:
            self.program.algorithm = self.program.algorithm_list[0]
        else:
            self.program.algorithm = self.program.algorithm_list[index + 1]

    def event_decrement_algoritm_list(self) -> None:
        """ Selects the next previous in the program.algorithm_list. """

        index = self.program.algorithm_list.index(self.program.algorithm)

        if index == 0:
            self.program.algorithm = self.program.algorithm_list[-1]
        else:
            self.program.algorithm = self.program.algorithm_list[index - 1]

    def event_increment_timer(self) -> None:
        """ Increments the delay timer for the drawing of the lines by 10. """

        self.program.delay_timer_ms += 10

    def event_decrement_timer(self) -> None:
        """ decrements the delay timer for the drawing of the lines by 10. """

        if self.program.delay_timer_ms >= 10:
            self.program.delay_timer_ms -= 10
        else:
            self.program.delay_timer_ms = 0

    def event_toggle_pause(self) -> None:
        """ Toggles a pause to stop or continue drawing the cables in
        visualisation mode. """

        if self.program.pause:
            self.program.pause = False
            self.button_dict["pause_button"].text = self.button_dict["pause_button"].font.render("⏸", True, pygame.Color("black"))
        else:
            self.program.pause = True
            self.button_dict["pause_button"].text = self.button_dict["pause_button"].font.render("⏵︎", True, pygame.Color("black"))

    def event_decrement_neighhourhood_list(self) -> None:
        """ Selects the previous neighbourhood in the
        program.neighbourhood_list. """

        index = self.program.neighhourhood_list.index(self.program.neighhourhood)

        if index == 0:
            self.program.neighhourhood = self.program.neighhourhood_list[-1]
        else:
            self.program.neighhourhood = self.program.neighhourhood_list[index - 1]

    def event_increment_neighhourhood_list(self) -> None:
        """ Selects the next neighbourhood in the
        program.neighbourhood_list. """

        index = self.program.neighhourhood_list.index(self.program.neighhourhood)

        if index >= len(self.program.neighhourhood_list) - 1:
            self.program.neighhourhood = self.program.neighhourhood_list[0]
        else:
            self.program.neighhourhood = self.program.neighhourhood_list[index + 1]

    def event_change_neighbourhood(self) -> None:
        """ Swaps the neigbourhood to the selected neighbourhood in
        visualisation mode. """

        self.program.swap_neighbourhood()

    def event_execute_battery_algorithm(self) -> None:
        """ Executes the battery algorithm that moves the batteries into a
        better position. """

        self.program.execute_algoritm_battery_algorithm()
