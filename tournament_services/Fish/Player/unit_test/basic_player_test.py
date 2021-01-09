import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.fish_board import FishBoardModel
from Fish.Common.representations.game_state import FishGameStateFactory
from Fish.Other.test_harness_transformation import TestHarnessTransformationHelper as THHelper
from Fish.Player.player import BasicPlayer

class BasicPlayerTest(unittest.TestCase):
    """Test player implementation for our basic player"""

    def test_assign_color(self):
        """
        Test assigning a color to a player
        """
        player = BasicPlayer()
        player.assign_color(PlayerColor.RED)
        self.assertEqual(PlayerColor.RED, player.color)

    def test_basic_placement(self):
        """
        Test getting basic placement from this player.
        """
        test_board = FishBoardModel.create_with_same_fish_amount(4, 3, 3)
        test_state = FishGameStateFactory.create_place_penguins_state(test_board,
                                                                      [(PlayerColor.RED, []),
                                                                      (PlayerColor.WHITE, [])])
        player = BasicPlayer()
        placement = player.player_place_penguin(test_state)
        self.assertEqual((0, 0), placement)

    def test_basic_move(self):
        """
        Test getting a basic move from this player
        """
        board_json = [[1, 1, 1], [2, 3, 4], [1, 1, 1]]
        board = THHelper.parse_board(board_json)
        test_board_valid_row1 = [(0, 0), (2, 0), (4, 0)]
        test_board_valid_row2 = [(1, 1), (3, 1), (5, 1)]
        test_state = FishGameStateFactory.create_move_penguins_state(board,
                                                                     [(PlayerColor.RED, test_board_valid_row1, 0),
                                                                      (PlayerColor.BLACK, test_board_valid_row2, 0)],
                                                                     check_penguin_amount=False,
                                                                     turn=PlayerColor.BLACK)

        player = BasicPlayer()
        placement = player.player_move_penguin(test_state)
        self.assertEqual(((5, 1), (4, 2)), placement)

    def test_show_other_players(self):
        """
        Test showing other players colors
        """
        player = BasicPlayer()
        player.show_other_players_colors([PlayerColor.RED, PlayerColor.WHITE])
        self.assertEqual([PlayerColor.RED, PlayerColor.WHITE], player.other_colors)

    def test_show_winners(self):
        """
        Test being informed of winners
        """
        player = BasicPlayer()
        player.inform_of_winners([PlayerColor.RED, PlayerColor.WHITE])
        self.assertEqual([PlayerColor.RED, PlayerColor.WHITE], player.winners)


if __name__ == '__main__':
    unittest.main()
