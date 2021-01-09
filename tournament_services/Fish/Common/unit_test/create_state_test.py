import unittest

from Fish.Common.representations.enumerations.game_phase import GamePhase
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.fish_board import FishBoardModel
from Fish.Common.representations.game_state import FishGameState, FishGameStateFactory
from Fish.Common.representations.game_state_error import PenguinPlacementError


class CreateStateTest(unittest.TestCase):
    """
    Test cases for creating a game state
    """
    test_board = FishBoardModel.create_with_same_fish_amount(4, 3, 3)
    test_board_valid_col1 = [(0, 0), (0, 2), (1, 1), (1, 3)]
    test_board_valid_col2 = [(2, 0), (2, 2), (3, 3), (3, 1)]

    def test_create_initial_state(self):
        """
        Purpose:Test creating an initial game state where only the ref can remove
                penguins (no players yet)
        Signature: Void -> Void
        """
        board = FishBoardModel.create_with_same_fish_amount(4, 3, 3)
        game_state = FishGameState(board, player_colors=[PlayerColor.RED,
                                                         PlayerColor.BROWN])
        self.assertEqual([PlayerColor.RED, PlayerColor.BROWN], game_state.get_player_order())
        self.assertEqual(PlayerColor.RED, game_state.get_current_turn())
        self.assertEqual(GamePhase.PLACE_PENGUINS, game_state.get_game_phase())

    def test_create_initial_state_rows_cols(self):
        """
        Purpose: Test using convenience method to create board state
        Signature: Void -> Void
        """
        game_state = FishGameStateFactory.create_game_state_with_dimensions(4, 3,
                                                                            [PlayerColor.RED,
                                                                            PlayerColor.BROWN])
        self.assertEqual([PlayerColor.RED, PlayerColor.BROWN], game_state.get_player_order())
        self.assertEqual(PlayerColor.RED, game_state.get_current_turn())
        self.assertEqual(GamePhase.PLACE_PENGUINS, game_state.get_game_phase())

    def test_create_placement_state_no_penguins(self):
        """
        Purpose: Test creating a penguin placement state with no penguins
        Signature: Void -> Void
        """
        game_state = FishGameStateFactory.create_place_penguins_state(
            CreateStateTest.test_board, [(PlayerColor.RED, []), (PlayerColor.BROWN, [])]
        )
        self.assertEqual(GamePhase.PLACE_PENGUINS, game_state.get_game_phase())
        self.assertEqual(2, len(game_state.get_player_order()))

    def test_create_placement_state_same_penguins(self):
        """
        Purpose: Test creating a penguin placement state with same amount of penguins
        Signature: Void -> Void
        """
        game_state = FishGameStateFactory.create_place_penguins_state(
            CreateStateTest.test_board, [(PlayerColor.RED, [(1, 1)]), (PlayerColor.BROWN, [(0, 0)])]
        )
        self.assertEqual(GamePhase.PLACE_PENGUINS, game_state.get_game_phase())
        self.assertEqual(2, len(game_state.get_player_order()))
        self.assertEqual([(0, 0)], game_state.get_penguins_for_player(PlayerColor.BROWN))

    def test_create_placement_state_one_less(self):
        """
        Purpose: Test creating a penguin placement state with second penguin in order having one less penguin
        Signature: Void -> Void
        """
        game_state = FishGameStateFactory.create_place_penguins_state(
            CreateStateTest.test_board, [(PlayerColor.BROWN, [(0, 0)]), (PlayerColor.RED, [])]
        )
        self.assertEqual(GamePhase.PLACE_PENGUINS, game_state.get_game_phase())
        self.assertEqual(2, len(game_state.get_player_order()))
        self.assertEqual([(0, 0)], game_state.get_penguins_for_player(PlayerColor.BROWN))

    def test_create_placement_state_bad_penguin_amount(self):
        """
        Purpose: Test creating a penguin placement state with having the older player having penguins placed already
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishGameStateFactory.create_place_penguins_state(
                CreateStateTest.test_board, [(PlayerColor.RED, []), (PlayerColor.BROWN, [(0, 0)])]
            )

    def test_create_state_too_little_players(self):
        """
        Purpose: Test creating a state with only 1 player
        """
        with self.assertRaises(ValueError):
            FishGameStateFactory.create_place_penguins_state(
                CreateStateTest.test_board, [(PlayerColor.RED, [])]
            )

    def test_create_placement_state_bad_player_amount(self):
        """
        Purpose: Test creating a penguin placement state with too many players
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishGameStateFactory.create_place_penguins_state(
                CreateStateTest.test_board, [(PlayerColor.RED, []), (PlayerColor.BROWN, []),
                                             (PlayerColor.WHITE, []), (PlayerColor.BLACK, []), (PlayerColor.RED, [])]
            )

    def test_create_move_state_valid(self):
        """
        Purpose: Test creating a penguin movement state with correct amount of penguins
        Signature: Void -> Void
        """
        small_board = FishBoardModel.create_with_same_fish_amount(4, 5, 3)
        game_state = FishGameStateFactory.create_move_penguins_state(
            small_board, [(PlayerColor.RED, CreateStateTest.test_board_valid_col1, 0),
                          (PlayerColor.BROWN, CreateStateTest.test_board_valid_col2, 5)]
        )
        self.assertEqual(4, len(game_state.get_penguins_for_player(PlayerColor.RED)))
        self.assertEqual(4, len(game_state.get_penguins_for_player(PlayerColor.BROWN)))

    def test_create_move_state_no_pengs(self):
        """
        Purpose: Test creating a penguin movement state with no penguins throws error
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishGameStateFactory.create_move_penguins_state(
                CreateStateTest.test_board, [(PlayerColor.RED, [], 0), (PlayerColor.BROWN, [], 0)]
            )

    def test_create_move_state_same_place(self):
        """
        Purpose: Test creating a penguin movement state with trying to put penguins in the same place
        Signature: Void -> Void
        """
        with self.assertRaises(PenguinPlacementError):
            valid_posns = [(0, 0), (0, 2), (1, 1), (1, 3)]
            FishGameStateFactory.create_move_penguins_state(
                CreateStateTest.test_board, [(PlayerColor.RED, CreateStateTest.test_board_valid_col1, 0),
                                             (PlayerColor.BROWN, CreateStateTest.test_board_valid_col1, 0)]
            )

    def test_create_end_state_not_end(self):
        """
        Purpose: Test creating a penguin end state where it is not in an end state
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishGameStateFactory.create_end_game_state(
                CreateStateTest.test_board, [(PlayerColor.RED, CreateStateTest.test_board_valid_col1, 0),
                                             (PlayerColor.BROWN, CreateStateTest.test_board_valid_col2, 0)]
            )

    def test_create_end_state_end(self):
        """
        Purpose: Test creating a penguin end state
        Signature: Void -> Void
        """
        small_board = FishBoardModel.create_with_same_fish_amount(4, 2, 3)
        game_state = FishGameStateFactory.create_end_game_state(
            small_board, [(PlayerColor.RED, CreateStateTest.test_board_valid_col1, 0),
                          (PlayerColor.BROWN, CreateStateTest.test_board_valid_col2, 5)]
        )
        self.assertEqual(GamePhase.END_GAME, game_state.get_game_phase())


if __name__ == '__main__':
    unittest.main()
