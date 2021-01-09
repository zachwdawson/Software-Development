import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import importlib
xtree = importlib.import_module('xtree')
from Fish.Other.test_harness_transformation import TestHarnessTransformationHelper as THHelper
from Fish.Common.game_tree import FishGameTree
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor

class XTreeTests(unittest.TestCase):
    """
    Test our test harness for Milestone 4
    """

    def test_find_tiebreaker(self):
        """
        Purpose: Test finding the tiebreaker for choosing a move
        """
        final_actions = [((0, 0), (1, 1)), ((1, 1), (2, 2))]
        self.assertEqual(((0, 0), (1, 1)), xtree.find_tiebreaker(final_actions))

        final_actions = [((0, 2), (1, 1)), ((0, 1), (2, 2))]
        self.assertEqual(((0, 1), (2, 2)), xtree.find_tiebreaker(final_actions))

    def test_find_if_valid_move(self):
        """
        Purpose: Test finding valid move from a tree
        """
        state = {
                "players": [
                    {
                        "color": "red",
                        "score": 10,
                        "places": [[0, 0]]
                    },
                    {
                        "color": "black",
                        "score": 1,
                        "places": [[0, 2], [0, 1]]
                    }
                ],
                "board": [[4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [3, 3, 3, 3]]
            }
        state = THHelper.create_state(state)
        state.move_penguin(PlayerColor.RED, (0, 0), (3, 3))
        tree = FishGameTree(state)
        neighbors = THHelper.find_coord_neighbors([3, 3])
        self.assertListEqual([((4, 0) ,(3, 1)), ((2, 0), (3, 1))], xtree.find_if_valid_move_from_state(tree, neighbors))

if __name__ == '__main__':
    unittest.main()