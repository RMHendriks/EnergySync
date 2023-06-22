import pygame
from typing import List
from code.classes.grid import Grid
from code.classes.button import Button
from code.classes.text import Text

class UserInterface():

    def __init__(self, grid: Grid, grid_size: int, vertical_margin: int, horizontal_margin: int) -> None:
        
        self.grid = grid

        self.grid_size = grid_size
        self.vertical_margin = vertical_margin // 2
        self.horizontal_margin = horizontal_margin // 2

        self.button_list: List[Button] = [Button(125, self.vertical_margin + 50,
                                                 self.test, text="Button!"),
                                          Button(60, self.vertical_margin + 150,  
                                                 self.decrement_timer, text="<<",
                                                 width=75),
                                          Button(190, self.vertical_margin + 150,
                                                 self.increment_timer, text=">>",
                                                 width=75)]
        self.text_list: List[Text] = [Text(self.horizontal_margin + self.grid_size + 30,
                                           self.vertical_margin + 25, "Total Cost:",
                                           center_text=True),
                                      Text(self.horizontal_margin + self.grid_size + 30,
                                           self.vertical_margin + 55, "Total Cables:",
                                           center_text=True),
                                      Text(125, self.vertical_margin + 150, "Timer in ms",
                                           center_text=False)]

    def draw(self, window: pygame.surface.Surface) -> None:

        for button in self.button_list:
            button.draw(window)

        for text in self.text_list:
            text.draw(window)

    def test(self) -> None:
        print("CLICK!")

    def increment_timer(self) -> None:

        self.grid.delay_timer_ms += 0.1

    def decrement_timer(self) -> None:

        if self.grid.delay_timer_ms >= 0.1:
            self.grid.delay_timer_ms -= 0.1