import tkinter as tk
from PIL import ImageTk, Image
from typing import List
from const import WIN_H, WIN_W, FISH_IMAGE_PATH, PENGUIN_PATHS, HEX_HEIGHT, HEX_RADIUS, HEX_SIDE, PENGUIN_COLORS
from structures import EventHandler, Hexagon


class HexGridView(object):
    """
    HexGridView acts constructs a view and draws hexagons onto it.
    The hexagons must be drawn with certain colors to represent whether or not it is a hole, certain number of fish,
    and certain number of penguins.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIN_W, height=WIN_H)
        self.canvas.configure(background='grey')

        # For whatever reason, there needs to a reference active of
        # of the image in order for tkinter to render this.
        self._rendered_fish_ = {}
        self._rendered_user_ = {}

    """
    Draw the given hexagon and bind correct tags to allow for button presses.
    :param hexagon: Hexagon object that will be draws, includes row,col,x,y, and all vertices.
    :param event_handlers: events that must be bound to certain button presses.
    :param num_fish: number of fish to be drawn on hexagon
    :param is_tile: True if is_tile, False if hole
    :param border_color: Color of border of hexagon
    :param border_width: Width of hexagon border to be drawn.
    :param render_player: True if a player belongs on this tile, False otherwise
    :param player_color: color of player to be drawn, tells which color should be used.
    
    :return: self
    """
    def draw_hex(self,
                 hexagon: Hexagon,
                 event_handlers: List[EventHandler],
                 num_fish=0,
                 is_tile=True,
                 border_color="black",
                 border_width=1,
                 render_player=False,
                 player_color="",
                 ):

        # Checking if player is valid
        if render_player and player_color not in PENGUIN_COLORS:
            raise ValueError(f"[draw_hex] : player color must be in {PENGUIN_COLORS}, given {player_color}")

        # check if the tile is a hole or not
        fill_color = "yellow" if is_tile else "grey"

        # draw hexagon
        drawn_polygon = self.canvas.create_polygon(
            hexagon.vertices, outline=border_color, fill=fill_color, width=border_width, tags=f"{hexagon.x}:{hexagon.y}")

        # Add event handlers to hexagon
        for event_handler in event_handlers:
            self.canvas.tag_bind(
                drawn_polygon,
                event_handler.event,
                lambda event: event_handler.handler(event, drawn_polygon, hexagon)
            )

        # Keep Reference of fish to be drawn
        self._rendered_fish_[drawn_polygon] = [
            ImageTk.PhotoImage(Image.open(FISH_IMAGE_PATH).resize((40, 18)))
            for _ in range(num_fish)
        ]

        col = int(hexagon.x / (HEX_SIDE + HEX_HEIGHT)) % 2
        for i, fish_img in enumerate(self._rendered_fish_[drawn_polygon]):
            offset = (13 * (i + 1))
            self.canvas.create_image(
                hexagon.x + (2 * HEX_HEIGHT),
                hexagon.y + (2 * HEX_RADIUS) + (col * HEX_RADIUS) - offset,
                image=fish_img,
                tags="fish")

        if render_player:
            if player_color not in self._rendered_user_:
                self._rendered_user_[player_color] = []

            path = PENGUIN_PATHS[player_color]
            self._rendered_user_[player_color].append(
                ImageTk.PhotoImage(Image.open(path).resize((30, 30)))
            )

            offset = 25
            self.canvas.create_image(
                hexagon.x + (2 * HEX_HEIGHT),
                hexagon.y + (2 * HEX_RADIUS) + (col * HEX_RADIUS) - offset,
                image=self._rendered_user_[player_color][0],
                tags="user")

    def execute(self):
        self.canvas.lift("fish")
        self.canvas.lift("user")
        self.canvas.pack()
        self.root.mainloop()
