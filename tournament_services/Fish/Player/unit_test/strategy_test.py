import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.fish_board import FishBoardModel
from Fish.Common.representations.game_state import FishGameStateFactory
from Fish.Player.strategy import FishBasicStrategy
from Fish.Other.test_harness_transformation import TestHarnessTransformationHelper as THHelper


class StrategyTest(unittest.TestCase):

    def test_valid_next_placement_in_new_row(self):
        """
        Purpose: Tests if the next placement strategy is accurate with an open spot in the next row
        Signature: Void -> Void
        """
        test_board = FishBoardModel.create_with_same_fish_amount(4, 3, 3)
        test_board_valid_row1 = [(0, 0), (2, 0), (4, 0)]
        test_state = FishGameStateFactory.create_move_penguins_state(test_board,
                                                                     [(PlayerColor.RED, test_board_valid_row1, 0),
                                                                      (PlayerColor.BLACK, [], 0)],
                                                                     check_penguin_amount=False)
        coord = FishBasicStrategy(1).find_next_placement(test_state)
        self.assertEqual((1,1), coord)

    def test_valid_next_placement_in_same_row(self):
        """
        Purpose: Tests if the next placement strategy is accurate with an open spot in the same row
        Signature: Void -> Void
        """
        test_board = FishBoardModel.create_with_same_fish_amount(4, 3, 3)
        test_board_valid_row1 = [(0, 0), (2, 0)]
        test_state = FishGameStateFactory.create_move_penguins_state(test_board,
                                                                     [(PlayerColor.RED, test_board_valid_row1, 0),
                                                                      (PlayerColor.BLACK, [], 0)],
                                                                     check_penguin_amount=False)
        coord = FishBasicStrategy(1).find_next_placement(test_state)
        self.assertEqual((4, 0), coord)

    def test_invalid_next_placement(self):
        """
        Purpose: Tests if the next placement strategy raises an error on an filled board
        Signature: Void -> Void
        """
        test_board = FishBoardModel.create_with_same_fish_amount(2, 2, 3)
        test_board_valid_col1 = [(0, 0), (2, 0), (1, 1), (3,1)]
        test_state = FishGameStateFactory.create_move_penguins_state(test_board,
                                                                     [(PlayerColor.RED, test_board_valid_col1, 0),
                                                                      (PlayerColor.BLACK, [], 0)],
                                                                     check_penguin_amount=False)
        with self.assertRaises(ValueError):
            FishBasicStrategy(1).find_next_placement(test_state)

    def test_tie_breaker(self):
        """
        Purpose: Test that the tiebreaker selects the top-most row and left-most column when all moves would result in an equally good
        amount of fish.
        Signature: Void -> Void
        """
        test_board = FishBoardModel.create_with_same_fish_amount(3, 3, 3)
        test_board_valid_row1 = [(0, 0), (2, 0), (4, 0)]
        test_board_valid_row2 = [(1, 1), (3, 1), (5, 1)]
        test_state = FishGameStateFactory.create_move_penguins_state(test_board,
                                                                     [(PlayerColor.RED, test_board_valid_row1, 0),
                                                                      (PlayerColor.BLACK, test_board_valid_row2, 0)],
                                                                     check_penguin_amount=False,
                                                                     turn=PlayerColor.BLACK)
        best_move = FishBasicStrategy(1).find_next_move(test_state)
        self.assertEqual(((1, 1), (0, 2)), best_move)

    def test_base_case(self):
        """
        Purpose: Tests a situation where we look ahead for one turn and the best move is picked for that turn.
        Signature: Void -> Void
        """
        board_json = [[1,1,1],[2,3,4],[1,1,1]]
        board = THHelper.parse_board(board_json)
        test_board_valid_row1 = [(0, 0), (2, 0), (4, 0)]
        test_board_valid_row2 = [(1, 1), (3, 1), (5, 1)]
        test_state = FishGameStateFactory.create_move_penguins_state(board,
                                                                     [(PlayerColor.RED, test_board_valid_row1, 0),
                                                                      (PlayerColor.BLACK, test_board_valid_row2, 0)],
                                                                     check_penguin_amount=False,
                                                                     turn=PlayerColor.BLACK)
        best_move = FishBasicStrategy(1).find_next_move(test_state)
        self.assertEqual(((5, 1), (4, 2)), best_move)

    def test_end_game(self):
        """
        Purpose: Test getting at a deep depth when an end game state is hit
        Signature: Void -> Void
        """
        test_board = FishBoardModel.create_with_same_fish_amount(3, 3, 3)
        test_board_valid_row1 = [(0, 0), (2, 0), (4, 0)]
        test_board_valid_row2 = [(1, 1), (3, 1), (5, 1)]
        test_state = FishGameStateFactory.create_move_penguins_state(test_board,
                                                                     [(PlayerColor.RED, test_board_valid_row1, 0),
                                                                      (PlayerColor.BLACK, test_board_valid_row2, 0)],
                                                                     check_penguin_amount=False,
                                                                     turn=PlayerColor.BLACK)
        best_move = FishBasicStrategy(30).find_next_move(test_state)
        self.assertEqual(((1, 1), (0, 2)), best_move)

    def test_basic_maximin(self):
        """
        Purpose: Test getting a few levels down with a contrived example
        Signature: Void -> Void
        """
        coords_to_fish = [((0, 0), 1), ((2, 0), 1),
                          ((1, 1), 1), ((3, 1), 1),
                          ((0, 2), 2), ((2, 2), 3),
                          ((1, 3), 1), ((3, 3), 1)]
        test_board = FishBoardModel.create_with_coords_to_fish(4, 2, coords_to_fish)
        penguins_first_player = [(0, 0)]
        penguins_second_player = [(3, 1)]
        test_state = FishGameStateFactory.create_move_penguins_state(test_board,
                                                                     [(PlayerColor.RED, penguins_first_player, 0),
                                                                      (PlayerColor.BLACK, penguins_second_player, 0)],
                                                                     check_penguin_amount=False,
                                                                     turn=PlayerColor.BLACK)
        # player moves to get 1 fish after tiebreaker
        best_move = FishBasicStrategy(1).find_next_move(test_state)
        self.assertEqual(((3, 1), (2, 0)), best_move)

        # player moves to square with 3 fish after looking ahead for more moves
        best_move = FishBasicStrategy(2).find_next_move(test_state)
        self.assertEqual(((3, 1), (2, 2)), best_move)

    def test_player_turn_skipped(self):
        """
        Purpose: Test that minimax still works when player turn has to be skipped
        Signature: Void -> Void
        """
        test_board = FishBoardModel.create_with_same_fish_amount(3, 3, 3)
        # this penguin will always be boxed in because the tiebreaker will always block it in
        test_board_valid_col1 = [(0, 2)]
        test_board_valid_col2 = [(2, 0), (2, 2), (3, 1)]
        test_state = FishGameStateFactory.create_move_penguins_state(test_board,
                                                                     [(PlayerColor.RED, test_board_valid_col1, 0),
                                                                      (PlayerColor.BLACK, test_board_valid_col2, 0)],
                                                                     check_penguin_amount=False,
                                                                     turn=PlayerColor.BLACK)
        best_move = FishBasicStrategy(3).find_next_move(test_state)
        self.assertEqual(((2,0), (1, 1)), best_move)


if __name__ == '__main__':
    unittest.main()
