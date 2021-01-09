from enum import Enum


class HexDirection(Enum):
    """
    Class representing directions for neighbors in a
    double-height representation of hexagons. Applying these values to x,y coordinates will find the possible neighbor
    in that direction.
    """
    SOUTHEAST = [+1, +1]
    NORTHEAST = [+1, -1]
    NORTH = [0, -2]
    NORTHWEST = [-1, -1]
    SOUTHWEST = [-1, +1]
    SOUTH = [0, +2]
