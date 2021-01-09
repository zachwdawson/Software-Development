from board import FishBoard
from state import FishGameState
from controllers.fish_game_controller import FishGameBehavior, FishGameController
from views.render import HexGridView
from const import HEXES_ROWS, HEXES_COLUMNS
from structures import Coordinate, Player
from typing import List
from demos.demo_util import RandomlyGenerateFish, RandomlyGenerateHole

def Demo3(holes: List[Coordinate]) -> FishGameController:
    """
    Given the list of holes, render a board with holes at those
    cooridates and 1 fish at every non-hole tile.
    :param holes: List of hole Coordinates
    :return: A controller to be execute in main.
    """

    hexgrid = HexGridView()
    board = FishBoard(num_rows=HEXES_ROWS, num_cols=HEXES_COLUMNS)

    for hole in holes:
        board = board.create_hole(row=hole.row, col=hole.col)

    for row in range(board.num_rows):
        for col in range(board.num_cols):
            if board.retrieve_num_fish(row=row, col=col) == 0 and board.is_tile(row=row, col=col):
                board = board.add_fish(row=row, col=col)

    player_1 = Player("red", 0, 0, [])
    state = FishGameState(
        board=board,
        num_players=1,
        players=[player_1],
        current_player=player_1)
    behavior = FishGameBehavior(state=state, view=hexgrid)

    controller = FishGameController(
        behavior=behavior,
        view=hexgrid,
        state=state
    )

    return controller


def Demo2(n_fish_per_tile=1) -> FishGameController:
    """
    Randomly Generated Holes with 1 Fish on all tiles...
    :return: A controller to be execute in main.
    """

    hexgrid = HexGridView()
    board = FishBoard(num_rows=HEXES_ROWS, num_cols=HEXES_COLUMNS)

    for row in range(board.num_rows):
        for col in range(board.num_cols):
            if board.retrieve_num_fish(row=row, col=col) == 0 and board.is_tile(row=row, col=col):
                for i in range(n_fish_per_tile):
                    board = board.add_fish(row=row, col=col)
    player_1 = Player("red", 0, 0, [])
    state = FishGameState(
        board=board,
        num_players=1,
        players=[player_1],
        current_player=player_1)
    behavior = FishGameBehavior(state=state, view=hexgrid)

    controller = FishGameController(
        behavior=behavior,
        view=hexgrid,
        state=state
    )

    return controller


def Demo1() -> FishGameController:
    """
    "Randomly Generate number of holes, hole locations, number of fish, and
    fish location.

    :return: A controller to be execute in main.
    """

    hexgrid = HexGridView()
    board = FishBoard(num_rows=HEXES_ROWS, num_cols=HEXES_COLUMNS)

    board = RandomlyGenerateHole(board)
    board = RandomlyGenerateFish(board)

    player_1 = Player("red", 0, 0, [])
    state = FishGameState(
        board=board,
        num_players=1,
        players=[player_1],
        current_player=player_1)
    behavior = FishGameBehavior(state=state, view=hexgrid)

    controller = FishGameController(
        behavior=behavior,
        view=hexgrid,
        state=state
    )

    return controller
