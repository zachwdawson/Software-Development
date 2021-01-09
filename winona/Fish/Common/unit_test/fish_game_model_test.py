#!/usr/bin/python3

import unittest
from board import FishBoard
from structures import Tile
from structures import Coordinate


class TestBoard(unittest.TestCase):
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

    def test_create_board(self):
        model = FishBoard(num_rows=4, num_cols=3)
        expected_board = [
            [
                Tile(coordinate=Coordinate(row=0, col=0), is_tile=True, num_fish=0, top_coordinate=None, top_left_coordinate=None, top_right_coordinate=None, bottom_coordinate=(2, 0), bottom_left_coordinate=None, bottom_right_coordinate=(1, 0)),
                Tile(coordinate=Coordinate(row=0, col=1), is_tile=True, num_fish=0, top_coordinate=None, top_left_coordinate=None, top_right_coordinate=None, bottom_coordinate=(2, 1), bottom_left_coordinate=(1, 0), bottom_right_coordinate=(1, 1)),
                Tile(coordinate=Coordinate(row=0, col=2), is_tile=True, num_fish=0, top_coordinate=None, top_left_coordinate=None, top_right_coordinate=None, bottom_coordinate=(2, 2), bottom_left_coordinate=(1, 1), bottom_right_coordinate=(1, 2))],
            [
                Tile(coordinate=Coordinate(row=1, col=0), is_tile=True, num_fish=0, top_coordinate=None, top_left_coordinate=(0, 0), top_right_coordinate=(0, 1), bottom_coordinate=(3, 0), bottom_left_coordinate=(2, 0), bottom_right_coordinate=(2, 1)),
                Tile(coordinate=Coordinate(row=1, col=1), is_tile=True, num_fish=0, top_coordinate=None, top_left_coordinate=(0, 1), top_right_coordinate=(0, 2), bottom_coordinate=(3, 1), bottom_left_coordinate=(2, 1), bottom_right_coordinate=(2, 2)),
                Tile(coordinate=Coordinate(row=1, col=2), is_tile=True, num_fish=0, top_coordinate=None, top_left_coordinate=(0, 2), top_right_coordinate=None, bottom_coordinate=(3, 2), bottom_left_coordinate=(2, 2), bottom_right_coordinate=None)],
            [
                Tile(coordinate=Coordinate(row=2, col=0), is_tile=True, num_fish=0, top_coordinate=(0, 0), top_left_coordinate=None, top_right_coordinate=(1, 0), bottom_coordinate=None, bottom_left_coordinate=None, bottom_right_coordinate=(3, 0)),
                Tile(coordinate=Coordinate(row=2, col=1), is_tile=True, num_fish=0, top_coordinate=(0, 1), top_left_coordinate=(1, 0), top_right_coordinate=(1, 1), bottom_coordinate=None, bottom_left_coordinate=(3, 0), bottom_right_coordinate=(3, 1)),
                Tile(coordinate=Coordinate(row=2, col=2), is_tile=True, num_fish=0, top_coordinate=(0, 2), top_left_coordinate=(1, 1), top_right_coordinate=(1, 2), bottom_coordinate=None, bottom_left_coordinate=(3, 1), bottom_right_coordinate=(3, 2))],
            [
                Tile(coordinate=Coordinate(row=3, col=0), is_tile=True, num_fish=0, top_coordinate=(1, 0), top_left_coordinate=(2, 0), top_right_coordinate=(2, 1), bottom_coordinate=None, bottom_left_coordinate=None, bottom_right_coordinate=None),
                Tile(coordinate=Coordinate(row=3, col=1), is_tile=True, num_fish=0, top_coordinate=(1, 1), top_left_coordinate=(2, 1), top_right_coordinate=(2, 2), bottom_coordinate=None, bottom_left_coordinate=None, bottom_right_coordinate=None),
                Tile(coordinate=Coordinate(row=3, col=2), is_tile=True, num_fish=0, top_coordinate=(1, 2), top_left_coordinate=(2, 2), top_right_coordinate=None, bottom_coordinate=None, bottom_left_coordinate=None, bottom_right_coordinate=None)
            ]
        ]
        self.assertEqual(model.num_rows, 4)
        self.assertEqual(model.num_cols, 3)
        self.assertEqual(model.board, expected_board)

    def test_retrieve_num_fish(self):
        model = FishBoard(num_rows=4, num_cols=3)
        self.assertEqual(model.board[0][0].num_fish, 0)
        model = model.add_fish(0,0)
        model = model.add_fish(0,0)
        model = model.add_fish(0,0)
        self.assertEqual(model.board[0][0].num_fish, 3)

    def test_is_tile_true(self):
        model = FishBoard(num_rows=4, num_cols=3)
        self.assertTrue(model.board[0][0].is_tile)

    def test_is_tile_false(self):
        model = FishBoard(num_rows=4, num_cols=3)
        model = model.create_hole(0,0)
        self.assertFalse(model.board[0][0].is_tile)

    def test_get_reachable_tiles(self):
        model = FishBoard(num_rows=5, num_cols=4)
        expected_reachable = [Coordinate(row=0, col=1),
                             Coordinate(row=1, col=1),
                             Coordinate(row=0, col=2),
                             Coordinate(row=3, col=1),
                             Coordinate(row=4, col=2),
                             Coordinate(row=4, col=1),
                             Coordinate(row=3, col=0),
                             Coordinate(row=4, col=0),
                             Coordinate(row=1, col=0),
                             Coordinate(row=0, col=0)]
        self.assertEqual(model.get_reachable_tiles(2, 1), expected_reachable)

    def test_get_reachable_tiles_with_holes(self):
        model = FishBoard(num_rows=5, num_cols=4)
        model = model.create_hole(3, 1)
        expected_reachable = [Coordinate(row=0, col=1),
                             Coordinate(row=1, col=1),
                             Coordinate(row=0, col=2),
                             Coordinate(row=4, col=1),
                             Coordinate(row=3, col=0),
                             Coordinate(row=4, col=0),
                             Coordinate(row=1, col=0),
                             Coordinate(row=0, col=0)]
        self.assertEqual(model.get_reachable_tiles(2, 1), expected_reachable)

    def test_create_hole(self):
        model = FishBoard(num_rows=4, num_cols=3)
        self.assertTrue(model.board[0][0].is_tile)
        model = model.create_hole(0,0)
        self.assertFalse(model.board[0][0].is_tile)

    def test_add_fish(self):
        model = FishBoard(num_rows=4, num_cols=3)
        self.assertEqual(model.board[0][0].num_fish, 0)
        model = model.add_fish(0,0)
        self.assertEqual(model.board[0][0].num_fish, 1)

    def test_max_fish(self):
        model = FishBoard(num_rows=4, num_cols=3)
        self.assertEqual(model.board[0][0].num_fish, 0)
        model = model.add_fish(0,0)
        model = model.add_fish(0,0)
        model = model.add_fish(0,0)
        model = model.add_fish(0,0)
        model = model.add_fish(0,0)
        self.assertEqual(model.board[0][0].num_fish, 5)
        with self.assertRaises(ValueError):
            model = model.add_fish(0, 0)

    def test_valid_row_and_col_true(self):
        model = FishBoard(num_rows=4, num_cols=3)
        self.assertTrue(model.valid_row_and_col(1,2))

    def test_valid_row_and_col_false(self):
        model = FishBoard(num_rows=4, num_cols=3)
        self.assertFalse(model.valid_row_and_col(4,5))


    def test_get_reachable_tile_coordinates_by_direction(self):
        model = FishBoard(num_rows=4, num_cols=3)
        tile = model.board[1][2]
        direction = 'bottom_left_coordinate'
        expected = [Coordinate(row=2, col=2), Coordinate(row=3, col=1)]
        self.assertEqual(model.get_reachable_tile_coordinates_by_direction(tile, direction), expected)

    def test_get_reachable_tile_coordinates_by_direction_empty(self):
        model = FishBoard(num_rows=4, num_cols=3)
        tile = model.board[1][2]
        direction = 'top_right_coordinate'
        expected = []
        self.assertEqual(model.get_reachable_tile_coordinates_by_direction(tile, direction), expected)

    def test_is_equal(self):
        board1 = FishBoard(num_rows=4, num_cols=3)
        board2 = FishBoard(num_rows=4, num_cols=3)

        board1 = board1.add_fish(row=0, col=0)
        board2 = board2.add_fish(row=0, col=0)

        board1 = board1.create_hole(row=1, col=0)
        board2 = board2.create_hole(row=1, col=0)

        self.assertTrue(board1.is_equal(board2))

    def test_is_equal_false_different_size(self):
        board1 = FishBoard(num_rows=4, num_cols=3)
        board2 = FishBoard(num_rows=5, num_cols=3)

        self.assertFalse(board1.is_equal(board2))

    def test_is_equal_false_different_num_fish(self):
        board1 = FishBoard(num_rows=4, num_cols=3)
        board2 = FishBoard(num_rows=4, num_cols=3)

        board1 = board1.add_fish(row=0, col=0)
        board2 = board2.add_fish(row=1, col=0)

        self.assertFalse(board1.is_equal(board2))

    def test_is_equal_false_different_holes(self):
        board1 = FishBoard(num_rows=4, num_cols=3)
        board2 = FishBoard(num_rows=4, num_cols=3)

        board1 = board1.create_hole(row=1, col=0)
        board2 = board2.create_hole(row=1, col=1)

        self.assertFalse(board1.is_equal(board2))


if __name__ == '__main__':
    unittest.main()
