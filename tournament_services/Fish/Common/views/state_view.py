from tkinter import *
from typing import Tuple

from Fish.Common.representations.game_state import FishGameState, PlayerOrder
from Fish.Common.views.pieces_view import FishBoardView, FishAvatarView


class FishGameStateView(object):

    @classmethod
    def display_state(cls, state: FishGameState):
        window, canvas = cls.create_state_window(state)
        window.mainloop()

    @classmethod
    def create_state_window(cls, state: FishGameState) -> Tuple[Tk, Canvas]:
        """
        Purpose: Display the game state overall
        Signature: FishGameState -> TkWindow TkCanvas
        :param state: current state of the game to display
        :return: the state window and canvas the board is drawn on
        """
        board = state.get_board()
        window, canvas = FishBoardView.create_board_window(Tk(), board)
        FishGameStateView.render_penguins(state, canvas)
        order = state.get_player_order()
        fish_dict = dict()
        for color in order:
            fish_dict[color] = state.get_fish_for_player(color)
        FishGameStateView.render_order(order, window)
        FishGameStateView.render_fish(fish_dict, window)
        FishGameStateView.render_game_phase(state.get_game_phase(), window)
        FishGameStateView.render_turn(state.get_current_turn(), window)
        return window, canvas

    @classmethod
    def render_penguins(cls, state: FishGameState, canvas: Canvas) -> None:
        """
        Purpose: Display the penguins on the board
        Signature: FishGameState TkCanvas -> Void
        :param state: State that we want to render penguins for
        :param canvas: Canvas that we want to display penguins on
        """
        order = state.get_player_order()
        penguins = dict()
        for color in order:
            penguins[color] = state.get_penguins_for_player(color)
        for color, coordinates in penguins.items():
            for coord in coordinates:
                x_offset, y_offset = FishBoardView.offset_coordinate(*coord)
                FishAvatarView.add_avatar_to_canvas(canvas, x_offset, y_offset, color.value)

    @classmethod
    def render_order(cls, order: PlayerOrder, window: Tk):
        """
        Purpose: Display the order of player movement
        Signature: PlayerOrder TkWindow -> Void
        :param order: Order of players
        :param window: Window that we want to display order of players on
        """
        order_text = ''
        for i, color in enumerate(order):
            order_text += '{}: {} \n'.format(str(i + 1), color.value.upper())
        order_label = Label(window, text='Order: {}'.format(str(order_text)))
        order_label.pack()

    @classmethod
    def render_fish(cls, fish_dict, window):
        """
        Purpose: Display the amount of fish per person
        Signature: Dict[PlayerColor, int] TkWindow -> Void
        :param fish_dict: dictionary mapping players to how many fish they have
        :param window: Window that we want to display amount for each player on
        """
        fish_text = ''
        for color, fish_amnt in fish_dict.items():
            fish_text += '{}: {} fish \n'.format(color.value, str(fish_amnt))
        fish_label = Label(window, text='Fish amount: {}'.format(str(fish_text)))
        fish_label.pack()

    @classmethod
    def render_game_phase(cls, phase, window):
        """
        Purpose: Display the game phase
        Signature: GamePhase TkWindow -> Void
        :param phase: Phase of game
        :param window: Window that we want to display amount of fish on
        """
        phase_label = Label(window, text='Game phase: {}'.format(str(phase.value)))
        phase_label.pack()

    @classmethod
    def render_turn(cls, turn_color, window):
        """Purpose: Display the current turn of a player
        Signature: GamePhase TkWindow -> Void
        :param turn_color: Turn color for whose turn it is in the game
        :param window: Window that we want to display amount of fish on
        """
        turn_label = Label(window, text='Player turn: {}'.format(str(turn_color.value)))
        turn_label.pack()

