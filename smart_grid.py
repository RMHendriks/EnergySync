import pygame
import csv
from typing import List
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.grid import Grid

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 1020
SPACING = 100
GRID_SIZE = 51


def main() -> None:
    # pygame setup
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH + SPACING, SCREEN_HEIGHT + SPACING))
    clock = pygame.time.Clock()
    running = True

    grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, SPACING)
    grid.make_grid()

    battery_list: List[Battery] = []
    house_list: List[House] = []

    import_neighbourhood(grid, battery_list, house_list, "1")

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        window.fill(pygame.Color("white"))
        draw(window, grid, battery_list, house_list)

        # RENDER YOUR GAME HERE
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


def draw(window: pygame.surface.Surface, grid: Grid, battery_list: List[Battery],
         house_list: List[House]) -> None:
    """ Draw objects to the screen"""

    for cell in grid:
        cell.draw(window)

    for house in house_list:
        house.draw(window)

    for battery in battery_list:
        battery.draw(window)

def import_neighbourhood(grid: Grid, battery_list: List[Battery],
                         house_list: List[House] ,district: str) -> None:
    """ Import a neighboorhoud by reading the supplied csv file"""

    # open the battery csv file
    with open(f"data/neighbourhoods/district_{district}/district-{district}_batteries.csv") as file:
        csv_battery_list = csv.reader(file)

        # skip the header
        next(csv_battery_list)

        for battery in csv_battery_list:
            position = battery[0].split(",")
            cell = grid.get_cell_by_index(int(position[0]), int(position[1]))
            battery_object = Battery(cell, float(battery[1]))
            cell.battery = battery_object
            battery_list.append(battery_object)

    # open the house csv file
    with open(f"data/neighbourhoods/district_{district}/district-{district}_houses.csv") as file:
        csv_house_list = csv.reader(file)

        # skip the header
        next(csv_house_list)

        for house in csv_house_list:
            cell = grid.get_cell_by_index(int(house[0]), int(house[1]))
            house_object = House(cell, float(house[2]))
            cell.house = house_object
            house_list.append(house_object)


if __name__ == "__main__":
    main()