import pygame
from classes.grid import Grid

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GRID_SIZE = 50


def main() -> None:
    # pygame setup
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)
    grid.make_grid()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        draw(window, grid)

        # RENDER YOUR GAME HERE
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


def draw(window: pygame.surface.Surface, grid: Grid) -> None:
    """ Draw objects to the screen"""

    for cell in grid:
        cell.draw(window)


if __name__ == "__main__":
    main()