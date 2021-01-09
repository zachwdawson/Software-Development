import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


import unittest
from Fish.Common.representations.fish_board import FishBoardModel
from Fish.Common.representations.fish_tile import FishTile


class FishBoardModelTest(unittest.TestCase):

    def test_invalid_row_col(self):
        """
        Purpose: Test passing in invalid values for constructing a board with a row or column
        Signature: Void -> Void
        """
        with self.assertRaises(TypeError):
            FishBoardModel("string", 1)
        with self.assertRaises(ValueError):
            FishBoardModel(-1, 1)

    def test_valid_row_col(self):
        """
        Purpose: Test passing in valid values for constructing a board
        Signature: Void -> Void
        """
        model = FishBoardModel(4, 3)
        self.assertEqual((4, 3), model.get_dimensions())

    def test_invalid_holes(self):
        """
        Purpose: Test passing in holes that are not on the board for creation with holes function
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishBoardModel.create_with_holes(4, 3, {(6, 0)}, 1)
        with self.assertRaises(ValueError):
            FishBoardModel.create_with_holes(4, 3, {(-1, -1)}, 1)

    def test_invalid_one_fish(self):
        """
        Purpose: Test passing in less than 0 minimum one fish tiles throws an exception
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishBoardModel.create_with_holes(4, 3, {}, -1)

    def test_valid_holes(self):
        """
        Purpose: Test creating holes in valid places
        Signature: Void -> Void
        """
        model = FishBoardModel.create_with_holes(4, 3, {(0, 0)}, 1)
        self.assertIsNone(model.get_tile_at_coord(0, 0))
        amount_one_fish = 0
        for x, y in model.get_tile_coords():
            tile = model.get_tile_at_coord(x, y)
            if tile and tile.num_fish == 1:
                amount_one_fish += 1
        self.assertGreaterEqual(amount_one_fish, 1)

    def test_invalid_not_enough_tiles(self):
        """
        Purpose:Test that error is thrown when you don't have enough tiles available to satisfy the minimum
        1-tiles requirement
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishBoardModel.create_with_holes(1, 1, {}, 2)
        with self.assertRaises(ValueError):
            FishBoardModel.create_with_holes(1, 1, {(0, 0)}, 1)

    def test_invalid_fish_num_same_no_holes(self):
        """
        Purpose: Test that if you pass in invalid value for amount of fish tiles you get an error
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishBoardModel.create_with_same_fish_amount(4, 3, 0)
        with self.assertRaises(ValueError):
            FishBoardModel.create_with_same_fish_amount(4, 3, FishTile.MAX_AMOUNT_FISH + 1)

    def test_valid_same_no_holes(self):
        """
        Purpose: Test creating a valid board with no holes returns a board with no holes
        Signature: Void -> Void
        """
        model = FishBoardModel.create_with_same_fish_amount(4, 3, 1)
        for x, y in model.get_tile_coords():
            tile = model.get_tile_at_coord(x, y)
            self.assertEqual(1, tile.num_fish)

    def test_reachable_pos_basic(self):
        """
        Purpose: Test creating reachable positions returns the right positions in a basic example
        Signature: Void -> Void
        """
        model = FishBoardModel.create_with_same_fish_amount(4, 2, 2)
        positions = model.find_straight_line_positions(1, 1)
        test_dict = {'SOUTHEAST': [(2, 2), (3, 3)],
                     'NORTHEAST': [(2, 0)],
                     'NORTH': [],
                     'NORTHWEST': [(0, 0)],
                     'SOUTHWEST': [(0, 2)],
                     'SOUTH': [(1, 3)]}
        self.assertDictEqual(test_dict, positions)

    def test_reachable_pos_missing(self):
        """
        Purpose: Tests that positions are not reachable that were previously reachable if you remove tiles
        Signature: Void -> Void
        """
        model = FishBoardModel.create_with_holes(4, 2, {(0, 0), (0, 2), (2, 2)}, 1)
        positions = model.find_straight_line_positions(1, 1)
        test_dict = {'SOUTHEAST': [],
                     'NORTHEAST': [(2, 0)],
                     'NORTH': [],
                     'NORTHWEST': [],
                     'SOUTHWEST': [],
                     'SOUTH': [(1, 3)]}
        self.assertDictEqual(test_dict, positions)

    def test_invalid_reachable_pos(self):
        """
        Purpose: Test trying to find reachable tiles from a position off the board
        Signature: Void -> Void
        """
        model = FishBoardModel.create_with_same_fish_amount(4, 3, 2)
        with self.assertRaises(ValueError):
            model.find_straight_line_positions(10, 0)

    def test_remove_tile_valid(self):
        """
        Purpose: Test removing tiles in a valid way and getting the tile return and seeing that there is no tile there
        Signature: Void -> Void
        """
        model = FishBoardModel.create_with_same_fish_amount(4, 3, 2)
        tile = model.remove_tile(0, 0)
        self.assertEqual(2, tile.num_fish)
        self.assertIsNone(model.get_tile_at_coord(0, 0))

    def test_remove_bad_coords(self):
        """
        Purpose: Test trying to remove tile from a bad coordinate and getting an error with that
        Signature: Void -> Void
        """
        model = FishBoardModel.create_with_same_fish_amount(4, 3, 2)
        with self.assertRaises(ValueError):
            model.remove_tile(-1, -1)
        with self.assertRaises(ValueError):
            model.remove_tile(10, 0)

    def test_remove_no_tile(self):
        """
        Purpose: Test removing a tile from a position that was already tile-less and getting None back
        Signature: Void -> Void
        """
        model = FishBoardModel.create_with_same_fish_amount(4, 3, 2)
        tile = model.remove_tile(0, 0)
        self.assertEqual(2, tile.num_fish)
        self.assertIsNone(model.get_tile_at_coord(0, 0))
        self.assertIsNone(model.remove_tile(0, 0))

    def test_sort_iterator(self):
        """
        Purpose: Test sorting a board's valid coordinates by the y value and then the x value
        Signature: Void -> Void
        """
        model = FishBoardModel.create_with_same_fish_amount(4, 3, 2)
        sorted_coord = model.get_coords_sorted_by_row()

if __name__ == '__main__':
    unittest.main()
