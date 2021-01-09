""" Immutable and simple data representations."""

from typing import Callable, NamedTuple, List, Optional
from const import HEX_HEIGHT, HEX_SIDE, HEX_RADIUS
from enum import Enum

Coordinate = NamedTuple(
    "Coordinate",
    [("row", int),
     ("col", int)]
)

"""
Phase is the state the game is currently in.
Penguins can be placed in INITIAL
Penguins can be moved in FINAL
Nothing can be done in OVER, as the game is over
"""
class GameStatePhase(Enum):
    INITIAL = 1
    FINAL = 2
    OVER = 3


"""
A tile is a simplified form a hexagon tile within the fish game board. It is not 
used for rendering but rather for game state / play logic. 
"""


class Tile(NamedTuple(
    "Tile",
    [("coordinate", Coordinate),
     ("is_tile", bool),
     ("num_fish", int),
     ("top_coordinate", Coordinate),
     ("top_left_coordinate", Coordinate),
     ("top_right_coordinate", Coordinate),
     ("bottom_coordinate", Coordinate),
     ("bottom_left_coordinate", Coordinate),
     ("bottom_right_coordinate", Coordinate)])):
    coordinate: Coordinate
    is_tile: bool
    num_fish: int
    top_coordinate: Coordinate
    top_left_coordinate: Coordinate
    top_right_coordinate: Coordinate
    bottom_coordinate: Coordinate
    bottom_left_coordinate: Coordinate
    bottom_right_coordinate: Coordinate

    @classmethod
    def from_dict(cls, params):
        """
        Create a tile from dictionary parameters
        :param params: the parameters of a tile and their value
        :return: Tile
        """
        return cls(**params)

    @classmethod
    def from_coordinate(cls, coordinate, num_fish, num_rows, num_cols):
        """
        Calculates a tile based on the given information. Used for convenience
        for calculating neighbors.
        :param coordinate: The cooridate location of the tile
        :param num_fish: the number of fish on this tile.
        :param num_rows: the number of rows in this grid
        :param num_cols: the number of columns in this grid.
        :return: A tile
        """
        return cls(
            coordinate=coordinate,
            is_tile=True,
            num_fish=num_fish,
            top_coordinate=cls.calculate_top_neighbor(coordinate=coordinate),
            top_left_coordinate=cls.calculate_top_left_neighbor(coordinate=coordinate),
            top_right_coordinate=cls.calculate_top_right_neighbor(num_cols=num_cols, coordinate=coordinate),
            bottom_coordinate=cls.calculate_bottom_neighbor(num_rows=num_rows, coordinate=coordinate),
            bottom_left_coordinate=cls.calculate_bottom_left_neighbor(num_rows=num_rows, coordinate=coordinate),
            bottom_right_coordinate=cls.calculate_bottom_right_neighbor(
                num_rows=num_rows, num_cols=num_cols, coordinate=coordinate)
        )

    @staticmethod
    def calculate_top_left_neighbor(coordinate: Coordinate) -> Optional[Coordinate]:
        # Find neighbor above and to the left, None if it not a valid tile
        if coordinate.row == 0 or (coordinate.col == 0 and coordinate.row % 2 == 0):
            return None
        elif coordinate.row % 2 == 0:
            return Coordinate(row=coordinate.row - 1, col=coordinate.col - 1)
        return Coordinate(row=coordinate.row - 1, col=coordinate.col)

    @staticmethod
    def calculate_top_right_neighbor(num_cols: int, coordinate: Coordinate) -> Optional[Coordinate]:
        # Find neighbor above and to the right, None if not a valid tile
        if (coordinate.row == 0) or (coordinate.col == num_cols - 1 and coordinate.row % 2 == 1):
            return None
        elif coordinate.row % 2 == 0:
            return Coordinate(row=coordinate.row - 1, col=coordinate.col)
        else:
            return Coordinate(row=coordinate.row - 1, col=coordinate.col + 1)

    @staticmethod
    def calculate_bottom_left_neighbor(num_rows: int, coordinate: Coordinate) -> Optional[Coordinate]:
        # Find neighbor below and to the left, None if not a valid tile
        if (coordinate.row == num_rows - 1) or (coordinate.col == 0 and coordinate.row % 2 == 0):
            return None
        elif coordinate.row % 2 == 0:
            return Coordinate(row=coordinate.row + 1, col=coordinate.col - 1)
        else:
            return Coordinate(row=coordinate.row + 1, col=coordinate.col)

    @staticmethod
    def calculate_bottom_right_neighbor(num_rows, num_cols, coordinate: Coordinate) -> Optional[Coordinate]:
        # Find neighbor below and to the right, None if not a valid tile
        if (coordinate.row == num_rows - 1) or (coordinate.col == num_cols - 1 and coordinate.row % 2 == 1):
            return None
        elif coordinate.row % 2 == 0:
            return Coordinate(row=coordinate.row + 1, col=coordinate.col)
        else:
            return Coordinate(row=coordinate.row + 1, col=coordinate.col + 1)

    @staticmethod
    def calculate_top_neighbor(coordinate: Coordinate) -> Optional[Coordinate]:
        # Find neighbor above and to the left, None if not a valid tile
        if coordinate.row == 0 or coordinate.row == 1:
            return None
        else:
            return Coordinate(row=coordinate.row - 2, col=coordinate.col)

    @staticmethod
    def calculate_bottom_neighbor(num_rows, coordinate: Coordinate) -> Optional[Coordinate]:
        # Find neighbor above and to the left, None if not a valid tile
        if coordinate.row == num_rows - 1 or coordinate.row == num_rows - 2:
            return None
        else:
            return Coordinate(row=coordinate.row + 2, col=coordinate.col)


