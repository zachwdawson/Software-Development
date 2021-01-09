from random import randint
from const import HEXES_ROWS, HEXES_COLUMNS, MAX_NUM_FISH
from board import FishBoard

def RandomlyGenerateHole(board: FishBoard, total_num_hole=2):
    for _ in range(total_num_hole):
        not_added = True
        while not_added:
            random_row = randint(0, HEXES_ROWS - 1)
            random_col = randint(0, HEXES_COLUMNS - 1)
            if board.retrieve_num_fish(random_row, random_col) == 0 and board.is_tile(random_row, random_col):
                board = board.create_hole(random_row, random_col)
                not_added = False
    return board


def RandomlyGenerateFish(board: FishBoard, total_num_fish=10):
    for _ in range(total_num_fish):
        not_added = True
        while not_added:
            random_row = randint(0, HEXES_ROWS - 1)
            random_col = randint(0, HEXES_COLUMNS - 1)
            if board.retrieve_num_fish(random_row, random_col) < MAX_NUM_FISH and board.is_tile(random_row, random_col):
                board = board.add_fish(row=random_row, col=random_col)
                not_added = False
    return board
