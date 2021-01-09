#!/usr/bin/python3

import sys
sys.path.insert(0, '../')
import unittest
from unittest.mock import MagicMock
from board import FishBoard
from state import FishGameState
from Player.strategy import GenericStrategyComponent
from structures import Coordinate, Action
from structures import Player, GameStatePhase
from Player.player import PlayerComponent
from Admin.referee import Referee


class TestGameStrategy(unittest.TestCase):
    currentResult = None  # holds last result object passed to run method

    @staticmethod
    def setup():
        test_board = FishBoard(4, 3)
        player_1 = Player("red", 0, 0, [])
        player_2 = Player("white", 0, 0, [])
        test_players = [player_1, player_2]

        state = FishGameState(board=test_board, num_players=len(test_players), players=test_players,
                              current_player=player_1, phase=GameStatePhase.INITIAL)

        return state

    @classmethod
    def setResult(cls, amount, errors, failures, skipped):
        cls.amount, cls.errors, cls.failures, cls.skipped = \
            amount, errors, failures, skipped

    def tearDown(self):
        amount = self.currentResult.testsRun
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        skipped = self.currentResult.skipped
        self.setResult(amount, errors, failures, skipped)

    @classmethod
    def tearDownClass(cls):
        print("\ntests run: " + str(cls.amount))
        print("errors: " + str(len(cls.errors)))
        print("failures: " + str(len(cls.failures)))
        print("success: " + str(cls.amount - len(cls.errors) - len(cls.failures)))
        print("skipped: " + str(len(cls.skipped)))

    def run(self, result=None):
        # remember result for use in tearDown
        self.currentResult = result
        # call superclass run method
        unittest.TestCase.run(self, result)

    def test_notify_player_placement(self):
        state = self.setup()
        player_1_component = PlayerComponent()
        player_2_component = PlayerComponent()

        ref = Referee(
            players=[player_1_component, player_2_component],
            num_rows=4, num_cols=3
        )

        ref.notify_player_placement()
        expected_state = state.add_penguin(0, 0, 'red')
        self.assertTrue(ref.state.is_equal(expected_state))

    def test_notify_player_placement_invalid(self):
        state = self.setup()

        expected_placement = Coordinate(row=5, col=5)

        mocked_strategy_player1 = GenericStrategyComponent()
        mocked_strategy_player1.place_penguin = MagicMock(
            return_value=expected_placement
        )

        player_1_component = PlayerComponent(strategy=mocked_strategy_player1)
        player_2_component = PlayerComponent()

        ref = Referee(
            players=[player_1_component, player_2_component],
            num_rows=4, num_cols=3
        )

        expected = state.kick_player(player_to_kick=state.current_player)
        ref.notify_player_placement()
        self.assertTrue(ref.state.is_equal(expected))

    def test_notify_players_movement(self):
        state = self.setup()
        state = state.add_penguin(row=0, col=0, color="red")
        state = state.add_penguin(row=1, col=1, color="white")
        state = state.finalize()

        expected_action = Action(
                start=Coordinate(row=0, col=0),
                end=Coordinate(row=1, col=0),
                player_color="red"
        )

        not_expected_action = Action(
                start=Coordinate(row=1, col=1),
                end=Coordinate(row=2, col=2),
                player_color="white"
        )

        mocked_strategy_player1 = GenericStrategyComponent()
        mocked_strategy_player1.choose_action_from_state = MagicMock(
            return_value=expected_action
        )

        mocked_strategy_player2 = GenericStrategyComponent()
        mocked_strategy_player2.choose_action_from_state = MagicMock(
            return_value=not_expected_action
        )

        player_1_component = PlayerComponent(strategy=mocked_strategy_player1)
        player_2_component = PlayerComponent(strategy=mocked_strategy_player2)

        ref = Referee(
            players=[player_1_component, player_2_component],
            num_rows=4, num_cols=3
        )

        expected = state.move_penguin(color="red",
                                      start_row=expected_action.start.row,
                                      start_col=expected_action.start.col,
                                      end_row=expected_action.end.row,
                                      end_col=expected_action.end.col)

        ref.state = state
        ref.end_penguin_placement()
        ref.notify_players_movement()
        actual = ref.state
        self.assertTrue(actual.is_equal(expected))


    def test_notify_player_placement_invalid_movement(self):
        state = self.setup()
        state = state.add_penguin(row=0, col=0, color="red")
        state = state.add_penguin(row=1, col=1, color="white")
        state = state.finalize()

        expected_action = Action(
                start=Coordinate(row=0, col=0),
                end=Coordinate(row=3, col=2),
                player_color="red"
        )

        not_expected_action = Action(
                start=Coordinate(row=1, col=1),
                end=Coordinate(row=2, col=2),
                player_color="white"
        )

        mocked_strategy_player1 = GenericStrategyComponent()
        mocked_strategy_player1.choose_action_from_state = MagicMock(
            return_value=expected_action
        )

        mocked_strategy_player2 = GenericStrategyComponent()
        mocked_strategy_player2.choose_action_from_state = MagicMock(
            return_value=not_expected_action
        )

        player_1_component = PlayerComponent(strategy=mocked_strategy_player1)
        player_2_component = PlayerComponent(strategy=mocked_strategy_player2)

        ref = Referee(
            players=[player_1_component, player_2_component],
            num_rows=4, num_cols=3
        )
        expected = state.kick_player(player_to_kick=state.current_player)
        ref.state = state

        ref.end_penguin_placement()
        ref.notify_players_movement()
        actual = ref.state
        self.assertTrue(actual.is_equal(expected))

    def test_notify_player_kicked(self):
        player_1_component = PlayerComponent()
        player_2_component = PlayerComponent()

        player_1_component.notify_kicked = MagicMock()

        ref = Referee(
            players=[player_1_component, player_2_component],
            num_rows=4, num_cols=3
        )

        ref.notify_player_kicked(player=player_1_component)
        player_1_component.notify_kicked.assert_called_once_with()

    def test_notify_winners(self):
        player_1_component = PlayerComponent()
        player_2_component = PlayerComponent()

        player_1_component.notify_winner = MagicMock()
        player_2_component.notify_winner = MagicMock()

        ref = Referee(
            players=[player_1_component, player_2_component],
            num_rows=4, num_cols=3
        )
        ref.notify_winners()
        player_1_component.notify_winner.assert_called_once_with()
        player_2_component.notify_winner.assert_called_once_with()


    def test_end_game(self):
        state = self.setup()
        state = state.finalize()
        state.end_game()

        player_1_component = PlayerComponent()
        player_2_component = PlayerComponent()

        player_1_component.notify_game_over = MagicMock()
        player_2_component.notify_game_over = MagicMock()

        ref = Referee(
            players=[player_1_component, player_2_component],
            num_rows=4, num_cols=3
        )

        ref.end_game()
        player_1_component.notify_game_over.assert_called_once_with()
        player_2_component.notify_game_over.assert_called_once_with()

        self.assertTrue(state.is_equal(ref.state))


