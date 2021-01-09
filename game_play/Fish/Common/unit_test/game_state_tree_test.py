#!/usr/bin/python3

import unittest
from board import FishBoard
from state import FishGameState
from structures import Tile
from structures import Coordinate
from typing import Callable
from game_tree import *


class TestBoard(unittest.TestCase):

    @staticmethod
    def setup():
        test_board = FishBoard(4, 3)
        player_1 = Player("red", 0, 0, [])
        player_2 = Player("white", 0, 0, [])
        test_players = [player_1, player_2]
        factory = FishGameState(board=test_board, players=test_players, phase=GameStatePhase.INITIAL,
                                num_players=len(test_players), current_player=test_players[0])
        factory = factory.add_penguin(0, 0, "red")
        factory = factory.add_penguin(0, 2, "white")
        factory = factory.add_penguin(1, 0, "red")
        factory = factory.add_penguin(1, 2, "white")
        factory = factory.add_penguin(2, 0, "red")
        factory = factory.add_penguin(2, 2, "white")
        factory = factory.add_penguin(3, 0, "red")
        factory = factory.add_penguin(3, 2, "white")
        return factory.finalize(), factory.board, factory.players

    currentResult = None  # holds last result object passed to run method

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

    def test_get_next_nodes_one_step(self):
        state, *_ = self.setup()

        tree = GameStateTree(state, previous_action=None)
        first_children = tree.get_children()
        expected_moves = tree.state.get_player_actions_from(tree.state.current_player)
        i = 0
        while first_children:
            try:
                child = next(first_children)
                self.assertEqual(expected_moves[i], child.previous_action)
                i += 1
            except StopIteration:
                break

    def test_take_action(self):
        state, *_ = self.setup()
        tree = GameStateTree(state)

        first_children = tree.get_children()
        next_node = next(first_children)
        move = next_node.previous_action
        result_state = tree.take_action(move)
        for player1, player2 in zip(next_node.state.players.values(), result_state.players.values()):
            self.assertEqual(player1, player2)
        for row1, row2 in zip(next_node.state.board.board, result_state.board.board):
            for tile1, tile2 in zip(row1, row2):
                self.assertEqual(tile1, tile2)
        self.assertEqual(result_state.current_player, next_node.state.current_player)

    def test_take_action_failure(self):
        state, *_ = self.setup()

        tree = GameStateTree(state)
        self.assertEqual(tree.take_action(Action(start=Coordinate(0, 1), end=Coordinate(2, 2), player_color="red")),
                         "Player color red does not own penguin at row 0, col 1")
    
    def test_get_children(self):
        state, test_board, test_players = self.setup()
        tree = GameStateTree(state)

        actions = state.get_player_actions_from(player=test_players['red'])
        expected = [state.move_penguin(
            color=test_players['red'].color,
            start_row=action.start.row,
            start_col=action.start.col,
            end_row=action.end.row,
            end_col=action.end.col
        ) for action in actions]

        actual = [child.state for child in tree.get_children()]

        for idx, expected_state in enumerate(expected):
            self.assertTrue(expected_state.is_equal(actual[idx]))

    def test_apply_fn(self):
        state, test_board, test_players = self.setup()
        tree = GameStateTree(state)

        # Simple Policy : Just return the number of actions I can take.
        def simply_policy(s: FishGameState) -> int:
            return len(s.get_player_actions_from(s.current_player))

        # Descendents structure is as pre-order traversal, meaning
        # the left most state is first.
        expected = [
            len(descendant.state.get_player_actions_from(descendant.state.current_player))
            for descendant in tree.descendants
        ]

        # Current state is not a descendent
        expected += [simply_policy(state)]

        # Apply_fn traverses the tree pre-order also, meaning actual and expected should match.
        actual = tree.apply_fn(policy=simply_policy)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
