import os
import sys
import copy
import unittest
from unittest.mock import MagicMock

# relative path importing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from Fish.Admin.referee import Referee
from Fish.Common.game_tree import FishGameTree
from Fish.Common.representations.enumerations.game_phase import GamePhase
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Player.player import BasicPlayer
from Fish.Admin.kicked_player_type import KickedPlayerType


class RefTests(unittest.TestCase):
    """
    This is a class that will run different tests to unit-test our referee
    """

    def raise_exception_while_finding_action(self, fish_game_state):
        """This mocks raising an exception on the players side"""
        raise Exception('Boom')

    # Here we define misbehaving players that can be used to mock a player making an invalid placement in a game
    bad_player_invalid_placement = BasicPlayer()
    bad_player_invalid_placement.player_place_penguin = MagicMock(return_value=(-1, -1))
    bad_player_invalid_move = BasicPlayer()
    bad_player_invalid_move.player_move_penguin = MagicMock(return_value=((-1, -1), (0, 0)))

    # Here we define misbehaving players for failing types returned
    bad_player_failing_type_placement = BasicPlayer()
    bad_player_failing_type_placement.player_place_penguin = MagicMock(return_value=((1, 1), (2, 0)))
    bad_player_failing_type_movement = BasicPlayer()
    bad_player_failing_type_movement.player_move_penguin = MagicMock(return_value=(0, 0))

    # Here we define misbehaving players for throwing an internal exception
    bad_player_exception_placement = BasicPlayer()
    bad_player_exception_placement.player_place_penguin = MagicMock(side_effect=raise_exception_while_finding_action)
    bad_player_exception_movement = BasicPlayer()
    bad_player_exception_movement.player_move_penguin = MagicMock(side_effect=raise_exception_while_finding_action)

    def set_up_game_phases(self, rows, columns, num_players=2, run_placement_phase=False, bad_player_obj=None):
        """
        Purpose: Set up basic game phases for use in testing movement and placement phases
        Signature: Int Int Int Bool PlayerInterface -> Referee
        """
        ref = Referee()
        players = []
        for i in range(num_players):
            if bad_player_obj and i == 0:
                append_obj = bad_player_obj, i + 1
            else:
                append_obj = BasicPlayer(), i + 1
            players.append(append_obj)
        ref._init_board(rows, columns, players)
        if run_placement_phase:
            ref._run_placement_phase()
        return ref

    def test_init_board_2_player(self):
        """
        Test basic properties about initializing a game with 2 logical players
        """
        ref = Referee()
        players = [(BasicPlayer(), 1), (BasicPlayer(), 2)]
        ref._init_board(3, 3, players)

        # Test the amount of players, order according to default order and turn and phase
        self.assertEqual(4, ref.amount_penguins_per_player)
        self.assertEqual([PlayerColor.RED, PlayerColor.WHITE], list(ref.players.keys()))
        self.assertEqual(PlayerColor.RED, ref.current_game_state.get_current_turn())
        self.assertEqual(GamePhase.PLACE_PENGUINS, ref.current_game_state.get_game_phase())
        self.assertEqual([PlayerColor.RED, PlayerColor.WHITE], ref.current_game_state.get_player_order())

    def test_init_board_4_player(self):
        """
        Test basic properties about initializing a game with 4 logical players
        """
        ref = Referee()
        players = [(BasicPlayer(), 1), (BasicPlayer(), 2), (BasicPlayer(), 3), (BasicPlayer(), 4)]
        ref._init_board(5, 5, players)

        # Test the amount of players, order according to default order and turn and phase
        self.assertEqual(2, ref.amount_penguins_per_player)
        self.assertEqual([PlayerColor.RED, PlayerColor.WHITE,
                          PlayerColor.BROWN, PlayerColor.BLACK], list(ref.players.keys()))
        self.assertEqual(PlayerColor.RED, ref.current_game_state.get_current_turn())
        self.assertEqual(GamePhase.PLACE_PENGUINS, ref.current_game_state.get_game_phase())
        self.assertEqual([PlayerColor.RED, PlayerColor.WHITE,
                          PlayerColor.BROWN, PlayerColor.BLACK], ref.current_game_state.get_player_order())

    def test_kick_player_place_penguins(self):
        """
        Test kicking a player in the place_penguins state
        """
        ref = Referee()
        players = [(BasicPlayer(), 1), (BasicPlayer(), 2), (BasicPlayer(), 3), (BasicPlayer(), 4)]
        ref._init_board(5, 5, players)
        ref._add_kicked_player(PlayerColor.RED, GamePhase.PLACE_PENGUINS, cheating=True)

        # Test kicking a player functionality works well
        self.assertEqual({KickedPlayerType.CHEATING: [PlayerColor.RED], KickedPlayerType.FAILING: []}, ref.kicked_players)
        self.assertEqual({KickedPlayerType.CHEATING: [PlayerColor.RED], KickedPlayerType.FAILING: []}, ref.kicked_players)
        self.assertFalse(PlayerColor.RED in ref.current_game_state.get_player_order())
        self.assertFalse(PlayerColor.RED in ref.players.keys())

    def test_run_placement_turn_valid(self):
        """
        Test running a valid placement turn with no issues
        """
        ref = self.set_up_game_phases(5, 5)

        # Test that a penguin is added and turn is incremented
        self.assertEqual(0, len(ref.current_game_state.get_penguins_for_player(PlayerColor.RED)))
        ref._run_placement_turn()
        self.assertEqual(1, len(ref.current_game_state.get_penguins_for_player(PlayerColor.RED)))
        self.assertEqual(PlayerColor.WHITE, ref.current_game_state.get_current_turn())

    def test_run_placement_turn_invalid(self):
        """
        Test running a placement turn where someone makes an invalid move (a bad logical move)
        """
        ref = self.set_up_game_phases(5, 5, num_players=4, bad_player_obj=RefTests.bad_player_invalid_placement)
        ref._run_placement_turn()
        # Test that player is incremented, and player is kicked when cheating
        self.assertEqual(PlayerColor.WHITE, ref.current_game_state.get_current_turn())
        self.assertEqual([PlayerColor.RED], ref.kicked_players[KickedPlayerType.CHEATING])
        self.assertFalse(PlayerColor.RED in ref.current_game_state.get_player_order())

    def test_run_placement_turn_failing_type(self):
        """
        Test running a placement turn with failing type returned
        """
        ref = self.set_up_game_phases(5, 5, num_players=4, bad_player_obj=RefTests.bad_player_failing_type_placement)
        ref._run_placement_turn()

        # Test that player is incremented, and player is kicked when failing
        self.assertEqual(PlayerColor.WHITE, ref.current_game_state.get_current_turn())
        self.assertEqual([PlayerColor.RED], ref.kicked_players[KickedPlayerType.FAILING])
        self.assertFalse(PlayerColor.RED in ref.current_game_state.get_player_order())

    def test_run_placement_turn_failing_error(self):
        """
        Test running a placement turn with internal error on the player side.
        """
        ref = self.set_up_game_phases(5, 5, num_players=4, bad_player_obj=RefTests.bad_player_exception_placement)

        ref._run_placement_turn()

        # Test that player is incremented, and player is kicked when failing
        self.assertEqual(PlayerColor.WHITE, ref.current_game_state.get_current_turn())
        self.assertEqual([PlayerColor.RED], ref.kicked_players[KickedPlayerType.FAILING])
        self.assertFalse(PlayerColor.RED in ref.current_game_state.get_player_order())

    def test_run_movement_turn_valid(self):
        """
        Test running a valid movement turn with no issues
        """
        # player that throws an exception when trying to place it
        ref = self.set_up_game_phases(5, 5, run_placement_phase=True)

        initial_pengs = ref.current_game_state.get_penguins_for_player(player_color=PlayerColor.RED)
        ref._run_movement_turn()
        moved_pengs = ref.current_game_state.get_penguins_for_player(player_color=PlayerColor.RED)
        # Test lists of penguins and number of fish
        self.assertNotEqual(initial_pengs, moved_pengs)
        self.assertGreater(ref.current_game_state.get_fish_for_player(player_color=PlayerColor.RED), 0)

    def test_run_movement_turn_skip(self):
        """
        Test running a movement turn where someone is skipped
        """
        # player that throws an exception when trying to place it
        ref = self.set_up_game_phases(3, 3, num_players=4, run_placement_phase=True)

        # Set player color to black, they can not go and will be skipped
        ref.current_game_state.set_turn(PlayerColor.BLACK)
        ref.current_game_tree = FishGameTree(copy.deepcopy(ref.current_game_state))

        initial_pengs = ref.current_game_state.get_penguins_for_player(player_color=PlayerColor.BLACK)
        ref._run_movement_turn()
        # Player 4 can't go and is skipped so they have no penguins
        moved_pengs = ref.current_game_state.get_penguins_for_player(player_color=PlayerColor.BLACK)
        self.assertEqual(initial_pengs, moved_pengs)
        self.assertEqual(0, ref.current_game_state.get_fish_for_player(player_color=PlayerColor.BLACK))

    def test_run_movement_turn_invalid(self):
        """
        Test running a movement turn where someone makes an invalid move
        """
        ref = self.set_up_game_phases(4, 4, num_players=2, run_placement_phase=True,
                                      bad_player_obj=RefTests.bad_player_invalid_move)
        ref._run_movement_turn()
        # Player 4 is making an invalid move so they are put in cheating category.
        self.assertIsNone(ref.current_game_state.get_fish_for_player(PlayerColor.RED))
        self.assertEqual({KickedPlayerType.CHEATING: [PlayerColor.RED], KickedPlayerType.FAILING: []}, ref.kicked_players)

    def test_run_movement_turn_failing_type(self):
        """
        Test running a movement turn with failing type
        """
        ref = self.set_up_game_phases(4, 4, num_players=2, run_placement_phase=True,
                                      bad_player_obj=RefTests.bad_player_failing_type_movement)

        ref._run_movement_turn()
        # Player 4 is making a move with a bad type so they are put in failing category.
        self.assertIsNone(ref.current_game_state.get_fish_for_player(PlayerColor.RED))
        self.assertEqual({KickedPlayerType.FAILING: [PlayerColor.RED], KickedPlayerType.CHEATING: []}, ref.kicked_players)

    def test_run_movement_turn_failing_error(self):
        """
        Test running a movement turn with internal error on its side.
        """
        # player that makes an invalid move
        ref = self.set_up_game_phases(4, 4, num_players=2, run_placement_phase=True,
                                      bad_player_obj=RefTests.bad_player_exception_movement)

        ref._run_movement_turn()
        # Player 4 can't go and is skipped so they have no penguins
        self.assertIsNone(ref.current_game_state.get_fish_for_player(PlayerColor.RED))
        self.assertEqual({KickedPlayerType.FAILING: [PlayerColor.RED], KickedPlayerType.CHEATING: []}, ref.kicked_players)

    def test_run_placement_round_valid(self):
        """
        Test running a whole placement round with no errors for placement
        """
        ref = self.set_up_game_phases(5, 5)
        ref._run_placement_round()

        # Test a new penguin gets placed each round
        for color in ref.current_game_state.get_player_order():
            self.assertEqual(1, len(ref.current_game_state.get_penguins_for_player(color)))
        ref._run_placement_round()
        for color in ref.current_game_state.get_player_order():
            self.assertEqual(2, len(ref.current_game_state.get_penguins_for_player(color)))

    def test_run_placement_round_invalid(self):
        """
        Test running a whole placement round with errors for placement
        """
        # player that makes an invalid move
        ref = self.set_up_game_phases(5, 5, num_players=4, bad_player_obj=RefTests.bad_player_failing_type_placement)

        ref._run_placement_round()
        # Check that player gets kicked out but other players place penguin
        self.assertEqual(3, len(ref.current_game_state.get_player_order()))
        self.assertEqual(1, len(ref.kicked_players[KickedPlayerType.FAILING]))
        for color in ref.current_game_state.get_player_order():
            self.assertEqual(1, len(ref.current_game_state.get_penguins_for_player(color)))

        # Check that all other players can keep playing
        ref._run_placement_round()
        for color in ref.current_game_state.get_player_order():
            self.assertEqual(2, len(ref.current_game_state.get_penguins_for_player(color)))
        self.assertEqual(3, len(ref.current_game_state.get_player_order()))
        self.assertEqual(1, len(ref.kicked_players[KickedPlayerType.FAILING]))

    def test_run_movement_round_valid(self):
        """
        Test running a whole movement round with no errors for placement
        """
        ref = self.set_up_game_phases(5, 5, run_placement_phase=True)

        penguins_for_red_init = ref.current_game_state.get_penguins_for_player(PlayerColor.RED)
        penguins_for_white_init = ref.current_game_state.get_penguins_for_player(PlayerColor.WHITE)
        ref._run_movement_round()
        penguins_for_red_new = ref.current_game_state.get_penguins_for_player(PlayerColor.RED)
        penguins_for_white_new = ref.current_game_state.get_penguins_for_player(PlayerColor.WHITE)
        # Test new penguins
        self.assertNotEqual(penguins_for_red_init, penguins_for_red_new)
        self.assertNotEqual(penguins_for_white_init, penguins_for_white_new)
        self.assertGreater(ref.current_game_state.get_fish_for_player(PlayerColor.RED), 0)
        self.assertGreater(ref.current_game_state.get_fish_for_player(PlayerColor.WHITE), 0)

    def test_run_movement_round_invalid(self):
        """
        Test running a movement round with an invalid penguin
        """
        ref = self.set_up_game_phases(5, 5, num_players=4, run_placement_phase=True,
                                      bad_player_obj=RefTests.bad_player_invalid_move)

        penguins_for_white_init = ref.current_game_state.get_penguins_for_player(PlayerColor.WHITE)
        ref._run_movement_round()
        penguins_for_white_new = ref.current_game_state.get_penguins_for_player(PlayerColor.WHITE)

        # Test kicking a player from an invalid movement round
        self.assertNotEqual(penguins_for_white_init, penguins_for_white_new)
        self.assertGreater(ref.current_game_state.get_fish_for_player(PlayerColor.WHITE), 0)
        self.assertFalse(PlayerColor.RED in ref.current_game_state.get_player_order())
        self.assertEqual(3, len(ref.current_game_state.get_player_order()))

    def test_run_whole_basic_game(self):
        """
        Test running a whole game and getting a winner
        """
        players = [(BasicPlayer(), 1), (BasicPlayer(), 2)]
        ref = Referee()
        ref.initialize_and_run_game(3, 3, players)
        # In this 3x3 board only one player can move so RED will always win
        self.assertEqual(GamePhase.END_GAME, ref.current_game_state.get_game_phase())
        self.assertEqual([PlayerColor.RED], ref.winners)
        self.assertEqual([], ref.kicked_players[KickedPlayerType.FAILING])
        self.assertEqual([], ref.kicked_players[KickedPlayerType.CHEATING])

    def test_run_whole_basic_game_multiple_winners(self):
        """
        Test running a whole game and getting 2 winners
        """
        players = [(BasicPlayer(), 1), (BasicPlayer(), 2), (BasicPlayer(), 3)]
        ref = Referee()
        ref.initialize_and_run_game(3, 3, players)
        self.assertEqual(GamePhase.END_GAME, ref.current_game_state.get_game_phase())
        self.assertEqual([PlayerColor.RED, PlayerColor.WHITE, PlayerColor.BROWN], ref.winners)
        self.assertEqual([], ref.kicked_players[KickedPlayerType.FAILING])
        self.assertEqual([], ref.kicked_players[KickedPlayerType.CHEATING])

    def test_single_player_left_game(self):
        """
        Tests running a game when only a single player left
        """
        players = [(BasicPlayer(), 1), (RefTests.bad_player_invalid_placement, 2)]
        ref = Referee()
        ref.initialize_and_run_game(3, 3, players)
        self.assertEqual(GamePhase.END_GAME, ref.current_game_state.get_game_phase())
        self.assertEqual([PlayerColor.RED], ref.winners)
        self.assertGreater(ref.current_game_state.get_fish_for_player(PlayerColor.RED), 0)
        self.assertEqual([PlayerColor.WHITE], ref.kicked_players[KickedPlayerType.CHEATING])

    def test_no_players_left_in_game_placement(self):
        """
        Tests running a game with no players left in the game and that it exits out of the game if that happens in placement phase.
        """
        players = [(RefTests.bad_player_invalid_placement, 1), (RefTests.bad_player_invalid_placement, 2)]
        ref = Referee()
        ref.initialize_and_run_game(3, 3, players)
        self.assertEqual(GamePhase.END_GAME, ref.current_game_state.get_game_phase())
        self.assertEqual([], ref.winners)
        self.assertListEqual([PlayerColor.RED, PlayerColor.WHITE], ref.kicked_players[KickedPlayerType.CHEATING])

    def test_no_players_left_in_game_movement(self):
        """
        Tests running a game with no players left in the game and that it exits out of the game in movement phase
        """
        players = [(RefTests.bad_player_invalid_move, 1), (RefTests.bad_player_invalid_move, 2)]
        ref = Referee()
        ref.initialize_and_run_game(3, 3, players)
        self.assertEqual(GamePhase.END_GAME, ref.current_game_state.get_game_phase())
        self.assertEqual([], ref.winners)
        self.assertListEqual([PlayerColor.RED, PlayerColor.WHITE], ref.kicked_players[KickedPlayerType.CHEATING])

    def test_run_larger_game(self):
        """
        Tests running a larger more non-trivial game
        """
        players = [(BasicPlayer(), 1), (BasicPlayer(), 2)]
        ref = Referee()
        ref.initialize_and_run_game(7, 4, players)
        self.assertEqual(GamePhase.END_GAME, ref.current_game_state.get_game_phase())
        self.assertTrue(PlayerColor.RED in ref.winners or PlayerColor.WHITE in ref.winners)
        self.assertGreater(ref.current_game_state.get_fish_for_player(PlayerColor.RED), 0)
        self.assertGreater(ref.current_game_state.get_fish_for_player(PlayerColor.WHITE), 0)


if __name__ == '__main__':
    unittest.main()
