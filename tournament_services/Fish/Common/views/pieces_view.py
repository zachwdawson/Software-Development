from tkinter import *
from typing import Tuple

from Fish.Common.representations.fish_board import FishBoardModel
from Fish.Common.representations.fish_tile import FishTile


class FishTileView(object):

    # constants for the different colors for the board
    TILE_MISSING_FILL = ''
    TILE_FILL_COLOR = 'orange'
    BORDER_OUTLINE_COLOR = 'white'
    FISH_COLOR = 'blue'

    # Line width (in pixels for the hexagon)
    HEXAGON_LINE_WIDTH = 3

    # Size constants for hexagon
    SIZE_MULTIPLIER = 70  # size multiplier in pixels that overall hexagon size is based on
    HEX_WIDTH = 3 * SIZE_MULTIPLIER
    HEX_HEIGHT = 2 * SIZE_MULTIPLIER

    # Size constants for fish on hexagon
    FISH_HEIGHT = HEX_HEIGHT / FishTile.MAX_AMOUNT_FISH
    END_OF_FISH_TAIL = 2 * SIZE_MULTIPLIER
    FISH_BODY_SIZE_CONSTANT = 2 * SIZE_MULTIPLIER * 0.9  # constant for where the fish body stops and the tail starts
    TAIL_SHRINK_CONSTANT = SIZE_MULTIPLIER / 10  # applied to both sides of tail to shrink it in size

    @classmethod
    def _hexagon_points(cls):
        """
        Purpose: Return the basic points of a FishTile hexagon
        Signature: Void -> (Int, Int)
        :return: List of points representing the points in a basic hexagon
        """
        middle_left_corner = (0, FishTileView.SIZE_MULTIPLIER)
        bottom_left_corner = (FishTileView.SIZE_MULTIPLIER, 0)
        bottom_right_corner = (2 * FishTileView.SIZE_MULTIPLIER, 0)
        middle_right_corner = (cls.HEX_WIDTH, FishTileView.SIZE_MULTIPLIER)
        top_right_corner = (cls.HEX_HEIGHT, cls.HEX_HEIGHT)
        top_left_corner = (FishTileView.SIZE_MULTIPLIER, cls.HEX_HEIGHT)
        return [middle_left_corner, bottom_left_corner, bottom_right_corner, middle_right_corner, top_right_corner,
                top_left_corner, middle_left_corner]

    @classmethod
    def _fish_body_points(cls, fish_num):
        """
        Fetch the points for a given fish body
        Signature: Int -> [(Int, Int)]
        :param fish_num: which fish (from top to bottom) is being drawn on the hexagon
        :return: A list of the points which make up the fish body oval
        """

        # y coordinate is from top of FISH_HEIGHT for a given fish, to bottom of FISH_HEIGHT for a given FISH
        left_oval_side = FishTileView.SIZE_MULTIPLIER, \
                         (fish_num * cls.FISH_HEIGHT) + (cls.FISH_HEIGHT / FishTile.MAX_AMOUNT_FISH)
        right_oval_side = cls.FISH_BODY_SIZE_CONSTANT, \
                          (fish_num + 1) * cls.FISH_HEIGHT - (cls.FISH_HEIGHT / FishTile.MAX_AMOUNT_FISH)
        return [left_oval_side, right_oval_side]

    @classmethod
    def _fish_tail_points(cls, fish_num):
        """
        Purpose: Returns the points creating a triangle for the fish tail
        Signature: Int -> [(Int, Int)]
        :param fish_num: Which number fish (from top to bottom) is being drawn on the canvas
        :return: List of (x,y) points that make up a triangle for the fish tail
        """
        middle_of_fish = fish_num + 0.5
        point_of_triangle = cls.FISH_BODY_SIZE_CONSTANT, middle_of_fish * cls.FISH_HEIGHT
        # y coordinate goes from top of current fish to bottom of next fish
        top_back = cls.END_OF_FISH_TAIL, (fish_num * cls.FISH_HEIGHT) + cls.TAIL_SHRINK_CONSTANT
        bottom_back = cls.END_OF_FISH_TAIL, ((fish_num + 1) * cls.FISH_HEIGHT) - cls.TAIL_SHRINK_CONSTANT

        return [point_of_triangle, top_back, bottom_back, point_of_triangle]

    @classmethod
    def add_fish_tile_to_canvas(cls, canvas, fish_tile, tag, x_offset, y_offset):
        """
        Purpose: Add fish tile to the board canvas
        Signature: TkCanvas FishTile Tag Int Int -> Void
        :param canvas: Canvas to have the fish tile added to
        :param fish_tile: Fish tile that is being represented
        :param tag: Tag that provides a reference string for a tile
        :param x_offset: Value on the canvas that the tile should be offset by
        :param y_offset: Value on the canvas that the tile should be offset by
        :return: Modifies the canvas to add the Fish tile to it
        """
        cls.add_hexagon_to_canvas(canvas, fish_tile, tag, x_offset, y_offset)
        if fish_tile:
            for fish_num in range(fish_tile.num_fish):
                cls.create_body(canvas, fish_num, x_offset, y_offset, tag)
                cls.create_tail(canvas, fish_num, x_offset, y_offset, tag)

    @classmethod
    def add_hexagon_to_canvas(cls, canvas, fish_tile, tag, x_offset, y_offset):
        """
        Purpose: Add hexagon to canvas
        Signature: TkCanvas FishTile String Int Int -> Void
        :param canvas: Canvas to have the fish tile added to
        :param fish_tile: Fish tile that is being represented
        :param tag: Tag that provides a reference string for a tile
        :param x_offset: x-value on the canvas that the tile should be offset by
        :param y_offset: y-value on the canvas that the tile should be offset by
        :return: Modifies the canvas to add hexagon to it
        """
        points = [(x + x_offset, y + y_offset) for (x, y) in cls._hexagon_points()]
        if fish_tile:
            fill = cls.TILE_FILL_COLOR
        else:
            fill = cls.TILE_MISSING_FILL
        canvas.create_polygon(*points, fill=fill, width=cls.HEXAGON_LINE_WIDTH,
                              tag=tag, outline=cls.BORDER_OUTLINE_COLOR)

    @classmethod
    def create_body(cls, canvas, fish_num, x_offset, y_offset, tag):
        """
        Purpose: Create the body of a fish on a canvas
        Signature: TkCanvas Int Int Int String -> Void
        :param canvas: Canvas that fish body is being added to
        :param fish_num: Represents which fish on a given fish tile this is
        :param x_offset: x-value on the canvas that the fish body should be offset by
        :param y_offset: y-value on the canvas that the fish body should be offset by
        :param tag: Unique ID that tags this FishBody as an object
        :return: Adds fish body to the canvas
        """
        points = [(x + x_offset, y + y_offset) for (x, y) in cls._fish_body_points(fish_num)]
        canvas.create_oval(*points,
                           fill=cls.FISH_COLOR,
                           tag=tag)

    @classmethod
    def create_tail(cls, canvas, fish_num, x_offset, y_offset, tag):
        """
        Purpose: Create the tail of a fish on a canvas
        Signature: TkCanvas Int Int Int String -> Void
        :param canvas: Canvas that fish body is being added to
        :param fish_num: Represents which fish on a given fish tile this is
        :param x_offset: x-value on the canvas that the fish tail should be offset by
        :param y_offset: y-value on the canvas that the fish tail should be offset by
        :param tag: Unique ID that tags this fish tail as an object
        :return: Adds fish tail to the canvas
        """
        points = [(x + x_offset, y + y_offset) for (x, y) in cls._fish_tail_points(fish_num)]
        canvas.create_polygon(*points,
                              fill=cls.FISH_COLOR,
                              tag=tag)


