import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import unittest
from Fish.Common.views.pieces_view import FishBoardView


class FishAvatarTest(unittest.TestCase):

    def test_not_board(self):
        """
        Purpose: Tests passing not a board to initialize view
        Signature: Void -> Void
        """
        with self.assertRaises(TypeError):
            FishBoardView.show_window(board='test')


if __name__ == '__main__':
    unittest.main()
