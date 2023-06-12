import pygame

class Cell():
    def __init__(self, x: int, y: int, size: int) -> None:
        self.x = x
        self.y = y
        self.size = size

        self.sprite = self.load_sprite()
    
    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw cell to the screen. """

        window.blit(self.sprite, [self.x, self.y])

    def load_sprite(self) -> None:
        """ Draw cell to the screen. """

        sprite = pygame.image.load("sprites/grid.png")
        return pygame.transform.scale(sprite, (self.size, self.size))