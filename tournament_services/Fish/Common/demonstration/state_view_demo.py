import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.fish_board import FishBoardModel
from Fish.Common.representations.game_state import FishGameStateFactory
from Fish.Common.views.state_view import FishGameStateView


board = FishBoardModel.create_with_same_fish_amount(3, 3, 3)
placed_penguins = [
    (PlayerColor.RED, [(0, 0)]),
    (PlayerColor.WHITE,  [(2, 2)]),
    (PlayerColor.BROWN,  [(1, 1)]),
    (PlayerColor.BLACK, [(2, 0)])
]
state = FishGameStateFactory.create_place_penguins_state(board, placed_penguins)
FishGameStateView.display_state(state)