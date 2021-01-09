import sys
import os

from Fish.Common.representations.game_state_error import PenguinMovementError, PenguinPlacementError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from Fish.Common.representations.game_state import PlayerColor, FishGameStateFactory
from Fish.Common.representations.fish_board import FishBoardModel


import unittest

class GameStateTest(unittest.TestCase):
    """
    Test cases for creating a game state
    """
    test_board = FishBoardModel.create_with_same_fish_amount(4, 3, 3)
    test_board_valid_col1 = [(0, 0), (0, 2), (1, 1), (1, 3)]
    test_board_valid_col2 = [(2, 0), (2, 2), (3, 3), (3, 1)]
    test_board_valid_col3 = [(4, 0), (4, 2), (5, 3), (5, 1)]

    def test_moving_valid_penguin(self):
        """
        Purpose: Test what happens when you attempt to move a penguin to a valid spot.
        Signature: Void -> Void
        """
        small_board = FishBoardModel.create_with_same_fish_amount(4, 5, 3)
        game_state = FishGameStateFactory.create_move_penguins_state(
            small_board, [(PlayerColor.RED, GameStateTest.test_board_valid_col1, 0),
                          (PlayerColor.BROWN, GameStateTest.test_board_valid_col2, 5)],
            turn=PlayerColor.BROWN
        )
        # Valid move from penguin at 3,3 to 4,2
        game_state.move_penguin(PlayerColor.BROWN, (3, 3), (4,2))
        # Tile should be removed now, try going back
        with self.assertRaises(PenguinMovementError):
            game_state.set_turn(PlayerColor.BROWN)
            game_state.move_penguin(PlayerColor.BROWN, (4, 2), (3, 3))

    def test_moving_valid_penguin_turns(self):
        """
        Purpose: Test what happens when you move penguins in turn order
        Signature: Void -> Void
        """
        small_board = FishBoardModel.create_with_same_fish_amount(4, 5, 3)
        game_state = FishGameStateFactory.create_move_penguins_state(
            small_board, [(PlayerColor.RED, GameStateTest.test_board_valid_col1, 0),
                          (PlayerColor.BROWN, GameStateTest.test_board_valid_col3, 5)],
            turn=PlayerColor.BROWN
        )
        # Valid move from penguin at 3,3 to 4,2
        game_state.move_penguin(PlayerColor.BROWN, (4, 2), (3,1))
        # Valid move for next turn
        game_state.move_penguin(PlayerColor.RED, (1,1), (2,0))

        # attempt to move out of order
        with self.assertRaises(ValueError):
            game_state.move_penguin(PlayerColor.RED, (2, 0), (2, 2))



    def test_moving_penguin_to_invalid_or_existing(self):
        """
        Purpose: Test what happens when you attempt to move a penguin to an invalid spot.
        Signature: Void -> Void
        """
        small_board = FishBoardModel.create_with_same_fish_amount(4, 5, 3)
        game_state = FishGameStateFactory.create_move_penguins_state(
            small_board, [(PlayerColor.RED, GameStateTest.test_board_valid_col1, 0),
                          (PlayerColor.BROWN, GameStateTest.test_board_valid_col2, 5)]
        )
        # Moving to a valid spot with another penguin on it
        with self.assertRaises(ValueError):
            game_state.move_penguin(PlayerColor.BROWN, (2, 2), (3, 1))
        # Moving to an invalid spot
        with self.assertRaises(ValueError):
            game_state.move_penguin(PlayerColor.BROWN, (2, 2), (4, 0))

    def test_moving_penguin_from_invalid_or_nonexisting(self):
        """
        Purpose: Test what happens when you attempt to move a penguin from an invalid spot
        (No existing penguin, no tile, not on board, or another player's penguin)
        Signature: Void -> Void
        """
        small_board = FishBoardModel.create_with_same_fish_amount(4, 5, 3)
        game_state = FishGameStateFactory.create_move_penguins_state(
            small_board, [(PlayerColor.BLACK, GameStateTest.test_board_valid_col1, 5),
                          (PlayerColor.BROWN, GameStateTest.test_board_valid_col2, 0)]
        )
        # No penguin
        with self.assertRaises(PenguinMovementError):
            game_state.move_penguin(PlayerColor.BLACK, (1, 4), (2, 3))
        # Not on board
        with self.assertRaises(PenguinMovementError):
            game_state.move_penguin(PlayerColor.BLACK, (10, 10), (11, 9))
        # Other player's penguin
        with self.assertRaises(PenguinMovementError):
            game_state.move_penguin(PlayerColor.BLACK, (3, 3), (4, 2))

    def test_placing_penguin_invalid(self):
        """
        Purpose: Test what happens when you place a penguin where one was already placed, where a tile doesn't exist,
        or off of the board completely.
        Signature: Void -> Void
        """

        test_board_hole = FishBoardModel.create_with_same_fish_amount(4, 3, 3)
        test_board_hole.remove_tile(0,0)
        game_state = FishGameStateFactory.create_place_penguins_state(
            test_board_hole, [(PlayerColor.BLACK, []), (PlayerColor.BROWN, [])]
        )
        # placing at position off board
        with self.assertRaises(PenguinPlacementError):
            game_state.place_penguin(PlayerColor.BLACK, (-1,-1))
        with self.assertRaises(PenguinPlacementError):
            game_state.place_penguin(PlayerColor.BLACK, (10,10))
        # placing where penguin already exists
        game_state.place_penguin(PlayerColor.BLACK, (1, 1))
        with self.assertRaises(PenguinPlacementError):
            game_state.place_penguin(PlayerColor.BROWN, (1, 1))
        # placing where no tile
        with self.assertRaises(PenguinPlacementError):
            game_state.place_penguin(PlayerColor.BROWN, (0,0))

    def test_placing_penguin_valid(self):
        """
        Purpose: Test what happens when you place a penguin in a valid tile on the board.
        Signature: Void -> Void
        """
        test_board_hole = FishBoardModel.create_with_same_fish_amount(4, 3, 3)
        test_board_hole.remove_tile(0,0)
        game_state = FishGameStateFactory.create_place_penguins_state(
            test_board_hole, [(PlayerColor.BLACK, []), (PlayerColor.BROWN, [])]
        )
        game_state.place_penguin(PlayerColor.BLACK, (1, 1))
        game_state.place_penguin(PlayerColor.BROWN, (2, 2))
        game_state.place_penguin(PlayerColor.BLACK, (3, 3))

    def test_if_players_can_move(self):
        """
        Purpose: Test the state if a player can't move, if 1 player can move, and where more than one player can move.
        Signature: Void -> Void
        """
        test_board = FishBoardModel.create_with_same_fish_amount(4, 3, 3)
        game_state = FishGameStateFactory.create_place_penguins_state(
            test_board, [(PlayerColor.BLACK, []), (PlayerColor.BROWN, [])]
        )
        game_state.place_penguin(PlayerColor.BLACK, (0, 0))
        game_state.place_penguin(PlayerColor.BROWN, (1, 1))
        self.assertEqual(True, game_state.can_any_player_move())

        # Remove tiles
        test_board.remove_tile(2, 2)
        test_board.remove_tile(2, 0)
        test_board.remove_tile(0, 2)
        test_board.remove_tile(1, 3)
        game_state_holes = FishGameStateFactory.create_place_penguins_state(
            test_board, [(PlayerColor.BLACK, [(0, 0)]), (PlayerColor.BROWN, [(1, 1)])]
        )
        self.assertEqual(False, game_state_holes.can_any_player_move())

    def test_get_fish(self):
        """
        Purpose: Test getting a player's fish before and after they move on a board
        Signature: Void -> Void
        """
        small_board = FishBoardModel.create_with_same_fish_amount(4, 5, 3)
        game_state = FishGameStateFactory.create_move_penguins_state(
            small_board, [(PlayerColor.BROWN, GameStateTest.test_board_valid_col2, 5),
                          (PlayerColor.BLACK, GameStateTest.test_board_valid_col1, 0)]
        )
        self.assertEqual(5, game_state.get_fish_for_player(PlayerColor.BROWN))
        # Valid move from penguin at 3,3 to 4,2
        game_state.move_penguin(PlayerColor.BROWN, (3, 3), (4, 2))
        self.assertEqual(8, game_state.get_fish_for_player(PlayerColor.BROWN))

    def test_add_fish(self):
        """
        Purpose: Test getting a player's fish before and after adding fish to a player
        Signature: Void -> Void
        """
        small_board = FishBoardModel.create_with_same_fish_amount(4, 5, 3)
        game_state = FishGameStateFactory.create_move_penguins_state(
            small_board, [(PlayerColor.BLACK, GameStateTest.test_board_valid_col1, 0),
                          (PlayerColor.BROWN, GameStateTest.test_board_valid_col2, 5)]
        )
        self.assertEqual(5, game_state.get_fish_for_player(PlayerColor.BROWN))
        game_state.add_fish_to_player(PlayerColor.BROWN, 6)
        self.assertEqual(11, game_state.get_fish_for_player(PlayerColor.BROWN))
        with self.assertRaises(ValueError):
            game_state.add_fish_to_player(PlayerColor.BROWN, -10)

    def test_check_penguin_amount(self):
        """
        Purpose: Test the check penguin's amount function with valid and invalid arguments
        Signature: Void -> Void
        """
        game_state = FishGameStateFactory.create_place_penguins_state(
            GameStateTest.test_board, [(PlayerColor.BLACK, []), (PlayerColor.BROWN, [])]
        )
        # Situation where not all penguins placed
        with self.assertRaises(ValueError):
            game_state.check_penguin_amount(2, {PlayerColor.BLACK: game_state.get_penguins_for_player(PlayerColor.BLACK),
                                               PlayerColor.BROWN: game_state.get_penguins_for_player(PlayerColor.BROWN)
                                               }, True)

        # Situation where not all penguins placed but not needed
        game_state.check_penguin_amount(2, {PlayerColor.BLACK: game_state.get_penguins_for_player(PlayerColor.BLACK),
                                               PlayerColor.BROWN: game_state.get_penguins_for_player(PlayerColor.BROWN)
                                               },False)

        # Situation where all penguins placed
        game_state.set_turn(PlayerColor.BROWN)
        game_state.place_penguin(PlayerColor.BROWN, (0,0), increase_turn=False)
        game_state.place_penguin(PlayerColor.BROWN, (1,1), increase_turn=False)
        game_state.place_penguin(PlayerColor.BROWN, (0,2), increase_turn=False)
        game_state.place_penguin(PlayerColor.BROWN, (2,0), increase_turn=False)

        game_state.set_turn(PlayerColor.BLACK)
        game_state.place_penguin(PlayerColor.BLACK, (2,2), increase_turn=False)
        game_state.place_penguin(PlayerColor.BLACK, (3,3), increase_turn=False)
        game_state.place_penguin(PlayerColor.BLACK, (3,1), increase_turn=False)
        game_state.place_penguin(PlayerColor.BLACK, (1,3), increase_turn=False)
        game_state.check_penguin_amount(2, {PlayerColor.BLACK: game_state.get_penguins_for_player(PlayerColor.BLACK),
                                            PlayerColor.BROWN: game_state.get_penguins_for_player(PlayerColor.BROWN)
                                            }, True)

    def test_remove_invalid_color_from_game(self):
        """
        Purpose: Tests the remove invalid color from game function when an invalid color (not in the game) is removed.
        Signature: Void -> Void
        """
        game_state = FishGameStateFactory.create_place_penguins_state(
            GameStateTest.test_board, [(PlayerColor.BLACK, []), (PlayerColor.BROWN, [])]
        )
        # check if color is not in game
        with self.assertRaises(ValueError):
            game_state.remove_color_from_game(PlayerColor.RED)

    def test_remove_color_from_game_player_info(self):
        """
        Purpose: Tests removing a color from the game, checks to see if the Player Color would be removed from the players
        in the state
        Signature: Void -> Void
        """
        game_state = FishGameStateFactory.create_place_penguins_state(
            GameStateTest.test_board, [(PlayerColor.BLACK, []), (PlayerColor.BROWN, [])]
        )
        # check if removed from player info
        game_state.remove_color_from_game(PlayerColor.BROWN)
        brown_not_in_players = PlayerColor.BROWN in game_state._players.keys()
        black_in_players = PlayerColor.BLACK in game_state._players.keys()
        self.assertFalse(brown_not_in_players)
        self.assertTrue(black_in_players)

    def test_remove_color_from_game_next_player(self):
        """
        Purpose: Tests removing a color from the game, checks to see if the current turn will shift to be the next player's
        turn once the color is removed
        Signature: Void -> Void
        """
        game_state = FishGameStateFactory.create_place_penguins_state(
            GameStateTest.test_board, [(PlayerColor.BLACK, []), (PlayerColor.BROWN, [])]
        )
        turn_before = game_state.get_current_turn()
        self.assertEqual(PlayerColor.BLACK, turn_before)
        game_state.remove_color_from_game(PlayerColor.BLACK)
        turn_after = game_state.get_current_turn()
        self.assertEqual(PlayerColor.BROWN, turn_after)

    def test_remove_color_from_game_order(self):
        """
        Purpose: Tests removing a color from a game, then checks if the state's game order has changed once a player color
        is removed from the game.
        Signature: Void -> Void
        """
        # check if removed from order
        game_state = FishGameStateFactory.create_place_penguins_state(
            GameStateTest.test_board, [(PlayerColor.BLACK, []), (PlayerColor.BROWN, [])]
        )
        order_before = game_state.get_player_order()
        self.assertEqual([PlayerColor.BLACK, PlayerColor.BROWN], order_before)
        game_state.remove_color_from_game(PlayerColor.BLACK)
        order_after = game_state.get_player_order()
        self.assertEqual([PlayerColor.BROWN], order_after)


if __name__ == '__main__':
    unittest.main()
