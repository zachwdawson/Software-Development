import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


import unittest
from Fish.Common.representations.fish_avatar import FishAvatar
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor


class FishAvatarTest(unittest.TestCase):

    def test_bad_color(self):
        """
        Purpose: Tests passing a bad color to the Fish avatar initialization
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            FishAvatar('fakecolor')

    def test_good_color(self):
        """
        Purpose: Tests passing a color in the enumeration to the Fish avatar initialization
        Signature: Void -> Void
        """
        avatar = FishAvatar(PlayerColor.RED)
        self.assertEqual(PlayerColor.RED, avatar.color)


if __name__ == '__main__':
    unittest.main()
