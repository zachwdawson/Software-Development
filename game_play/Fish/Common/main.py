#!/usr/bin/env python3

import argparse
from structures import Coordinate
import demos.render_board_demo as board
import demos.render_game_state as state


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-demo1', dest="board_demo1", action="store_true")
    parser.add_argument('--board-demo2', dest="board_demo2", action="store_true")
    parser.add_argument('--board-demo3', dest="board_demo3", action="store_true")
    parser.add_argument('--state-demo1', dest="state_demo1", action="store_true")
    parser.add_argument('--state-demo2', dest="state_demo2", action="store_true")

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_arguments()
    if args.board_demo1:
        controller = board.Demo1()
    elif args.board_demo2:
        controller = board.Demo2(2)
    elif args.board_demo3:
        controller = board.Demo3(holes=[
           Coordinate(row=1, col=0),
           Coordinate(row=0, col=1),
        ])
    elif args.state_demo1:
        controller = state.Demo1()
    elif args.state_demo2:
        controller = state.Demo2()
    else:
        raise ValueError("Must provide demo number")

    controller.run()
