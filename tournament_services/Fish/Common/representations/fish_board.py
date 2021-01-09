import random
from typing import Dict, List, Set, Tuple, Optional

from Fish.Common.representations.fish_tile import FishTile
from Fish.Common.representations.enumerations.directions_enum import HexDirection
from Fish.Common.representations.types import Coordinate


class FishBoardModel(object):
    """
    A FishBoardModel is {
    rows: Integer
    columns: Integer
    board_map: Dictionary[Coordinate, FishTile]
    coords: [Coordinate]
    }
    INTERP: This is a model of a board for the game Fish. rows and columns are positive integers representing the number
    of rows and columns in a FishBoard model.
    a row is a number of tiles placed horizontally next to one another
    a column is number of tiles placed vertically that are connected, with the first tile's southeast corner connected to a
    second tile's northwest corner, and the second tile's southwest corner will be connected to a third tile's northeast corner.
    This pattern can be repeated after the third tile to expand the height of the column.
    To reference specific positions on this board, we use a coordinate system. Our coordinate system is a Double Height hexagonal
    coordinate system. In this system, moving from left to right on the board will increase like a coordinate system by 1
    each time. The top left-most corner is (0,0), and the x and y coordinates can only increase from there, going right and down respectively.
    In 2 tiles connected to one another, the tile on the right will have an x value 1 greater than the tile on the left,
    while the y value will increase by 2 going to a y value that is directly south of the original tile. When moving south east or
    south west from the original tile, the y value will increase by 1. More explanation is included in Fish/Planning/double_height.pdf

    coords represent a list of all the possible coordinates on the board in our Double Height coordinate system, though not all
    coordinates need to have a tile on them.
    board_map represents a mapping between our coordinate system and the actual tiles in the game. If no mapping exists at that
    coordinate, then there will be no corresponding FishTile there, which is referred to as a hole
    a valid mapping would consist of a coordinate contained in our coords variable on one end of the mapping and a tile object
    on the other end which will contain a valid number of fish.

    """

    def __init__(self, rows: int, columns: int):
        """
        Purpose: Initialize a basic Fish board
        Signature: Int Int -> FishBoardModel
        :param rows: Amount of rows in the Fish board
        :param columns: Amount of columns in the Fish board
        :return: instance of the FishBoardModel
        """
        if rows <= 0 or columns <= 0:
            raise ValueError("Amount of rows and columns needs to be > 0")
        self.rows: int = rows
        self.columns: int = columns
        self.board_map: Dict[Coordinate, FishTile] = dict()
        self.coords: List[Coordinate] = self.create_coords(rows, columns)

    @staticmethod
    def create_coords(rows: int, cols: int) -> List[Coordinate]:
        """
        Purpose: Create coordinates for a hex grid using the "double height" method
        (see design document double_height.pdf in Fish/Planning to explain "double height")
        Signature: Int Int -> [Coordinate]
        :param rows: How many rows our board will have
        :param cols: How many columns our board will have
        :return: list of coordinates on our board
        """
        coords = []
        for col in range(cols):
            # each column contains 2 rows if rows are thought of as left to right,
            # so we need to double the row value
            x_value = col * 2
            for i in range(rows):
                if i % 2 == 0:
                    coordinate = (x_value, i)
                else:
                    coordinate = (x_value + 1, i)
                coords.append(coordinate)
        return coords

    @classmethod
    def create_with_coords_to_fish(cls, rows: int, cols: int, coords_to_fish: List[Tuple[Coordinate, int]]):
        """
        Purpose: Create a board that has amount of fish at certain coordinates
        Signature: Int Int List[Tuple(Coord, Int)] -> FishBoardModel
        :param rows: Amount of rows on board
        :param cols: Amount of columns on board
        :param coords_to_fish: List of tuples that contain coordinates and how many fish they have. If amount of fish is
                               0 or coordinate not specified, there are no fish at that position
        """
        board = FishBoardModel(rows, cols)
        for coord, fish in coords_to_fish:
            board._check_xy_position(coord)
            if fish != 0:
                board.board_map[coord] = FishTile(fish)
        return board

    @classmethod
    def create_with_same_fish_amount(cls, rows: int, cols: int, amount_fish: int = 1):
        """
        Purpose: Create a board with rows and columns and with no holes and the same amount of fish on each tile
        Signature: Int Int Int -> FishBoardModel
        :param rows: (Int) Amount of rows on the board
        :param cols: (Int) Amount of columns on the board
        :param amount_fish: (Int) Amount of fish on each tile
        :return: (FishBoardModel) A board with no holes with the same amount of fish on each column
        """
        if amount_fish <= 0:
            raise ValueError("Amount of fish must be > 0")
        board = FishBoardModel(rows, cols)
        for coord in board.coords:
            board.board_map[coord] = FishTile(num_fish=amount_fish)
        return board

    @classmethod
    def create_with_holes(cls, rows: int, cols: int, coords_with_holes: Set[Coordinate], 
                          one_fish_tiles: int):
        """
        Purpose: Create a board with holes in certain places and a certain amount of 1-fish tiles
        Signature: Int Int Set((Int, Int)) Int -> FishBoard
        :param rows: (Int) Amount of rows on the board
        :param cols: (Int) Amount of cols on the board
        :param coords_with_holes: (Set (Int, Int)) Set of the specific coordinates we want holes in the board
        :param one_fish_tiles: (Int) How many one fish tiles we want to place
        :return: (FishBoard) A board with holes in the specific places and a min number of 1 fish tiles
        """
        board = FishBoardModel(rows, cols)
        board._check_holes(coords_with_holes)
        board._check_minimum_tiles(coords_with_holes, one_fish_tiles)
        amount_one_fish_tiles_placed = 0
        for coord in board.coords:
            # amount of fish
            if amount_one_fish_tiles_placed < one_fish_tiles:
                fish_on_tile = 1
            else:
                fish_on_tile = random.randint(1, FishTile.MAX_AMOUNT_FISH)
            # check set of places with holes in specific places
            if coord not in coords_with_holes:
                board.board_map[coord] = FishTile(num_fish=fish_on_tile)
                amount_one_fish_tiles_placed += 1
        return board

    def _check_holes(self, coords_with_holes: Set[Coordinate]) -> None:
        """
        Purpose: Check coordinates that are supposed to have holes in them to make sure they are valid
        Signature: Set[Coordinate] -> Void
        :param coords_with_holes: Set representing the coordinates with holes in them
        :return: raises ValueError if the holes would not be on the board
        """
        coord_set = set(self.coords)
        for coord in coords_with_holes:
            column, row = coord
            if coord not in coord_set:
                raise ValueError('Specified hole {},{} cannot be created with given board dimensions'.format(column, row))

    def _check_minimum_tiles(self, coords_with_holes: Set[Coordinate], one_fish_tiles: int) -> None:
        """
        Purpose: Check that the minimum amount of tiles can be satisifed
        Signature: Set[Coordinate] Int -> Void
        :param coords_with_holes: Set representing the coordinates that should have holes in them
        :param one_fish_tiles: Int representing a minimum number of 1 fish tiles, can be 0 or greater
        :return: raises ValueError if one fish tiles cant be satisfied or negative
        1-fish tiles, raise TypeError if wrong type
        """
        if one_fish_tiles < 0:
            raise ValueError('Amount of one fish tiles must be > 0')
        amount_tiles_able = len(self.coords) - len(coords_with_holes)
        if one_fish_tiles > amount_tiles_able:
            raise ValueError("Cannot satisfy the minimum amount of 1 fish tiles with this starting amount of tiles: {}"
                             "Amount on board - holes being placed".format(str(amount_tiles_able)))

    def _check_xy_position(self, coordinate: Coordinate, inside_board=True) -> None:
        """
        Purpose: Check to make sure properties of column,row position hold (inside board)
        Signature: Coordinate Bool -> Void
        :param coordinate: represents the coordinate we are trying to check x, y position for
        :param inside_board: boolean representing whether we want to check that x and y aren't inside the board.
                             sometimes we don't want to to have flexibility to check neighbors that are outside the
                             board
        """
        if coordinate not in self.coords and inside_board:
            raise ValueError('column, row must be inside of the board coordinates')

    def find_neighbor_in_direction(self, x: int, y: int, direction: HexDirection) -> Tuple[Optional[FishTile], Coordinate]:
        """
        Purpose: Get neighbor in certain direction from a hexagon grid
        Signature: Int Int HexDirection -> Maybe[FishTile] Coordinate
        :param x: (int) The x coordinate that we want to find the neighbor from
        :param y: (int) The y coordinate we want to find the neighbor from
        :param direction: (HexDirection) direction that we want to find a neighbor in
        :return: Maybe[FishTile] Coordinate = a tuple containing the tile of a neighbor plus their x and y coordinates
        """
        starting_coord: Coordinate = (x, y)
        self._check_xy_position(starting_coord, inside_board=False)
        neighbor_coords = (x + direction[0]), (y + direction[1])
        neighbor = self.board_map.get(neighbor_coords, None)
        return neighbor, neighbor_coords

    def find_straight_line_positions(self, x: int, y: int) -> Dict[HexDirection, List[Coordinate]]:
        """
        Purpose: Find all positions reachable via straight lines from a given position
        Signature: Int Int -> Dict[HexDirection, List[Coordinate]]
        :param x: (int) = The x value that we want straight line positions from
        :param y: (int) = The y value that we want straight line positions from
        :return: array of positions that can be reached in a straight line in a dictionary that has keys
                 that are the direction of the line
        """
        overall_pos_dict: Dict[HexDirection, List[Coordinate]] = dict()

        for direction in HexDirection:
            # find straight lines from all directions
            dir_pos_list = self._find_direction_line_positions(x, y, direction.value)
            # concat all lists of coords together
            overall_pos_dict[direction.name] = dir_pos_list
        return overall_pos_dict

    def _find_direction_line_positions(self, x: int, y: int, direction: HexDirection) -> List[Coordinate]:
        """
        Purpose: Helper functions to find positions reachable in one direction for a give position
        Signature: Int Int HexDirection -> [Coordinate]
        :param x: (int) x coordinate that we are finding the straight line from
        :param y: (int) y coordinate that we are finding the straight line from
        :param direction: (HexDirection) = direction that we are find the straight line from
        :return: [Coordinate] = list of coordinates that are reachable in a certain direction
        """
        # make sure it is in board for starting position
        self._check_xy_position((x, y))
        current_tile = self.board_map.get((x, y), None)
        pos_list = []
        while current_tile:
            # check to see if there is a neighbor one step in the new direction that we are going
            current_tile, new_coords = self.find_neighbor_in_direction(x, y, direction)
            if current_tile:
                pos_list.append(new_coords)
                x, y = new_coords
        return pos_list

    def remove_tile(self, x: int, y: int) -> Optional[FishTile]:
        """
        Purpose: Remove a tile from the board at a certain x and y coordinate
        Signature: Int Int -> Maybe[FishTile]
        :param x: (Int) x coordinate to remove a tile from
        :param y: (Int) y coordinate to remove a tile from
        :return: Maybe[FishTile] returns the Tile that has been removed or None if no tile present there
        """
        self._check_xy_position((x, y))
        tile = self.get_tile_at_coord(x, y)
        if tile:
            del self.board_map[(x, y)]
        return tile

    def get_tile_at_coord(self, x: int, y: int) -> Optional[FishTile]:
        """
        Purpose: Retrieve a fish tile at a specific coordinate
        Signature: Int Int -> FishTile
        :param x: (Int) x coordinate to get a tile from
        :param y: (Int) y coordinate to get a tile from
        :return: (Tile/None) returns the Tile at that coordinate or None if no tile there
        """
        self._check_xy_position((x, y))
        return self.board_map.get((x, y), None)

    def get_dimensions(self) -> Tuple[int, int]:
        """
        Purpose: Return the dimensions of the given fish board
        Signature: Void -> (Int, Int)
        :return: Tuple representing the amount of rows and columns in the board
        """
        return self.rows, self.columns

    def get_tile_coords(self) -> List[Coordinate]:
        """
        Purpose: Return all of the coordinates for the given fish board
        Signature: Void -> [Coordinate]
        :return: List of all of the tile coordinates represented as a tuple for the board
        """
        return self.coords

    def get_coords_sorted_by_row(self):
        """
        Purpose: Returns the sorted coordinates of a board row by row
        Signature: Void -> List[Coordinate]
        :returns: A sorted list of coordinates, going row by row
        """
        # Tuple means sort by the y coordinate first, x coordinate second
        return sorted(self.coords, key=lambda coord: (coord[1], coord[0]))

