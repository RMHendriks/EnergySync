import pygame
from typing import Callable


class Button():
    """ Class that contains the UI button. """

    def __init__(self, x: int, y: int, event: Callable, width=200, height=75,
                 background_color=pygame.Color("grey"), font="agencyfb",
                 font_size=25, text="PLACEHOLDER") -> None:
        """ Initializes an UI button.

        Required paramters:
        - x as an int positions on the screen.
        - y as an int positions on the screen.
        - event as function that will get called when the button gets clicked on.

        Optional parameters:
        - width for the button width as an int (Default = 200).
        - height for the button height as an int (Default = 75).
        - background_color as a pygame.Color for the background color of the button (default = pygame.Color("grey")).
        - font as a str (uses pygames system fonts) (Default = "agencyfb").
        - font_size as an int (Default = 25).
        - text as a str for the text on the button. (Default = "PLACEHOLDER"). """

        self.width = width
        self.height = height
        self.text_content = text
        self.event_function = event

        self.font = pygame.font.SysFont(font, font_size)
        self.background_color = background_color
        self.background_hover_color = pygame.Color("grey80")

        self.position = [x - width // 2, y - height // 2,
                         width, height]

        self.text = self.font.render(text, True, pygame.Color("black"))
        self.text_position = self.text.get_rect(center=(x, y))

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draws the button to the screen.

        - Needs a window as pygame.surface.Surface object. """

        if self.clicked():
            pygame.draw.rect(window, self.background_color, self.position)        
            window.blit(self.text, self.text_position)
        else:
            pygame.draw.rect(window, self.background_hover_color, self.position)        
            window.blit(self.text, self.text_position)

    def clicked(self) -> bool:
        """ Checks if the mouse position is inside the button.
        
        Returns: True if the mouse is inside the button, False if not. """

        mouse_position = pygame.mouse.get_pos()

        if (self.position[1] + self.height > mouse_position[1]
           and self.position[1] < mouse_position[1]
           and self.position[0] + self.width > mouse_position[0]
           and self.position[0] < mouse_position[0]):

            return True

        return False

    def trigger_event(self) -> None:
        """ executes the event function of the button. """

        self.event_function()

    def __repr__(self) -> str:
        return f"Button: {self.text_content}"
