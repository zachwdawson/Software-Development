import unittest

import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.game_state import FishBoardModel, FishGameStateFactory
from Fish.Common.game_tree import FishGameTree
from Fish.Common.representations.types import Action


class GameTreeTest(unittest.TestCase):
    """
    Test cases for creating a tree for the game state
    """
    penguins_first_player = [(2, 0), (2, 2), (1, 1), (3, 1)]
    penguins_second_player = [(0, 0), (0, 2), (3, 3), (1, 3)]

    penguins_four_player = [penguins_first_player[:2], penguins_first_player[2:4],
                            penguins_second_player[:2], penguins_second_player[2:4]]

    @staticmethod
    def create_small_tree(rows=4, columns=4):
        """
        Purpose: Create a small tree to be used in tests
        Signature: Int Int -> FishGameTree
        :param rows: Amount of rows for the board
        :param columns: Amount of columns for the board
        """
        small_board = FishBoardModel.create_with_same_fish_amount(rows, columns, 3)
        game_state = FishGameStateFactory.create_move_penguins_state(
            small_board, [(PlayerColor.RED, GameTreeTest.penguins_first_player, 5),
                          (PlayerColor.BLACK, GameTreeTest.penguins_second_player, 0)]
        )
        tree_node = FishGameTree(game_state)
        return tree_node

    @staticmethod
    def create_multiple_players(rows=5, columns=5):
        """
        Purpose: Create a larger board with multiple players to be used for testing
        Signature: Int Int -> FishGameTree
        :param rows: Amount of rows for the board
        :param columns: Amount of columns for the board
        """
        small_board = FishBoardModel.create_with_same_fish_amount(rows, columns, 3)
        game_state = FishGameStateFactory.create_move_penguins_state(
            small_board, [(PlayerColor.RED, GameTreeTest.penguins_four_player[1], 0),
                          (PlayerColor.BLACK, GameTreeTest.penguins_four_player[0], 0),
                          (PlayerColor.BROWN, GameTreeTest.penguins_four_player[2], 0),
                          (PlayerColor.WHITE, GameTreeTest.penguins_four_player[3], 0),
                          ]
        )
        tree_node = FishGameTree(game_state)
        return tree_node

    def test_not_move_state(self):
        """
        Purpose: Test trying to create a tree from a state that is not
                 the player movement state
        """
        with self.assertRaises(ValueError):
            small_board = FishBoardModel.create_with_same_fish_amount(4, 3, 3)
            game_state = FishGameStateFactory.create_place_penguins_state(
                small_board, [(PlayerColor.RED, []), (PlayerColor.BLACK, [])]
            )
            FishGameTree(game_state)

    def test_state_validation(self):
        """
        Purpose: Test that we can get a state from validating and then applying an action
        """
        tree_node = self.create_small_tree()

        # testing valid
        action: Action = ((3, 1), (4, 2))
        valid_state = tree_node.validate_and_apply_action(action)
        self.assertIsNotNone(valid_state)
        self.assertEqual(valid_state.get_fish_for_player(tree_node.get_turn_color()), 8)

    def test_invalid_state_failure(self):
        """
        Purpose: Test that an action is flagged as invalid when we try to apply an invalid
                 action
        """
        tree_node = self.create_small_tree()
        invalid_action = ((3, 1), (5, 1))
        # with no penguin at beginning position
        invalid_action_2 = ((6, 0), (5, 1))

        # with other penguin at ending position
        invalid_action_3 = ((3, 1), (3, 3))

        with self.assertRaises(ValueError):
            tree_node.validate_and_apply_action(invalid_action)
        with self.assertRaises(ValueError):
            tree_node.validate_and_apply_action(invalid_action_2)
        with self.assertRaises(ValueError):
            tree_node.validate_and_apply_action(invalid_action_3)

    def test_apply_successors(self):
        """
        Purpose: Test applying function to all successors
        """
        tree_node = self.create_small_tree()
        first_color = tree_node.get_turn_color()
        applied_list = tree_node.apply_to_successors(lambda state: state.get_fish_for_player(first_color))
        self.assertEqual([8, 8, 8], applied_list)

    def test_apply_successors_bad_func(self):
        """
        Purpose: Test trying to apply function to all successors that is not a function
        """
        tree_node = self.create_small_tree()
        with self.assertRaises(TypeError):
            tree_node.apply_to_successors(2)

    def test_get_successor_color_multiple_players(self):
        """
        Purpose: Test getting the successor color with multiple players
        """
        current_tree = self.create_multiple_players()
        order = current_tree.state.get_player_order()
        self.assertEqual(order[0], current_tree.get_turn_color())
        for child in current_tree.generate_direct_children():
            self.assertEqual(order[1], child.get_turn_color())
            if child.possible_moves:
                current_tree = child
                break
        for next_child in current_tree.generate_direct_children():
            self.assertEqual(order[2], next_child.get_turn_color())
            if next_child.get_children_moves():
                current_tree = next_child
                break
        for last_child in current_tree.generate_direct_children():
            self.assertEqual(order[3], last_child.get_turn_color())

    def get_penguin_set_for_tree_node_at_depth(self, tree_node, depth, colors):
        """
        Purpose: Get a set of what penguins possible placements n turns in the future are
        with both generators and return that set
        Signature: FishGameTree Int [PlayerColor] -> Set(Coordinate)
        :param tree_node: The node that we are getting the penguin set for
        :param depth: Depth we are finding the children at
        :param colors: Colors of players in the game to get the penguins for.
        """
        penguin_set = set()
        preorder_set = set()
        # Add penguins from original set
        for color in colors:
            for penguin in tree_node.state.get_penguins_for_player(color):
                penguin_set.add(penguin)
                preorder_set.add(penguin)

        # add penguins from BFS children generation
        for tree in tree_node.generate_children(depth=depth):
            for color in colors:
                for penguin in tree.state.get_penguins_for_player(color):
                    penguin_set.add(penguin)

        # add penguins from preorder generator
        for tree in tree_node.generate_children(depth=depth):
            for color in colors:
                for penguin in tree.state.get_penguins_for_player(color):
                    preorder_set.add(penguin)

        self.assertSetEqual(penguin_set, preorder_set)
        return penguin_set

    def test_generate_direct_children(self):
        """
        Purpose: Test generating direct children and see that we can get relevant info about
        penguins
        """
        tree_node = self.create_small_tree()
        colors = tree_node.state.get_player_order()
        expected_penguin_set = set(self.penguins_first_player + self.penguins_second_player)
        # Add other positions to set that can be reached
        expected_penguin_set.update([(4, 0), (4, 2), (5, 3)])
        penguin_set = self.get_penguin_set_for_tree_node_at_depth(tree_node, 1, colors)
        self.assertSetEqual(expected_penguin_set, penguin_set)

    def test_generate_depth2_children(self):
        """
        Purpose: Test generating children at depth 2 and getting relevant info about penguins
        penguins
        """
        tree_node = self.create_small_tree()
        colors = tree_node.state.get_player_order()
        expected_penguin_set = set(self.penguins_first_player + self.penguins_second_player)
        # Columns 3 and part of 4 now reachable
        expected_penguin_set.update([(4, 0), (4, 2), (5, 1), (5, 3),
                                     (6, 0)])
        penguin_set = self.get_penguin_set_for_tree_node_at_depth(tree_node, 2, colors)
        self.assertSetEqual(expected_penguin_set, penguin_set)

    def test_generate_depth3_children(self):
        """
        Purpose: Test generating children at depth 3 and getting relevant info about penguins
        penguins
        """
        tree_node = self.create_small_tree()
        colors = tree_node.state.get_player_order()
        expected_penguin_set = set(self.penguins_first_player + self.penguins_second_player)
        # Columns 3 and 4 now reachable
        expected_penguin_set.update([(4, 0), (4, 2), (5, 1), (5, 3),
                                     (6, 0), (6, 2), (7, 1), (7, 3)])
        penguin_set = self.get_penguin_set_for_tree_node_at_depth(tree_node, 3, colors)
        self.assertSetEqual(expected_penguin_set, penguin_set)



    def test_grab_large_depth_generation(self):
        """
        Purpose: Test using the generator to just get some values when you are looking at a
        large depth
        """
        large_tree = self.create_multiple_players(8, 8)
        generator = large_tree.generate_children(depth=30)
        for _ in range(1000):
            tree = next(generator)
            self.assertGreater(tree.depth, 0)

    def test_no_more_moves(self):
        """
        Purpose: Test trying to generate moves when there are no more moves
        """
        done_tree = self.create_small_tree(4, 2)
        self.assertEqual(0, len(list(done_tree.generate_children(depth=10))))
        self.assertTrue(done_tree.is_end_game_state())

    def test_stuck_state(self):
        """
        Purpose: Show generation of children when the current player cannot move
        """
        player_row1 = [(0, 0), (0, 2), (1, 1)]
        player_row2 = [(2, 0), (3, 1), (2, 2)]
        small_board = FishBoardModel.create_with_same_fish_amount(3, 3, 3)
        game_state = FishGameStateFactory.create_move_penguins_state(
            small_board, [(PlayerColor.RED, player_row1, 0),
                          (PlayerColor.BLACK, player_row2, 0)],
            check_penguin_amount=False
        )
        stuck_tree = FishGameTree(game_state)
        self.assertEqual(1, len(list(stuck_tree.generate_direct_children())))
        self.assertEqual(PlayerColor.BLACK, list(stuck_tree.generate_direct_children())[0].get_turn_color())


if __name__ == '__main__':
    unittest.main()
