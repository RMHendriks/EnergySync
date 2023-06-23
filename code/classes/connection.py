from typing import Tuple, Dict


SPRITE_DICT: Dict[Tuple[bool], str] = {
                        (True, True, True, True): "sprites/grid_1_2_3_4.png",
                        (True, True, True, False): "sprites/grid_1_2_3.png",
                        (True, True, False, True): "sprites/grid_1_2_4.png",
                        (True, False, True, True): "sprites/grid_1_3_4.png",
                        (False, True, True, True): "sprites/grid_2_3_4.png",
                        (True, False, True, False): "sprites/grid_1_3.png",
                        (False, True, False, True): "sprites/grid_2_4.png",
                        (True, True, False, False): "sprites/grid_1_2.png",
                        (False, True, True, False): "sprites/grid_2_3.png",
                        (False, False, True, True): "sprites/grid_3_4.png",
                        (True, False, False, True): "sprites/grid_1_4.png",
                        (True, False, False, False): "sprites/grid_1.png",
                        (False, True, False, False): "sprites/grid_2.png",
                        (False, False, True, False): "sprites/grid_3.png",
                        (False, False, False, True): "sprites/grid_4.png",
                        (False, False, False, False): "sprites/grid.png"}

HIGHLIGHT_SPRITE_DICT: Dict[Tuple[bool], str] = {
                        (True, False, True, False): "sprites/red_grid_1_3.png",
                        (False, True, False, True): "sprites/red_grid_2_4.png",
                        (True, True, False, False): "sprites/red_grid_1_2.png",
                        (False, True, True, False): "sprites/red_grid_2_3.png",
                        (False, False, True, True): "sprites/red_grid_3_4.png",
                        (True, False, False, True): "sprites/red_grid_1_4.png",
                        (True, False, False, False): "sprites/red_grid_1.png",
                        (False, True, False, False): "sprites/red_grid_2.png",
                        (False, False, True, False): "sprites/red_grid_3.png",
                        (False, False, False, True): "sprites/red_grid_4.png"}


class Connection():
    """ Class used for loading the correct sprite of a grid cell. """

    def __init__(self) -> None:
        
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False

    def transform_to_tuple(self) -> Tuple[bool]:
        """ Returns the connection format as a Tuple of booleans.
        Usefull for use with a dictionary.
        (self.top, self.right, self.bottom, self.left). """

        return (self.top, self.right, self.bottom, self.left)
    
    def load_sprite(self, highlight_sprite=False) -> str:
        """ Loads a cell/cable sprite based on the
        current connections of the grid. """

        if highlight_sprite:
            sprite = HIGHLIGHT_SPRITE_DICT[self.transform_to_tuple()]
        else:
            sprite = SPRITE_DICT[self.transform_to_tuple()]

        return sprite
    
    def clear_connections(self) -> None:
        """ Set all connections back to the base value of False"""

        self.top = False
        self.right = False
        self.bottom = False
        self.left = False       
    
    def __repr__(self) -> str:
        
        return f"{self.top}, {self.right}, {self.bottom}, {self.left}"
