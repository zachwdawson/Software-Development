from enum import Enum


class PlayerColor(Enum):
    """
    Class representing directions for neighbors in a
    double-height representation of hexagons. Applying these values to x,y coordinates will find the possible neighbor
    in that direction.
    """
    RED = 'red'
    WHITE = 'white'
    BROWN = 'brown'
    BLACK = 'black'
