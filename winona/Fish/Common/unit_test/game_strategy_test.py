#!/usr/bin/python3

import sys
sys.path.insert(0, '../')
import unittest
from unittest.mock import MagicMock
from board import FishBoard
from state import FishGameState
from game_tree import GameStateTree
from Player.strategy import GenericStrategyComponent
from structures import Coordinate, Action
from structures import Player, GameStatePhase


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
        state = state.add_penguin(0, 0, "red") \
            .add_penguin(0, 2, "white") \
            .add_penguin(0, 1, "red") \
            .add_penguin(1, 2, "white") \
            .add_penguin(2, 0, "red") \
            .add_penguin(2, 2, "white") \
            .add_penguin(3, 0, "red") \
            .add_penguin(3, 2, "white")

        return state.finalize(), state.board, state.players

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
        self.currentResult = result  # remember result for use in tearDown
        unittest.TestCase.run(self, result)  # call superclass run method

    def test_create_choose_action_base_case_0_turns(self):
        """
        If the player has 0 turns and it is the currents player turn,
        then the previous action is return.
        """
        state, *_ = self.setup()
        production_tree = GameStateTree(state, previous_action=None)
        production_tree.get_children = MagicMock(return_value=None)
        expected = Action(
            player_color=production_tree.state.current_player.color,
            start=Coordinate(0, 0),
            end=Coordinate(1, 0)
        )

        production_tree.previous_action = expected
        actual = GenericStrategyComponent.choose_action(tree=production_tree, num_turns=0)
        self.assertEqual(expected, actual)

    def test_create_choose_action_base_case_no_children_for_maximizing_player(self):
        """
        If the player has turns > 0 but has no children - end-game - then
        return the current's player's previous action
        """
        state, *_ = self.setup()
        production_tree = GameStateTree(state, previous_action=None)
        expected = Action(
            player_color=production_tree.state.current_player.color,
            start=Coordinate(0, 0),
            end=Coordinate(1, 0)
        )

        production_tree.previous_action = expected
        actual = GenericStrategyComponent.choose_action(tree=production_tree, num_turns=2)
        self.assertEqual(expected, actual)

    def test_create_choose_action_base_case_no_children_for_non_maximizing_player(self):
        """
        If the player has turns > 0 but has no children - end-game - and this is not
        the maximizing player, then we return None.
        """
        state, *_ = self.setup()
        production_tree = GameStateTree(state, previous_action=None)
        production_tree.get_children = MagicMock(return_value=[])
        production_tree.previous_action = Action(
            player_color=production_tree.state.current_player.color,
            start=Coordinate(0, 0),
            end=Coordinate(1, 0)
        )

        expected = None
        _, actual = GenericStrategyComponent.minimax(tree=production_tree, num_rounds=2, maximizing_player=Player("white", 0, 0, []))
        self.assertEqual(expected, actual)

    def test_create_choose_action_recursive_case_is_maximizing_once(self):
        """
        In a scenario where all the children of the maximizing player
        are leaves - aka end-games - than a tie-breaker decides which
        action to take.
        """
        state, *_ = self.setup()
        production_tree = GameStateTree(state, previous_action=None)
        expected = Action(
            player_color=production_tree.state.current_player.color,
            start=Coordinate(0, 0),
            end=Coordinate(1, 0)
        )

        children = [child for child in production_tree.get_children()]
        for idx, child in enumerate(children):
            if idx == 1:
                child.previous_action = expected

            child.get_children = MagicMock(return_value=[])

        production_tree.get_children = MagicMock(return_value=children)
        actual = GenericStrategyComponent.choose_action(tree=production_tree, num_turns=2)
        self.assertEqual(expected, actual)

    def test_create_choose_action_recursive_case_is_maximizing_twice(self):
        """
        In a recursive case where 1 round is played and the
        all leave nodes are the maximizing players, the minimum of
        these leave nodes is return.
        """
        state, *_ = self.setup()
        production_tree = GameStateTree(state, previous_action=None)
        expected = Action(
            player_color=production_tree.state.current_player.color,
            start=Coordinate(0, 0),
            end=Coordinate(1, 0)
        )

        children = [child for child in production_tree.get_children()]
        for idx, child in enumerate(children):
            second_players_children = [second_players_child for second_players_child in child.get_children()]
            for jdx, second_players_child in enumerate(second_players_children):
                if jdx == 1 and idx == 1:
                    score = 0
                    child.previous_action = expected
                else:
                    score = 10
                modified_player = Player.from_dict(
                    {
                        **second_players_child.state.current_player._asdict(),
                        **{'score': score}
                    }
                )
                second_players_child.state.current_player = modified_player
                second_players_child.get_children = MagicMock(return_value=[])
                second_players_child.state.check_any_player_can_move = MagicMock(return_value=False)

        production_tree.get_children = MagicMock(return_value=children)
        actual = GenericStrategyComponent.choose_action(tree=production_tree, num_turns=2)
        self.assertEqual(expected, actual)

