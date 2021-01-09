#!/usr/bin/env python3
import json

# relative path importing so that it can be used as a script
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  '..')))

from Fish.Other.test_harness_transformation import TestHarnessTransformationHelper as THHelper
from Fish.Common.game_tree import FishGameTree


def run_xtree(move_response_query):
    """
    Purpose: Run the xtree test harness
    Signature: Move-Response-Query -> Void
    :param move_response_query: MoveResponseQuery object
    as specified by harness to print out test values
    :return: Prints out the Action that results from moving the first
    move and moving the second player to the neighbor of the first
    """
    # Convert JSON into state and our coordinates
    state_json = move_response_query['state']
    from_coord = move_response_query['from']
    to_coord = move_response_query['to']
    state = THHelper.create_state(state_json)
    # Save the to position of the action we are are gonna take and
    # find its neighbors
    to_posn_dh = THHelper.convert_to_double_height(to_coord[0], to_coord[1])
    from_posn_dh = THHelper.convert_to_double_height(from_coord[0], from_coord[1])
    to_posn_neighbors = THHelper.find_coord_neighbors(to_posn_dh)
    # Take the move on the state_json
    tree = FishGameTree(state)
    new_state = tree.validate_and_apply_action((from_posn_dh, to_posn_dh))
    # Then we want to see if the new state_json which means
    # the next player(if it exists) has a move to a neighbor
    # of the to_pos
    new_tree = FishGameTree(new_state)
    final_actions = find_if_valid_move_from_state(new_tree, to_posn_neighbors)
    if final_actions:
        final_action = find_tiebreaker(final_actions)
        move_from_posn, move_to_posn = final_action
        move_from_org_posn = THHelper.convert_back_to_posn(move_from_posn[0], move_from_posn[1])
        move_to_org_posn = THHelper.convert_back_to_posn(move_to_posn[0], move_to_posn[1])
        final_action = [move_from_org_posn, move_to_org_posn]
        print(json.dumps(final_action))
    else:
        print(json.dumps(False))


def find_tiebreaker(final_actions):
    from_positions = [action[0] for action in final_actions]
    # sort by row and col order
    sorted_from_pos = sorted(from_positions, key=lambda position: (position[1], position[0]))
    top_from_idx = from_positions.index(sorted_from_pos[0])
    return final_actions[top_from_idx]


def find_if_valid_move_from_state(tree, to_posn_list):
    """
    Purpose: Find if there is a valid move from a state to another using a trees children
    and a list of valid moves that should be considered in order
    Signature: FishGameTree [Coordinate] -> Optional[Action]
    :param tree: Tree we can use to see future possible moves
    :param to_posn_list: List of positions that we should try and see if there is a move to
    in order
    """
    final_actions = []
    found_first_direction = False
    for to_posn in to_posn_list:
        if not found_first_direction:
            for move_from_posn, move_to_posn in tree.get_children_moves():
                if to_posn == move_to_posn:
                    found_first_direction = True
                    final_actions.append((move_from_posn, move_to_posn))
    return final_actions


if __name__ == '__main__':
    move_resp_q = json.loads(THHelper.read_from_stdin())
    run_xtree(move_resp_q)
