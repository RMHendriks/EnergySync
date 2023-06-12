from classes.cell import Cell

class Grid():
    def make_grid(self, x_len, y_len):
        """
        Makes the grid 

        Precondition: 
        Postcondition:
        """

        grid = [[Cell(x, y) for x in range(x_len)] for y in range(y_len)]


        for row in grid:
            print(row)
        
