import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from Fish.Common.representations.fish_board import FishBoardModel
from Fish.Common.views.pieces_view import FishBoardView

model = FishBoardModel.create_with_same_fish_amount(4, 4, 2)
FishBoardView.show_window(model)
