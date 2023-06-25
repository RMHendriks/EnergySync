import pygame
import csv
import json
import time
from typing import List
from copy import deepcopy
from statistics import mean, median
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable
from code.classes.grid import Grid
from code.classes.cell import Cell
from code.classes.user_interface import UserInterface
from code.algorithms.algorithm import Algorithm


class Program():

    def __init__(self, visualisation_mode: bool, screen_width: int,
                 screen_height: int, vertical_margin: int,
                 horizontal_margin: int, grid_size: int,
                 neighhourhood: str, iterations: int, battery_cost: int,
                 cable_cost: int, algorithm_list: List[Algorithm],
                 algorithm: Algorithm) -> None:

        self.visualisation_mode = visualisation_mode

        self.algorithm: Algorithm = algorithm

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vertical_margin = vertical_margin
        self.horizontal_margin = horizontal_margin
        self.grid_size = grid_size
        self.neighhourhood = neighhourhood
        self.iterations = iterations

        self.battery_cost = battery_cost
        self.cable_cost = cable_cost

        self.battery_list: List[Battery] = []
        self.house_list: List[House] = []
        self.cable_list: List[Cable] = []
        self.allocated_house_list: List[House] = []
        self.house_cable_iter_list: List[Cable] = []
        self.highlight_cable_list: List[Cable] = []

        self.grid = Grid(screen_width, screen_height, grid_size, vertical_margin,
                        horizontal_margin, self.battery_list, self.house_list,
                        self.cable_list)
        self.algorithm_list: List[Algorithm] = algorithm_list

        self.delay_timer_ms = 100
        self.update_cooldown_timer = pygame.time.get_ticks()
        self.house_index = 0
        self.cable_index = 0

    def run(self) -> None:

        self.grid.make_grid()
        self.import_neighbourhood()

        if self.visualisation_mode:
            self.run_visualisation_mode()
        else:
            self.run_console_mode()

    def import_neighbourhood(self) -> None:
        """ Import a neighboorhoud by reading the supplied csv file"""

        # open the battery csv file
        with open(f"data/neighbourhoods/district_{self.neighhourhood}/district-{self.neighhourhood}_batteries.csv") as file:
            csv_battery_list = csv.reader(file)

            # skip the header
            next(csv_battery_list)

            for battery in csv_battery_list:
                position = battery[0].split(",")
                cell = self.grid.get_cell_by_index(int(position[0]), int(position[1]))
                battery_object = Battery(cell, float(battery[1]))
                cell.battery = battery_object
                self.battery_list.append(battery_object)

        # open the house csv file
        with open(f"data/neighbourhoods/district_{self.neighhourhood}/district-{self.neighhourhood}_houses.csv") as file:
            csv_house_list = csv.reader(file)

            # skip the header
            next(csv_house_list)

            for house in csv_house_list:
                cell = self.grid.get_cell_by_index(int(house[0]), int(house[1]))
                house_object = House(cell, float(house[2]))
                cell.house = house_object
                self.house_list.append(house_object)

    def run_visualisation_mode(self) -> None:
        """ Runs the pygame visualisation. """

        # pygame setup
        pygame.init()
        window = pygame.display.set_mode((self.screen_width + self.horizontal_margin,
                                          self.screen_height + self.vertical_margin))
        clock = pygame.time.Clock()
        running = True

        # assign the connections to a cell for a correct pygame visualisation
        self.grid.assign_connections()
        self.load_sprites()

        # load the ui
        user_interface = UserInterface(self, self.algorithm_list,
                                       self.screen_width, self.vertical_margin,
                                       self.horizontal_margin)

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in user_interface.button_dict.values():
                            if button.clicked():
                                button.trigger_event()

            # fill the screen with a color to wipe away anything from last frame
            window.fill(pygame.Color("white"))

            # draw the screen with objects
            self.draw(window, user_interface)

            # updates the program every frame
            self.update(user_interface)
            
            # update all changes to the screen
            pygame.display.flip()

            # limits FPS to 60
            clock.tick()

        pygame.quit()

    def run_console_mode(self) -> None:
        """ Runs the console mode of the program. """

        cost_list: List[int] = []

        # calculate a random solution
        start_time_program = time.time()
        for iteration in range(self.iterations):
            self.execute_algoritm()
            cost_list.append(self.calculate_total_cost())
            print(self.calculate_total_cost())

            if iteration != self.iterations - 1:
                self.grid.clean_grid()

        end_time_program = time.time()

        print(f"Average: {round(mean(cost_list))}")
        print(f"Median: {round(median(cost_list))}")
        print(f"Total time for the program: {round(end_time_program - start_time_program, 3)} seconds for a total of {self.iterations} iteration(s)")

        # generate a csv file with the results
        self.generate_csv_output(cost_list)

        # write the last result in a JSON file
        self.generate_output()

    def execute_algoritm(self) -> None:
        """ Excutes the algoritm (needs to use an empty grid). """

        algorithm: Algorithm = self.algorithm(self.grid)
        algorithm.calculate_solution()

        if self.visualisation_mode:
            self.allocated_house_list = algorithm.allocated_house_list
            self.house_index = 0
            self.cable_index = 0
            self.house_cable_iter_list = iter(self.allocated_house_list[self.house_index].cable_list)
            self.highlight_cable_list = self.copy_cable_list()

    def draw(self, window: pygame.surface.Surface, user_interface: UserInterface) -> None:
        """ Draw objects to the screen every frame. """

        for row in self.grid.grid:
            for cell in row:
                cell.draw(window)

        for cable in self.highlight_cable_list:
            cable.cell.draw(window)

        for house in self.house_list:
            house.draw(window)

        for battery in self.battery_list:
            battery.draw(window)
        
        user_interface.draw(window)

    def update(self, user_interface: UserInterface) -> None:
        """ Updates the visualisation every frame. """

        self.update_objects()
        user_interface.update()

    def update_objects(self) -> None:
        """"" Draws a cable every delay_timer_ms ms. """
        
        if (pygame.time.get_ticks() - self.update_cooldown_timer >
            self.delay_timer_ms):
            for cable in self.house_cable_iter_list:

                if self.cable_index < len(self.allocated_house_list[self.house_index].cable_list) - 1:

                    # draws a regular (blue) cable
                    next_cell = self.allocated_house_list[self.house_index].cable_list[self.cable_index + 1]
                    cable.cell.assign_connection(next_cell)
    
                    # draws a highlighted (red) cable 
                    next_highlight_cell = self.highlight_cable_list[self.cable_index + 1]
                    self.highlight_cable_list[self.cable_index].cell.assign_connection(next_highlight_cell)


                # load the correct sprites for the regular and highlighted cable
                # don't draw the cable if it's already on the destanation
                if len(self.allocated_house_list[self.house_index].cable_list) > 1:
                    cable.cell.load_sprite()
                    self.highlight_cable_list[self.cable_index].cell.load_sprite(highlight_sprite=True)


                if cable == self.allocated_house_list[self.house_index].cable_list[-1]:
                    self.house_index += 1
                    if self.house_index >= len(self.allocated_house_list):
                        # empties the list to stop iteration when everything
                        # has been drawn
                        self.house_cable_iter_list = []
                        self.highlight_cable_list = []
                        cable.house.load_sprite_connected()

                    else:
                        # resets the cable list for the next house
                        self.highlight_cable_list = self.copy_cable_list()
                        self.house_cable_iter_list = iter(self.allocated_house_list[self.house_index].cable_list)
                        self.cable_index = 0
                        cable.house.load_sprite_connected()
                        break

                self.cable_index += 1
                break

            self.update_cooldown_timer = pygame.time.get_ticks()

    def load_sprites(self) -> None:
        """ Loads the correct cable sprite for the cell """

        for cell in self.grid:
            cell.load_sprite()

    def calculate_total_cost(self) -> int:
        """ Calculate the total costs of the cables and batteries on the grid. """

        return len(self.battery_list) * self.battery_cost + len(self.grid.cable_list) * self.cable_cost

    def copy_cable_list(self) -> List[Cable]:
        """ Copies a cable list and fills the cables with copied cells
        (Deepcopy doesn't work with pygame surfaces)"""

        copied_cable_list = []

        for cable in self.allocated_house_list[self.house_index].cable_list:
            cell = Cell(cable.cell.grid, cable.cell.x, cable.cell.y,
                        cable.cell.size, cable.cell.x_index, cable.cell.y_index)
            battery = cable.cell.battery
            house = cable.cell.house
            copied_cable_list.append(Cable(cell, battery, house))

        return copied_cable_list

    def generate_output(self) -> None:
        """ Generate a JSON output for the solution of the case. """

        output = [{"district": int(self.neighhourhood),
                   "costs-shared": self.calculate_total_cost()}]

        for battery in self.battery_list:
            house_output = []
            for house in battery.house_list:
                cable_list_str: List[str] = []
                for cable in house.cable_list:
                    cable_list_str.append(f"{cable.cell.x_index},{cable.cell.y_index}")

                house_output.append({"location:": f"{house.cell.x_index},{house.cell.y_index}",
                                     "output": house.max_output, "cables": cable_list_str})
        
            output.append({"location": f"{battery.cell.x_index},{battery.cell.y_index}",
                           "capacity": battery.max_capacity, "houses": house_output})

            json_data = json.dumps(output)

            with open("output.json", "w") as json_file:
                json_file.write(json_data)

    def generate_csv_output(self, cost_list: List[int]) -> None:
        """ Writes the results of the last iterations in a csv file. """

        # write the results to a csv file
        with open("data.csv", "w") as file:
            writer = csv.writer(file)

            writer.writerow(["Results"])
            for cost in cost_list:
                writer.writerow([cost])
