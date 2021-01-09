import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import unittest
from Fish.Common.representations.game_state import PlayerInfo, PlayerColor

class InfoTest(unittest.TestCase):

    def test_normal_player_info(self):
        """
        Purpose: Test what happens when you initialize the player info with a valid age, color, and number of penguins placeable
        Signature: Void -> Void
        """
        player_info = PlayerInfo(PlayerColor.BLACK, 3)
        self.assertEqual(PlayerColor.BLACK, player_info.get_color())
        self.assertEqual(0, player_info.get_fish())
        self.assertEqual([], player_info.get_penguin_posns())
        self.assertEqual(3, player_info._amount_penguins_placeable)

    def test_adding_single_penguin(self):
        """
        Purpose: Test what happens when you initialize the player info with a valid
        age, color, and number of penguins placeable, and add a penguin at a position
        Signature: Void -> Void
        """
        player_info = PlayerInfo(PlayerColor.BLACK, 3)
        player_info.place_new_penguin((0,0))
        self.assertEqual([(0,0)], player_info.get_penguin_posns())

        player_info.place_new_penguin((0,1))
        self.assertEqual([(0,0), (0,1)], player_info.get_penguin_posns())

    def test_adding_fish(self):
        """
        Purpose: Test what happens when you add fish to player info
        Signature: Void -> Void
        """
        player_info = PlayerInfo(PlayerColor.BLACK, 3)
        player_info.add_fish(11)
        self.assertEqual(11, player_info.get_fish())
        player_info.add_fish(-5)
        self.assertEqual(6, player_info.get_fish())

    def test_has_penguin_at_position(self):
        """
        Purpose: Test if a player has penguins at certain positions
        Signature: Void -> Void
        """
        player_info = PlayerInfo(PlayerColor.BLACK, 3)
        player_info.place_new_penguin((0,0))
        player_info.place_new_penguin((0,1))
        self.assertEqual([player_info.has_penguin_at_pos((0,0))], [True])
        self.assertEqual([player_info.has_penguin_at_pos((0,1))], [True])
        self.assertEqual([player_info.has_penguin_at_pos((0,2))], [False])
        self.assertEqual([player_info.has_penguin_at_pos((1,0))], [False])


if __name__ == '__main__':
    unittest.main()
