import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import importlib
xstate = importlib.import_module('xstate')

from Fish.Other.test_harness_transformation import TestHarnessTransformationHelper as THHelper
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor


class XstateTests(unittest.TestCase):
    """
    Test our test harness for Milestone 4
    """

    def test_create_player_info(self):
        """
        Purpose: Test creating player info list from JSON input
        Signature: Void -> Void
        """
        players = [
            {
                "color": "red",
                "score": 10,
                "places": [[0, 1], [1, 1], [0, 3]]
            },
            {
                "color": "black",
                "score": 12,
                "places": [[2, 2], [3, 1], [4, 0]]
            }
        ]

        ret_list = THHelper.create_player_info_list(players)
        self.assertListEqual([(PlayerColor.RED, [(2, 0), (3, 1), (6, 0)], 10),
                              (PlayerColor.BLACK, [(4, 2), (3, 3), (0, 4)], 12)], ret_list)


if __name__ == '__main__':
    unittest.main()
