""" Class representation of a fish board state."""
from typing import List
from structures import Tile, Coordinate
from const import MAX_NUM_FISH


class FishBoard(object):
    """
    A Fish Board represents a board for a game of Fish.
    It is represented by a 2D list of Tiles of size num_rows by num_cols.
    Each tile is a Tile tuple that can be found in structures.py. The tile row and column
    uses the same 'coordinate system' as specified by the oringinal Fish game spec. That is the rows represent
    the tiles that go in a straight line starting at the left going to the right,
    notice that this means no two tiles in a row will be touching.
    The column's start at the top and zig-zag down the corresponding location within a row. It zig-zags because each
    row is offset from the previous row to make each row have adjacent edges. Our coordinate system is not much
    of a coordinate system because each tile stores the row and column of its neightbors in each direcction in a
    Coordinate tuple, None if there is no neighbor in that direction. The list neighboring_coordinates in Board is used
    to iterate over each possible neighbor for each tile, so no math is done to calculate where a tile's neighbour.
    """

    def __init__(self, num_rows, num_cols, board: List[List[Tile]] = None):
        """
        :param num_rows: the number of rows
        :param num_cols: the number of cols
        """
        if num_rows <= 0 or num_cols <= 0:
            raise ValueError(f"[FishGame] : invalid board dimensions: ({num_cols}, {num_rows})")

        self.num_rows = num_rows
        self.num_cols = num_cols

        if board is None:
            self.board: List[List[Tile]] = []
            for r in range(self.num_rows):
                row = []
                for c in range(self.num_cols):
                    tile = Tile.from_coordinate(
                        coordinate=Coordinate(row=r, col=c),
                        num_fish=0,
                        num_rows=num_rows,
                        num_cols=self.num_cols)
                    row.append(tile)
                self.board.append(row)
        else:
            self.board = board

        self.neighboring_coordinates = [
            'top_coordinate',
            'top_right_coordinate',
            'bottom_right_coordinate',
            'bottom_coordinate',
            'bottom_left_coordinate',
            'top_left_coordinate'
        ]

    def retrieve_num_fish(self, row, col):
        """
        Get the number of fish for the Tile at (row,col)
        :param row: the row of the tile to be checked
        :param col: the col of the tile to be checked
        :return: number of fish at given tile -> int
        """
        # retrieve_num_fish : row, col
        # Retrieves number of fish for this tile
        # return int for num_fish
        if not self.valid_row_and_col(row, col):
            raise ValueError(f"[retrieve_num_fish] : invalid row and col: ({row}, {col})")

        return self.board[row][col].num_fish

    def is_tile(self, row, col):
        """
        Check if Tile at (row,col) is a a tile or a hole
        :param row: the row of the tile to be checked
        :param col: the col of the tile to be checked
        :return: False if the Tile is a hole, True otherwise
        """
        # is_tile : row, col
        # Checks if this row and column is a tile or a hole
        # return true if is a tile false if a hole
        if not self.valid_row_and_col(row, col):
            raise ValueError(f"[is_tile] : invalid row and col: ({row}, {col})")

        return self.board[row][col].is_tile

    def create_hole(self, row, col):
        """
        Removes the tile from the board by making it a hole.
        :param row: the row of the tile to be changed
        :param col: the col of the tile to be changed
        :return: self
        """
        if not self.valid_row_and_col(row, col):
            raise ValueError(f"[create_hole] : invalid row and col: ({row}, {col})")
        board = []
        for r in range(self.num_rows):
            row_list = []
            for c in range(self.num_cols):
                if r == row and c == col:
                    tile = Tile.from_dict(
                        {
                            **self.board[row][col]._asdict(),
                            **{"is_tile": False}, **{"num_fish": 0}
                        })
                else:
                    tile = self.board[r][c]
                row_list.append(tile)
            board.append(row_list)
        return FishBoard(num_rows=self.num_rows, num_cols=self.num_cols, board=board)

    def add_fish(self, row, col):
        """
        Add one fish to the tile at row and col
        :param row: the row of the tile to be added to
        :param col: the col of the tile to be added to
        :return: self
        """
        if not self.valid_row_and_col(row, col):
            raise ValueError(f"[add_fish] : invalid row and col: ({row}, {col})")

        if self.retrieve_num_fish(row, col) == MAX_NUM_FISH:
            raise ValueError(f"[add_fish] : max limit ({MAX_NUM_FISH}) of fish met")

        board = []
        for r in range(self.num_rows):
            row_list = []
            for c in range(self.num_cols):
                if r == row and c == col:
                    tile = Tile.from_dict(
                        {**self.board[row][col]._asdict(),
                         **{"num_fish": self.board[row][col].num_fish + 1}
                         }
                    )
                else:
                    tile = self.board[r][c]
                row_list.append(tile)
            board.append(row_list)
        return FishBoard(num_rows=self.num_rows, num_cols=self.num_cols, board=board)

    def valid_row_and_col(self, row, col):
        """
        Determine whether a row and column exist within a given board
        :param row: the row of the tile in question
        :param col: the col of the tile in question
        :return: True if the tile exists, False otherwise
        """
        return (row < self.num_rows) and (row >= 0) and (col < self.num_cols) and (col >= 0)

    def is_reachable_from(self, start_row, start_col, end_row, end_col, unreachable_tiles: List[Coordinate] = None):
        """
        Given the row,col information, determine whether the ending row and column
        is reachable from the starting row and column. Reachability is determined
        if the end row, col follows a straight path from the starting row and column.
        Holes or the provided unreachable tiles act as barriers meaning that tiles on
        or beyond them are not reachable.
        :param start_row: the starting row
        :param start_col: the starting column
        :param end_row: the ending row
        :param end_col: the ending cool
        :param unreachable_tiles: a list of Coordinate that are unreachable at it and past it.
        :return: a boolean representing if the ending row, col is reachable.
        """
        return Coordinate(end_row, end_col) in self.get_reachable_tiles(start_row, start_col, unreachable_tiles)

    def get_reachable_tiles(self, row: int, col: int, unreachable_tiles: List[Coordinate] = None) -> List[Coordinate]:
        """
        Get all reachable tiles from the given row and column.Reachability is determined
        if the end row, col follows a straight path from the starting row and column.
        Holes or the provided unreachable tiles act as barriers meaning that tiles on
        or beyond them are not reachable.
        :param row: the starting tile row
        :param col: the starting tile column
        :param unreachable_tiles: a list of Coordinate that are unreachable at it and past it.
        :return: a list of reachable tile coordinates.
        """
        if not self.valid_row_and_col(row, col):
            raise ValueError(f"[get_reachable_tiles] : invalid row and col: ({row}, {col})")

        start_tile = self.board[row][col]

        if not start_tile.is_tile:
            return []

        valid_tiles = []
        for direction in self.neighboring_coordinates:
            for coordinate in self.get_reachable_tile_coordinates_by_direction(start_tile, direction,
                                                                               unreachable_tiles):
                valid_tiles.append(coordinate)

        return valid_tiles

    def get_reachable_tile_coordinates_by_direction(
            self, start_tile: Tile, direction: str, unreachable_tiles: List[Coordinate] = None) -> List[Coordinate]:
        """
        Retrieves all reachable tiles from the given direction. This means that tiles
        that are holes or proceed after a hole are not include.Reachability is determined
        if the end row, col follows a straight path from the starting row and column.
        Holes or the provided unreachable tiles act as barriers meaning that tiles on
        or beyond them are not reachable.

        :param start_tile: The starting tile.
        :param direction: the direction to get reachable tiles.
        :param unreachable_tiles: a list of Coordinate that are unreachable at it and past it.
        :return: a list of tiles representing all reachable tiles at the given direction
        """

        if unreachable_tiles is None:
            unreachable_tiles = []

        if direction not in self.neighboring_coordinates:
            raise ValueError(f"[get_reachable_tile_coordinates_by_direction] : "
                             f"Invalid Direction Provided. Please use one of {start_tile._fields}")

        next_tile_coordinate = start_tile.__getattribute__(direction)

        if next_tile_coordinate is None or next_tile_coordinate in unreachable_tiles:
            return []
        current_tile = self.board[next_tile_coordinate.row][next_tile_coordinate.col]

        valid_tiles = []
        is_not_done = current_tile.is_tile
        while is_not_done:
            valid_tiles.append(current_tile.coordinate)
            next_tile_coordinate = current_tile.__getattribute__(direction)
            if next_tile_coordinate is None or next_tile_coordinate in unreachable_tiles:
                is_not_done = False
            else:
                current_tile = self.board[next_tile_coordinate.row][next_tile_coordinate.col]
                is_not_done = current_tile.is_tile

        return valid_tiles

    def is_equal(self, board):
        if self.num_cols != board.num_cols or self.num_rows != board.num_rows:
            return False

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                expected = self.board[row][col]
                actual = board.board[row][col]
                if expected != actual:
                    return False
        return True
