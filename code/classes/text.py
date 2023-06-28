import pygame


class Text():
    """ Class that holds text that can be printed to the screen. """

    def __init__(self, x: int, y: int, text="PLACEHOLDER", font="agencyfb",
                 font_size=25, color="black", center_text=False) -> None:
        """ Initializes a UI text object.

        Required paramters:
        - x as an int positions on the screen.
        - y as an int positions on the screen.

        Optional parameters:
        - text as a str. (Default = "PLACEHOLDER").
        - font as a str (uses pygames system fonts) (Default = "agencyfb").
        - font_size as an int (Default = 25).
        - color as a str that is supported by pygame.Color (Default = "black").
        - center_text as a bool (Default = False). """

        self.x = x
        self.y = y

        self.font = pygame.font.SysFont(font, font_size)
        self.text = text
        self.color = color

        self.center = center_text

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the text to the screen.

        - Needs a window as pygame.surface.Surface object. """

        self.text_render = self.font.render(self.text, True,
                                            pygame.Color(self.color))
        if self.center:
            position = self.text_render.get_rect(topleft=(self.x, self.y))
        else:
            position = self.text_render.get_rect(center=(self.x, self.y))

        window.blit(self.text_render, position)
