import pygame
import csv
import json
from typing import List
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.grid import Grid

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 1020
SPACING = 100
GRID_SIZE = 51
NEIGHBOURHOOD = "1"


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

    import_neighbourhood(grid, battery_list, house_list)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            print(pygame.mouse.get_pos())

        # fill the screen with a color to wipe away anything from last frame
        window.fill(pygame.Color("white"))

        # draw the screen with objects
        draw(window, grid, battery_list, house_list)

        # RENDER YOUR GAME HERE
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


def draw(window: pygame.surface.Surface, grid: Grid, battery_list: List[Battery],
         house_list: List[House]) -> None:
    """ Draw objects to the screen"""

    for row in grid.grid:
        for cell in row:
            cell.draw(window)

    for house in house_list:
        house.draw(window)

    for battery in battery_list:
        battery.draw(window)

def import_neighbourhood(grid: Grid, battery_list: List[Battery],
                         house_list: List[House]) -> None:
    """ Import a neighboorhoud by reading the supplied csv file"""

    # open the battery csv file
    with open(f"data/neighbourhoods/district_{NEIGHBOURHOOD}/district-{NEIGHBOURHOOD}_batteries.csv") as file:
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
    with open(f"data/neighbourhoods/district_{NEIGHBOURHOOD}/district-{NEIGHBOURHOOD}_houses.csv") as file:
        csv_house_list = csv.reader(file)

        # skip the header
        next(csv_house_list)

        for house in csv_house_list:
            cell = grid.get_cell_by_index(int(house[0]), int(house[1]))
            house_object = House(cell, float(house[2]))
            cell.house = house_object
            house_list.append(house_object)


def generate_output(battery_list: List[Battery], house_list: List[House]) -> None:

    output_dict = [{"district": int(NEIGHBOURHOOD), "costs-shared": 0}, {"location": ""}]

if __name__ == "__main__":
    main()