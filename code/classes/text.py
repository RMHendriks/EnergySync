import pygame

class Text():
    """ Class that holds text that can be printed to the screen. """
    
    def __init__(self, x: int, y: int, text="PLACEHOLDER", font="agencyfb",
                 size=25, color="black", center_text=False) -> None:
        
        self.x = x
        self.y = y

        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.color = color

        self.center = center_text

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the text to the screen. """
        
        self.text_render = self.font.render(self.text, True,
                                            pygame.Color(self.color))
        if self.center:
            position = self.text_render.get_rect(topleft=(self.x, self.y))
        else:
            position = self.text_render.get_rect(center=(self.x, self.y))

        window.blit(self.text_render, position)
