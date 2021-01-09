import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import unittest
from Fish.Common.representations.fish_tile import FishTile


class TileTest(unittest.TestCase):

    def test_not_int_tile(self):
        """
        Purpose: Test what happens when you try and create a tile with a value other than an integer
        Signature: Void -> Void
        """
        with self.assertRaises(TypeError):
            FishTile("string")
        with self.assertRaises(TypeError):
            FishTile(1.2)

    def test_zero_or_less_fish_tile(self):
        """
        Purpose: Test what happens when you try and create a tile with 0 or less fish
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishTile(-1)
        with self.assertRaises(ValueError):
            FishTile(0)

    def test_too_many_fish_tile(self):
        """
        Purpose: Test what happens when you try and create a tile with more than max amount of fish
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishTile(FishTile.MAX_AMOUNT_FISH + 1)

    def test_normal_fish_tile(self):
        """
        Purpose: Test what happens when you create a tile with an allowed amount of fish
        Signature: Void -> Void
        """
        tile = FishTile(1)
        self.assertEqual(1, tile.num_fish)

    def test_default_fish_tile(self):
        """
        Purpose: Test what happens when you create a tile with the default (MAX) amount of fish
        Signature: Void -> Void
        """
        tile = FishTile()
        self.assertEqual(FishTile.MAX_AMOUNT_FISH, tile.num_fish)


if __name__ == '__main__':
    unittest.main()