class FishAvatarView(object):
    """
    Class representing visual representation for avatars (penguins)
    """
    TOP_LEFT_CORNER = FishTileView.SIZE_MULTIPLIER * 1.3  # determines x + y for top left corner
    BOTTOM_RIGHT_CORNER = FishTileView.SIZE_MULTIPLIER * 1.7 # determines x + y for botom right corner
    AVATAR_WIDTH = 3

    @classmethod
    def add_avatar_to_canvas(cls, canvas, x_offset, y_offset, color):
        """
        Purpose: Add penguin avatar to canvas
        Signature: TkCanvas Int Int FishAvatar -> Void
        :param canvas: canvas that penguin avatar being added to
        :param x_offset: x offset that is added to the x-coordinate for the penguin
        :param y_offset: y offset that is being added to the y-coord for the penguin
        :return: Modifies canvas to add penguin to the canvas
        """
        points = [((x + x_offset), (y + y_offset)) for (x, y) in cls._avatar_points()]
        canvas.create_rectangle(*points, outline=color, width=cls.AVATAR_WIDTH)

    @classmethod
    def _avatar_points(cls):
        """
        Purpose: Get points for a penguin avatar
        Signature: Void -> [(Int, Int])
        :return: Array of x,y coordinate representing a penguin avatar
        """
        top_left = cls.TOP_LEFT_CORNER, cls.TOP_LEFT_CORNER
        bottom_right = cls.BOTTOM_RIGHT_CORNER, cls.BOTTOM_RIGHT_CORNER

        return [top_left, bottom_right]


