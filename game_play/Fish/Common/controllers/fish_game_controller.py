from typing import List
from structures import EventHandler, Hexagon, Coordinate
from const import HEX_SIDE, HEX_HEIGHT, HEX_DIAMETER
from state import FishGameState
from views.render import HexGridView


class FishGameBehavior(object):
    """
    The behavior class for FishGame - handles events that have occurred from the view
    """

    def __init__(self, state: FishGameState, view: HexGridView):
        self.state = state

    def on_left_button_press_down(self, event: str, tag, hexagon):
        """
        Note: Not Fully Implemented...

        Handles Left Button Pressed Down event. Currently only prints number of fish on tile pressed.
        :param event: The event that has occurred on the view
        :param tag: the associated tag
        :param hexagon: The hexagon that was clicked.
        :return: None
        """
        print(self.state.board.retrieve_num_fish(hexagon.row, hexagon.col))

        pass


class FishGameController(object):
    """
    The Fish Game controller bridges the FishGame model and the View.
    The controller takes data from the model (current a state) and tells the view what to render, like tiles, holes, fish, and players.
    """

    def __init__(self,
                 behavior: FishGameBehavior,
                 view: HexGridView,
                 state: FishGameState):
        """
        :param behavior: class that handles the behavior the game should taken, given an event from the view.
        :param view: The view that will be used.
        :param state: the state of the game (currently this is a game state).
        """

        self._behavior_ = behavior
        self.view = view
        self.state = state

        # Calculating Hexagons starting x,y points.
        hexagons = []
        for col in range(self.state.board.num_cols):
            point_y = 0
            for row in range(self.state.board.num_rows):
                point_x = col * 2 * (HEX_SIDE + HEX_HEIGHT)
                if row % 2 == 1:
                    point_x = point_x + (HEX_SIDE + HEX_HEIGHT)

                hexagon = Hexagon.create(
                    row=row,
                    col=col,
                    x=point_x,
                    y=point_y
                )
                point_y = (point_y + HEX_DIAMETER) if row % 2 == 1 else point_y
                hexagons.append(hexagon)

        for hexagon in hexagons:
            to_render_player = [
                player.color
                for player in self.state.players.values()
                if player.owns_penguin(row=hexagon.row, col=hexagon.col)
            ]

            if len(to_render_player) > 1:
                raise ValueError("[GameState Error] : More than 1 penguin cannot be on a tile.")

            if len(to_render_player) == 1:
                player_color, = to_render_player
            else:
                player_color = -1

            self.view.draw_hex(
                hexagon=hexagon,
                event_handlers=self._build_event_handlers_(),
                num_fish=self.state.board.retrieve_num_fish(hexagon.row, hexagon.col),
                is_tile=self.state.board.is_tile(hexagon.row, hexagon.col),
                render_player=len(to_render_player) == 1,
                player_color=player_color
            )

    def _build_event_handlers_(self) -> List[EventHandler]:
        """
        Creates all the event handlers the view needs to be aware of.
        :return: a list of event handlers
        """
        button_press_1 = EventHandler(
            event='<ButtonPress-1>',
            handler=self._behavior_.on_left_button_press_down)

        return [button_press_1]

    def run(self):
        """
        Begins the gameplay session.
        :return: N/A
        """
        self.view.execute()
