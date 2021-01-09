import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import importlib
xboard = importlib.import_module('xboard')
from Fish.Other.test_harness_transformation import TestHarnessTransformationHelper as THHelper


class MyTestCase(unittest.TestCase):
    """
    Test our test harness for Milestone 3
    """

    def test_posn_transformation_even_row(self):
        """
        Purpose: Test transforming position in an even row
        Signature: Void -> Void
        """
        board_posn = {'board': [[0, 0, 1], [1, 3, 1], [1, 1, 1]],
                      'position': [3, 1]}
        self.assertEqual((3, 3), THHelper.convert_to_double_height(*board_posn['position']))

    def test_posn_transformation_odd_row(self):
        """
        Purpose: Test transforming position in an odd row
        Signature: Void -> Void
        """
        board_posn = {'board': [[0, 0, 1, 1], [1, 3, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1]],
                      'position': [4, 1]}
        self.assertEqual((2, 4), THHelper.convert_to_double_height(*board_posn['position']))


if __name__ == '__main__':
    unittest.main()