class FishBoardView(object):

    @classmethod
    def create_board_window(cls, window: Tk, fish_board: FishBoardModel) -> Tuple[Tk, Canvas]:
        """
        Purpose: Render a visual representation of a Fish Board
        Signature: TkWindow FishBoardModel -> TkWindow TkCanvas
        :param window: TkWindow object to add the board to
        :param fish_board: FishBoardModel that represents the data about the game state
        :return: Returns the window object and the canvas object to be able to display the window and further modify
                 the canvas
        """
        if not isinstance(fish_board, FishBoardModel):
            raise TypeError('Must be a Fish board passed in to be rendered')
        board_canvas = cls._create_empty_canvas(fish_board, window)
        canvas_with_tiles = cls._populate_board_with_tiles(fish_board, board_canvas)
        canvas_with_tiles.pack()
        return window, board_canvas

    @classmethod
    def _create_empty_canvas(cls, fish_board: FishBoardModel, window: Tk) -> Canvas:
        """
        Purpose: Create an empty canvas that is the right size to accommodate all of the tiles for a certain board
        Signature: FishBoardModel TkWindow -> TkCanvas
        :param fish_board: Fish board that we are creating a canvas for
        :param window: Tkinter window that are creating the canvas in
        :return: Canvas that we can draw on that is the size of the board
        """
        rows, columns = fish_board.get_dimensions()
        # One column with 2 hexes is 5 width for first column + 4 width for the following columns
        board_width = (5 + ((columns - 1) * 4)) * FishTileView.SIZE_MULTIPLIER
        # Height of board is amount of rows + 1 since 4 * height for something stacked on one another and 3 * height
        # for being next to one another
        board_height = (rows + 1) * FishTileView.SIZE_MULTIPLIER
        canvas = Canvas(window, width=board_width, height=board_height)
        return canvas

    @classmethod
    def _populate_board_with_tiles(cls, fish_board: FishBoardModel, board_canvas: Canvas) -> Canvas:
        """
        Purpose: Populate an empty canvas with renderings of tiles
        Signature: FishBoardModel Canvas -> Canvas
        :param fish_board: Fish board that contains information about tiles
        :param board_canvas: Board canvas that is to be drawn on
        :return: The board canvas with the tiles drawn onto it
        """
        # x offset is 2 * size for each hexagon
        x_offset_func = lambda x: 2 * FishTileView.SIZE_MULTIPLIER * x
        # y offset is the height of one hexagon times the double height
        # else on odd rows it goes down 1 size instead of 2 * size
        y_offset_func = lambda y: FishTileView.HEX_HEIGHT * (y / 2) if y % 2 == 0 else (FishTileView.HEX_HEIGHT / 2) * y

        for x, y in fish_board.get_tile_coords():
            tile = fish_board.get_tile_at_coord(x, y)
            x_offset = x_offset_func(x)
            y_offset = y_offset_func(y)
            # TODO use tag in controller
            FishTileView.add_fish_tile_to_canvas(board_canvas, tile, '{}{}'.format(x, y), x_offset, y_offset)
        return board_canvas

    @classmethod
    def offset_coordinate(cls, x, y):
        # x offset is 2 * size for each hexagon
        x_offset_func = lambda x: 2 * FishTileView.SIZE_MULTIPLIER * x
        # y offset is the height of one hexagon times the double height
        # else on odd rows it goes down 1 size instead of 2 * size
        y_offset_func = lambda y: FishTileView.HEX_HEIGHT * (y / 2) if y % 2 == 0 else (FishTileView.HEX_HEIGHT / 2) * y

        return x_offset_func(x), y_offset_func(y)

    @classmethod
    def show_window(cls, board: FishBoardModel) -> None:
        """
        Purpose: Create and show a Tkinter window
        Signature: FishBoard -> Void
        :return: Calls Tkinter function to display a window on your screen
        """
        window = Tk()
        window, canvas = cls.create_board_window(window, board)
        window.mainloop()
