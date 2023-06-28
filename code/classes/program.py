import pygame
import csv
import json
import time
from typing import List
from statistics import mean, median
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable
from code.classes.grid import Grid
from code.classes.cell import Cell
from code.classes.user_interface import UserInterface
from code.algorithms.algorithm import Algorithm
from code.algorithms.move_batteries_simulated_annealing import MoveBatteriesSimulatedAnnealing


class Program():
    """ Class that holds all the logic to run algorithms and show their
    visualisation. """

    def __init__(self, neighhourhood: str, algorithm: Algorithm, iterations=1,
                 visualisation_mode=False, screen_width=1020, screen_height=1020,
                 vertical_margin=0, horizontal_margin=0, grid_size=51,
                 neighhourhood_list:List[str]=[], battery_cost=5000, cable_cost=9,
                 algorithm_list:List[Algorithm]=[]) -> None:
        """ Initializes the program.

        Required parameters:
        - Needs a neighbourhoud as a str (either "1", "2" or "3").
        - Needs an algorithm as a subclass of Algorithm.

        Optional parameters:
        - iterations as an interge for the amount of iterations in console mode (Default = 1).
        - Toggles visualsiation mode on by turing visualisation_mode to True.
        - screen_width to set the size of the width of display as an int in pixels (Default = 1020).
        - screen_height to set the size of the height of display as an int in pixels (Default = 1020).
        - vertical_margin to set the vertical margin of the grid as an int in pixels (Default = 0).
        - horizontal_margin to set the horizontal margin of the grid as an int in pixels (Default = 0).
        - grid size to decide the size of the grid as an int (Default = 51, with the default neighbourhoods this shouldn't be changed).
        - neighourbood_list as a list of neighbourhoods (Default = [], Can be filled with any combination of "1", "2" and "3").
        - battery_cost to decide the cost of the batteries (Default = 5000).
        - cable_cost to decide the cost of the cables (Default = 9).
        - algorithm_list as a list with any subclass of Algorithm (Default = []).

        For visualisation mode: All parameters need to be passed an argument (with the exception of grid_size and iterations).

        For Console mode: Only the amount of iterations needs to passed as an optional argument.
        """

        self.visualisation_mode = visualisation_mode

        # initialize visualisation mode variables
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vertical_margin = vertical_margin
        self.horizontal_margin = horizontal_margin
        self.delay_timer_ms = 20
        self.pause = False
        self.update_cooldown_timer = pygame.time.get_ticks()
        self.house_index = 0
        self.cable_index = 0

        # initialize visualisation mode lists
        self.house_cable_iter_list: List[Cable] = []
        self.highlight_cable_list: List[Cable] = []
        self.algorithm_list: List[Algorithm] = algorithm_list
        self.neighhourhood_list: List[str] = neighhourhood_list

        # initialize console mode variable(s)
        self.iterations = iterations

        # initialize grid and grid requirements 
        self.battery_cost = battery_cost
        self.cable_cost = cable_cost
        self.algorithm: Algorithm = algorithm
        self.neighhourhood = neighhourhood
        self.grid_size = grid_size
        self.grid = Grid(screen_width, screen_height, grid_size, vertical_margin,
                        horizontal_margin)

    def run(self) -> None:
        """ Starts the excecution of the program. """

        self.grid.make_grid()
        self.import_neighbourhood()

        if self.visualisation_mode:
            self.run_visualisation_mode()
        else:
            self.run_console_mode()

    def run_visualisation_mode(self) -> None:
        """ Runs the pygame visualisation. """

        # pygame setup
        pygame.init()
        window = pygame.display.set_mode((self.screen_width + self.horizontal_margin,
                                          self.screen_height + self.vertical_margin))
        clock = pygame.time.Clock()
        running = True

        # change the icon and header of the pygame window
        pygame.display.set_caption('EnergySync - SmartGrid')
        icon = pygame.image.load('sprites/battery_2.png')
        pygame.display.set_icon(icon)

        # assign the connections to a cell for a correct pygame visualisation
        self.grid.assign_connections()
        self.load_sprites()

        # load the ui
        user_interface = UserInterface(self, self.screen_width,
                                       self.vertical_margin,
                                       self.horizontal_margin)

        while running:
            # poll for events
            # pygame.QUIT triggers when the user closed the window
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
        """ Excutes the algoritm (needs to use an empty grid that can be
        achieved by grid.clean_grid()). """

        algorithm: Algorithm = self.algorithm(self.grid)
        algorithm.calculate_solution()

        if self.visualisation_mode:
            self.allocated_house_list = self.grid.allocated_house_list
            self.house_index = 0
            self.cable_index = 0
            self.house_cable_iter_list = iter(self.allocated_house_list[self.house_index].cable_list)
            self.highlight_cable_list = self.copy_cable_list()
            self.load_sprites()

    def execute_algoritm_battery_algorithm(self) -> None:
        """ Executes the battery MoveBatteriesSimulatedAnnealing algorithm"""

        self.house_cable_iter_list = []
        self.highlight_cable_list = []
        self.grid.clean_grid_visualisation()
        algorithm = MoveBatteriesSimulatedAnnealing(self.grid)
        self.grid = algorithm.calculate_solution()
        self.grid.assign_connections()
        self.load_sprites()

    def load_sprites(self) -> None:
        """ Loads the sprites of the houses, batteries and cells for the
        visualisation mode. """

        for battery in self.grid.battery_list:
            battery.load_sprite()

        for house in self.grid.house_list:
            house.load_sprite()

        for cell in self.grid:
            cell.load_sprite()

    def draw(self, window: pygame.surface.Surface, user_interface: UserInterface) -> None:
        """ Draw objects to the screen every frame. Needs a
        pygame.surface.Surface to be used as a window to draw on.
        Needs a UserInterface to draw the user interface to the window. """

        for row in self.grid.grid:
            for cell in row:
                cell.draw(window)

        for cable in self.highlight_cable_list:
            cable.cell.draw(window)

        for house in self.grid.house_list:
            house.draw(window)

        for battery in self.grid.battery_list:
            battery.draw(window)
        
        user_interface.draw(window)

    def update(self, user_interface: UserInterface) -> None:
        """ Updates the logic of the program fot he visualisation every
        frame. Needs a UserInterface as input to update the logic in the
        UI elements. """

        self.update_objects()
        user_interface.update_ui()

    def update_objects(self) -> None:
        """"" Draws a cable every delay_timer_ms ms. The cable thats being
        drawn is drawn in red. Other cables are in a thinner blue. """
        
        # draw objects when not paused and the delay timer ms have passed
        if not self.pause and (pygame.time.get_ticks() - self.update_cooldown_timer >
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

    def calculate_total_cost(self) -> int:
        """ Calculate the total costs of the cables and batteries on the grid. """

        return len(self.grid.battery_list) * self.battery_cost + len(self.grid.cable_list) * self.cable_cost

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

    def import_neighbourhood(self) -> None:
        """ Import a neighboorhoud by reading the supplied csv file.
        Imports the neighbourhood into the grid. """

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
                self.grid.battery_list.append(battery_object)

        # open the house csv file
        with open(f"data/neighbourhoods/district_{self.neighhourhood}/district-{self.neighhourhood}_houses.csv") as file:
            csv_house_list = csv.reader(file)

            # skip the header
            next(csv_house_list)

            for house in csv_house_list:
                cell = self.grid.get_cell_by_index(int(house[0]), int(house[1]))
                house_object = House(cell, float(house[2]))
                cell.house = house_object
                self.grid.house_list.append(house_object)
                self.grid.non_allocated_house_list.append(house_object)

    def swap_neighbourhood(self) -> None:
        """ Changes the grid and loads a new neighbourhood. Clears all lists
        and loads them with the data of the new neighbourhoods. """

        self.house_cable_iter_list = []
        self.highlight_cable_list = []
        self.grid = Grid(self.screen_width, self.screen_height, self.grid_size,
                         self.vertical_margin, self.horizontal_margin)
        self.import_neighbourhood()
        self.grid.assign_connections()
        self.load_sprites()

    def generate_output(self) -> None:
        """ Generate a JSON output for the solution of the case.
        Output gets stored in the root folder of the project as output.json """

        output = [{"district": int(self.neighhourhood),
                   "costs-shared": self.calculate_total_cost()}]

        for battery in self.grid.battery_list:
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
        """ Writes the results of the last iterations in a csv file.
        
        - Needs a list of total costs for every iteration that has been
        run. """

        # write the results to a csv file
        with open("data.csv", "w") as file:
            writer = csv.writer(file)

            writer.writerow(["Results"])
            for cost in cost_list:
                writer.writerow([cost])
