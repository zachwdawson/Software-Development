import math
import os
from pathlib import Path


FISH_IMAGE_PATH = Path(f"{os.getcwd()}/resources/fish.png")

PENGUIN_PATHS = {
    "red": Path(f"{os.getcwd()}/resources/penguin0.png"),
    "white": Path(f"{os.getcwd()}/resources/penguin1.png"),
    "brown": Path(f"{os.getcwd()}/resources/penguin2.png"),
    "black": Path(f"{os.getcwd()}/resources/penguin3.png"),
}

PENGUIN_COLORS = ["red", "white", "brown", "black"]


HEXES_COLUMNS = 5
HEXES_ROWS = 5

# Hex Dimensions
HEX_SIDE = 40
HEX_HEIGHT = math.ceil(math.sin(math.radians(30)) * HEX_SIDE)
HEX_RADIUS = math.ceil(math.cos(math.radians(30)) * HEX_SIDE)
HEX_DIAMETER = 2 * HEX_RADIUS

MAX_NUM_FISH = 5

# Window Dimensions
WIN_W = HEX_DIAMETER * 1.8 * HEXES_COLUMNS
WIN_H = HEX_RADIUS * (HEXES_ROWS + 1)
CENTER_X = WIN_W / 2
CENTER_Y = WIN_H / 2
