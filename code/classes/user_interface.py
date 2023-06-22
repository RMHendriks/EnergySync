import pygame
from typing import List
from code.classes.button import Button
from code.classes.text import Text

class UserInterface():

    def __init__(self, grid_size: int, vertical_margin: int, horizontal_margin: int) -> None:
        
        self.grid_size = grid_size
        self.vertical_margin = vertical_margin // 2
        self.horizontal_margin = horizontal_margin // 2

        self.button_list: List[Button] = [Button(125, self.vertical_margin + 50,
                                                 self.test, text="Button!")]
        self.text_list: List[Text] = [Text(self.horizontal_margin + self.grid_size + 100,
                                           self.vertical_margin + 50, "Total Cost:")]

    def draw(self, window: pygame.surface.Surface) -> None:

        for button in self.button_list:
            button.draw(window)

        for text in self.text_list:
            text.draw(window)

    def test(self) -> None:
        print("CLICK!")
