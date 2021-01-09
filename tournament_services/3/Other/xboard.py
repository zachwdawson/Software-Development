#!/usr/bin/env python3
import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  '..')))

from Fish.Other.test_harness_transformation import TestHarnessTransformationHelper as THHelper


def create_board_and_find_positions(board_posn):
    """
    Purpose: Create our board representation to find straight line positions
             from a given board and coordinate representation
    Signature: BoardPosn -> List<Coordinate>
    :param board_posn: Board position object containing a board and a position to find
                       position from
    """
    board = board_posn['board']
    board = THHelper.parse_board(board)
    posn = board_posn['position']
    position = THHelper.convert_to_double_height(posn[0], posn[1])
    straight_line_posns = board.find_straight_line_positions(*position)
    return straight_line_posns


if __name__ == '__main__':
    json_obj = json.loads(THHelper.read_from_stdin())
    posns = create_board_and_find_positions(json_obj)
    values_sum = sum([len(positions) for positions in posns.values()])
    print(values_sum)
