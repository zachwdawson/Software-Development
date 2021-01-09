#!/usr/bin/python3

import unittest
from board import FishBoard
from state import FishGameState
from structures import Coordinate, GameStatePhase
from structures import Player


class TestGameState(unittest.TestCase):
    currentResult = None  # holds last result object passed to run method
    player_1 = Player("red", 0, 0, [])
    player_2 = Player("white", 0, 0, [])
    player_3 = Player("brown", 0, 0, [])
    player_list = [player_1, player_2, player_3]

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

    def test_create_game_state(self):
        board = FishBoard(4, 3)
        game_state = FishGameState(board, 3, TestGameState.player_list,
                                   current_player=TestGameState.player_list[0], phase=GameStatePhase.INITIAL)
        expected_players = {
            "red": Player(color="red", age=0, score=0, penguins=[]),
            "white": Player(color="white", age=0, score=0, penguins=[]),
            "brown": Player(color="brown", age=0, score=0, penguins=[])
        }
        self.assertEqual(game_state.players, expected_players)
        self.assertEqual(game_state.board, board)
        self.assertEqual(game_state.num_players, 3)
        self.assertEqual(game_state.num_penguins, 3)

    def test_validate_input_true(self):
        board = FishBoard(4, 3)
        game_state = FishGameState(board, 3, TestGameState.player_list,
                                   current_player=TestGameState.player_list[0], phase=GameStatePhase.FINAL)
        is_valid, error_msg = game_state.validate_input("red", 0, 0)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

    def test_validate_input_invalid_player_id(self):
        board = FishBoard(4, 3)
        game_state = FishGameState(board, 3, TestGameState.player_list,
                                   current_player=TestGameState.player_list[0], phase=GameStatePhase.FINAL)
        is_valid, error_msg = game_state.validate_input(-1, 0, 0)
        self.assertFalse(is_valid)
        self.assertEqual(error_msg, "Player color does not exist")

    def test_validate_input_invalid_player_id_upperbound(self):
        board = FishBoard(4, 3)
        game_state = FishGameState(board, 3, TestGameState.player_list,
                                   current_player=TestGameState.player_list[0], phase=GameStatePhase.FINAL)
        is_valid, error_msg = game_state.validate_input("", 0, 0)
        self.assertFalse(is_valid)
        self.assertEqual(error_msg, "Player color does not exist")

    def test_validate_input_invalid_row_and_col_out_of_bounds(self):
        board = FishBoard(4, 3)
        game_state = FishGameState(board, 3, TestGameState.player_list,
                                   current_player=TestGameState.player_list[0], phase=GameStatePhase.FINAL)
        is_valid, error_msg = game_state.validate_input("red", 6, 6)
        self.assertFalse(is_valid)
        self.assertEqual(error_msg, "Row and column do not exist in this board")

    def test_validate_input_invalid_row_and_col_has_hole(self):
        board = FishBoard(4, 3)
        board = board.create_hole(1, 1)
        game_state = FishGameState(board, 3, TestGameState.player_list,
                                   current_player=TestGameState.player_list[0], phase=GameStatePhase.FINAL)
        is_valid, error_msg = game_state.validate_input("red", 1, 1)
        self.assertFalse(is_valid)
        self.assertEqual(error_msg, "Row and column is a hole")

    def test_validate_input_invalid_row_and_col_has_penguin(self):
        board = FishBoard(4, 3)
        factory = FishGameState(board=board, num_players= 2, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory = factory.add_penguin(2, 2, "red")
        is_valid, error_msg = factory.validate_input("white", 2, 2)
        self.assertFalse(is_valid)
        self.assertEqual(error_msg, "This tile already has a penguin")

    def test_add_penguin_success(self):
        board = FishBoard(4, 3)
        factory = FishGameState(board=board, num_players= 2, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory = factory.add_penguin(0, 0, "red")
        expected_penguins = [Coordinate(0, 0)]
        self.assertEqual(factory.players["red"].penguins, expected_penguins)

    def test_add_penguin_failure(self):
        board = FishBoard(4, 3)
        factory = FishGameState(board=board, num_players= 2, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory = factory.add_penguin(0, 0, "red")
        factory = factory.add_penguin(0, 1, "white")
        with self.assertRaises(ValueError):
            factory = factory.add_penguin(0, 2, "white")

    def test_move_penguin(self):
        board = FishBoard(4, 3)
        factory = FishGameState(board=board, num_players=3, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory = factory.add_penguin(row=0, col=1, color="red")
        factory = factory.add_penguin(row=0, col=0, color="white")
        factory = factory.add_penguin(row=3, col=0, color="brown")

        game_state = factory.finalize()
        game_state = game_state.move_penguin("red", 0, 1, 2, 1)
        expected_penguins = [Coordinate(row=2, col=1)]
        self.assertEqual(game_state.players["red"].penguins, expected_penguins)

    def test_move_penguin_failure(self):
        board = FishBoard(4, 3)
        factory = FishGameState(board=board, num_players=3, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory = factory.add_penguin(row=0, col=0, color="red")
        factory = factory.add_penguin(row=0, col=1, color="white")
        factory = factory.add_penguin(row=0, col=2, color="brown")
        game_state = factory.finalize()
        with self.assertRaises(ValueError):
            game_state.move_penguin("red", 0, 0, 0, 2)

    def test_has_penguin(self):
        board = FishBoard(4, 3)
        factory = FishGameState(board=board, num_players=3, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory = factory.add_penguin(0, 0, "red")
        self.assertTrue(factory.has_penguin(0, 0))
        self.assertFalse(factory.has_penguin(1, 1))

    def test_any_player_can_move_success(self):
        board = FishBoard(4, 3)
        factory = FishGameState(board=board, num_players=3, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory = factory.add_penguin(0, 0, "red")
        factory = factory.add_penguin(1, 1, "white")
        game_state = factory.finalize()
        self.assertTrue(game_state.check_any_player_can_move())

    def test_any_player_can_move_failure(self):
        board = FishBoard(4, 3)
        board = board.create_hole(2, 0)
        board = board.create_hole(3, 0)
        board = board.create_hole(2, 1)
        board = board.create_hole(0, 1)
        factory = FishGameState(board=board, num_players=3, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory = factory.add_penguin(0, 0, "red")
        factory = factory.add_penguin(1, 0, "white")
        game_state = factory.finalize()
        self.assertFalse(game_state.check_any_player_can_move())

    def test_get_player_id_success(self):
        board = FishBoard(4, 3)
        board = board.create_hole(2, 0)
        board = board.create_hole(3, 0)
        board = board.create_hole(2, 1)
        board = board.create_hole(0, 1)
        factory = FishGameState(board=board, num_players=3, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory = factory.add_penguin(0, 0, "red")
        factory = factory.add_penguin(1, 0, "white")

        game_state = factory.finalize()
        self.assertEqual(game_state.get_player_color(0, 0), "red")
        self.assertEqual(game_state.get_player_color(3, 2), "")

    def test_is_equal(self):
        board1 = FishBoard(4, 3)
        board1 = board1.create_hole(2, 0)
        board1 = board1.create_hole(3, 0)
        board1 = board1.create_hole(2, 1)
        board1 = board1.create_hole(0, 1)

        board2 = FishBoard(4, 3)
        board2 = board2.create_hole(2, 0)
        board2 = board2.create_hole(3, 0)
        board2 = board2.create_hole(2, 1)
        board2 = board2.create_hole(0, 1)

        factory1 = FishGameState(board=board1, num_players=3, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory1 = factory1.add_penguin(0, 0, "red")
        factory1 = factory1.add_penguin(1, 0, "white")

        factory2 = FishGameState(board=board2, num_players=3, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        factory2 = factory2.add_penguin(0, 0, "red")
        factory2 = factory2.add_penguin(1, 0, "white")

        state1 = factory1.finalize()
        state2 = factory2.finalize()

        self.assertTrue(state1.is_equal(state2))

    def test_is_equal_false_players_only(self):
        board1 = FishBoard(4, 3)
        board2 = FishBoard(4, 3)

        state1 = FishGameState(board=board1, num_players=3, players=TestGameState.player_list[0:2],
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        state2 = FishGameState(board=board2, num_players=3, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])

        self.assertFalse(state1.is_equal(state2))

    def test_is_equal_false_board_only(self):
        board1 = FishBoard(5, 3)
        board2 = FishBoard(4, 3)

        state1 = FishGameState(board=board1, num_players=3, players=TestGameState.player_list[0:2],
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])
        state2 = FishGameState(board=board2, num_players=3, players=TestGameState.player_list,
                                phase=GameStatePhase.INITIAL, current_player=TestGameState.player_list[0])

        self.assertFalse(state1.is_equal(state2))



if __name__ == '__main__':
    unittest.main()
