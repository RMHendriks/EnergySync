import pygame
import csv
import json
from typing import List
from statistics import mean, median
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable
from code.classes.grid import Grid
from code.algorithms.random import Random

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 1020
SPACING = 100
GRID_SIZE = 51
NEIGHBOURHOOD = "1"

BATTERY_COST = 5000
CABLE_COST = 9


def main() -> None:
    # pygame setup
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH + SPACING, SCREEN_HEIGHT + SPACING))
    clock = pygame.time.Clock()
    running = True

    battery_list: List[Battery] = []
    house_list: List[House] = []
    cable_list: List[Cable] = []

    grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, SPACING, battery_list, house_list, cable_list)
    grid.make_grid()

    import_neighbourhood(grid, battery_list, house_list)

    cost_list: List[int] = []

    # calculate a random solution
    for _ in range(100):
        algorithm = Random(grid)
        algorithm.calculate_solution()
        cost_list.append(calculate_total_cost(grid))
        print(calculate_total_cost(grid))
        grid.clean_grid()
    
    print(f"Average: {round(mean(cost_list))}")
    print(f"Median: {round(median(cost_list))}")

    # write the results to a csv file
    with open("data.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(["Results"])
        for cost in cost_list:
            writer.writerow([cost])

    # generate_output(grid)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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


def calculate_total_cost(grid: Grid) -> int:
    """ Calculate the total costs of the cables and batteries on the grid. """

    return len(grid.battery_list) * BATTERY_COST + len(grid.cable_list) * CABLE_COST


def generate_output(grid: Grid) -> None:
    """ Generate a JSON output for the solution of the case. """

    output = [{"district": int(NEIGHBOURHOOD), "costs-shared": calculate_total_cost(grid)}]

    for battery in grid.battery_list:
        house_output = []
        for house in battery.house_list:
            cable_list_str: List[str] = []
            for cable in house.cable_list:
                cable_list_str.append(f"{cable.cell.x_index},{cable.cell.y_index}")

            house_output.append({"location:": f"{house.cell.x_index},{house.cell.y_index}", "output": house.max_output, "cables": cable_list_str})
    
        output.append({"location": f"{battery.cell.x_index},{battery.cell.y_index}", "capacity": battery.max_capacity, "houses": house_output})

        json_data = json.dumps(output)

        with open("output.json", "w") as json_file:
            json_file.write(json_data)

         
if __name__ == "__main__":
    main()