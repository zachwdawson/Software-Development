from board import FishBoard
from state import FishGameStateFactory
from controllers.fish_game_controller import FishGameBehavior, FishGameController
from views.render import HexGridView
from demos.demo_util import RandomlyGenerateFish, RandomlyGenerateHole
from const import HEXES_ROWS, HEXES_COLUMNS
from structures import Player
from typing import Tuple


def setup(no_holes=False) -> Tuple[FishBoard, HexGridView]:
    hexgrid = HexGridView()
    board = FishBoard(num_rows=HEXES_ROWS, num_cols=HEXES_COLUMNS)

    if not no_holes:
        board = RandomlyGenerateHole(board)

    board = RandomlyGenerateFish(board)

    return board, hexgrid


def Demo2() -> FishGameController:
    """
    Non-Hole board where players have each selected 1 penguin.
    :return: A controller to be execute in main.
    """

    board, hexgrid = setup(no_holes=True)

    player_1 = Player("red", 0, 0, [])
    player_2 = Player("white", 0, 0, [])
    factory = FishGameStateFactory(
        board=board,
        players=[player_1, player_2]
    )
    factory = factory.add_penguin(row=0, col=0, color="red")
    factory = factory.add_penguin(row=1, col=1, color="white")
    state = factory.build()

    behavior = FishGameBehavior(state=state, view=hexgrid)

    controller = FishGameController(
        behavior=behavior,
        view=hexgrid,
        state=state
    )

    return controller


def Demo1() -> FishGameController:
    """
    Players in but no penguins has been selected. No Penguins Rendered.

    :return: A controller to be execute in main.
    """

    board, hexgrid = setup()
    player_1 = Player("red", 0, 0, [])
    player_2 = Player("white", 0, 0, [])
    player_3 = Player("brown", 0, 0, [])
    factory = FishGameStateFactory(
        board=board,
        players=[player_1, player_2, player_3]
    )
    state = factory.build()
    behavior = FishGameBehavior(state=state, view=hexgrid)

    controller = FishGameController(
        behavior=behavior,
        view=hexgrid,
        state=state
    )

    return controller