"""
Event Handler is a tuple that contains the name of the event and the fundtion used when the even happens.
This is important for handling Tkinter button presses.
"""

EventHandler = NamedTuple(
    "EventHandler",
    [('event', str),
     ('handler', Callable)
     ])

"""
A hexagon is a tuple used only for graphical rendering which stores all necessary information 
to draw a hexagon at a specific place.
"""


class Hexagon(NamedTuple(
    "Hexagon",
    [('row', int),
     ('col', int),
     ('x', int),
     ('y', int),
     ('vertices', List[int])
     ])):
    row: int
    col: int
    x: int
    y: int
    vertices: List[int]

    @classmethod
    def create(cls, row, col, x, y):
        # create : int row, int col, int x, int y
        # Creates Hexagon at (row,col) in board and (x,y) in the window.
        # return Hexagon at (row,col), (x,y) and with vertices

        y_const = (int(x / (HEX_SIDE + HEX_HEIGHT)) % 2) * HEX_RADIUS
        vertices = [
            x, y + HEX_RADIUS + y_const,
               x + HEX_HEIGHT, y + y_const,
               x + HEX_HEIGHT + HEX_SIDE, y + y_const,
               x + (2 * HEX_HEIGHT) + HEX_SIDE, y + HEX_RADIUS + y_const,
               x + HEX_HEIGHT + HEX_SIDE, y + (2 * HEX_RADIUS) + y_const,
               x + HEX_HEIGHT, y + (2 * HEX_RADIUS) + y_const
        ]

        return cls(row, col, x, y, vertices)


"""
A Player is a tuple that represents a player in a game. It has a color, age, score to represent the number of fish
collected, and a list of locations for the players penguins.
"""


class Player(NamedTuple(
    "Player",
    [('color', str),
     ('age', int),
     ('score', int),
     ("penguins", List[Coordinate])
     ])):
    color: int
    age: int
    score: int
    penguins: List[Coordinate]

    def owns_penguin(self, row, col):
        for penguin in self.penguins:
            if penguin.row == row and penguin.col == col:
                return True
        return False

    @classmethod
    def from_dict(cls, params):
        # convert tile in dictionary form to Player tuple
        return cls(**params)


"""
Actions represent a move from a start coordinate to an end coordinate for the player with the given color.
"""
Action = NamedTuple(
    "Action",
    [("start", Coordinate),
     ("end", Coordinate),
     ("player_color", str)]
)
