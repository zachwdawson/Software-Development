""" Class representation of a fish game state"""
from board import *
from structures import Coordinate, Player, Action, GameStatePhase
from typing import Tuple
from const import PENGUIN_COLORS
from collections import OrderedDict


class FishGameState(object):
    """
    A game state represents the state of a game at any given time. That means that it stores a FishBoard to represent the
    state of the tiles(number of fish, holes, etc.), an OrderedDict of players to maintain the players score, penguins,
    and move order, a Player to represent the player whose turn it currently is to play, and a GameStatePhase to represent
    whether we are in moving or placing stage of a game. FishGameState handles all penguin placement, penguin moving, and
    move validation. It also handles turn taking for each of the game phases: placement phase and movement phase.
    """

    def __init__(self,
                 board: FishBoard,
                 num_players: int,
                 players: List[Player],
                 current_player: Player,
                 phase: GameStatePhase
                 ):
        self.board = board
        self.num_players = num_players
        self.num_penguins = 6 - num_players
        self.players = OrderedDict()
        self.current_player = current_player
        self.phase = phase

        for player in players:
            self.players[player.color] = player

    def finalize(self):
        return FishGameState(
            board=self.board,
            num_players=self.num_players,
            players=list(self.players.values()),
            current_player=self.current_player,
            phase=GameStatePhase.FINAL,
        )

    def can_add_penguin(self, row, col, color):
        """
        Determines whether the given color penguin can add penguin
        to the requested row and col.
        :param row: the row of the tile to add penguin on
        :param col: the col of the tile to add penguin on
        :param color: the color who will be adding the penguin
        :return: Whether the requested add penguin can be done and the reason
        if not.
        """
        selected_player, = [player for player in self.players.values() if player.color == color]

        if self.phase != GameStatePhase.INITIAL:
            return False, "Cannot add a penguin to a non-initial phase..."

        elif color != self.current_player.color:
            return False, f"Not player {color} turn."
        elif len(selected_player.penguins) >= self.num_penguins:
            return False, "Max number of penguins reached for this player"

        return self.validate_input(color=color, row=row, col=col)

    def add_penguin(self, row, col, color):
        """
        Add a penguin for the given player id at the given row and column
        :param row: the row of the tile to add penguin on
        :param col: the col of the tile to add penguin on
        :param color: the color who will be adding the penguin
        :return: Updated GameState with added penguin
        """

        is_valid, err = self.can_add_penguin(row=row, col=col, color=color)
        if not is_valid:
            raise ValueError(err)

        players = []
        for player in self.players.values():
            if player.color == color:
                players.append(Player.from_dict(
                    {**player._asdict(),
                     **{"penguins": player.penguins + [(Coordinate(row, col))]
                        }}))
            else:
                players.append(player)

        return FishGameState(
            board=self.board,
            num_players=self.num_players,
            players=players,
            current_player=self.next_player(),
            phase=self.phase
        )

    def has_penguin(self, row, col):
        """
        Check if this row and tile has a penguin on it
        :param row: The row of the tile to check
        :param col: The col of the tile to check
        :return: True if a penguin is on this tile, False otherwise
        """
        for _, player in self.players.items():
            for penguin in player.penguins:
                if penguin.row == row and penguin.col == col:
                    return True
        return False

    def is_valid_move(self, color, start_row, start_col, end_row, end_col):
        if color != self.current_player.color:
            return False, f"Not player {color} turn."

        if not self.players[color].owns_penguin(row=start_row, col=start_col):
            return False, "Player color %s does not own penguin at row %d, col %d" % (color, start_row, start_col)

        is_valid, err = self.validate_input(color=color, row=end_row, col=end_col)
        if not is_valid:
            return False, err

        if not self.board.is_reachable_from(start_row, start_col, end_row, end_col, [
            penguin for _, player in self.players.items() for penguin in player.penguins
        ]):
            return False, "Not a valid move"

        return True, ""

    def can_move_penguin(self, color, start_row, start_col, end_row, end_col):
        """
        Determines whether based the requested penguin the requested movement
        is valid.
        :param color: the color of the player who wants to move the penguin
        :param start_row: the current row of the penguin to be moved
        :param start_col: the current col of the penguin to be moved
        :param end_row: the desired row to which the penguin will be moved
        :param end_col: the desired col to which the penguin will be moved
        :return: Whether the movement can be taken and the reason why it cant (optional)
        """

        if self.phase != GameStatePhase.FINAL:
            return False, "Cannot move a penguin in initial phase."
        return self.is_valid_move(color, start_row, start_col, end_row, end_col)

    def move_penguin(self, color, start_row, start_col, end_row, end_col):
        """
        Move penguin for player with color from start position to end position if possible.
        :param color: the color of the player who wants to move the penguin
        :param start_row: the current row of the penguin to be moved
        :param start_col: the current col of the penguin to be moved
        :param end_row: the desired row to which the penguin will be moved
        :param end_col: the desired col to which the penguin will be moved
        :return: a new FishGameState with the action taken.
        """

        is_valid, err = self.can_move_penguin(color, start_row, start_col, end_row, end_col)
        if not is_valid:
            raise ValueError(err)

        players = [
            Player.from_dict(
                {**self.players[color]._asdict(),
                 **{"score": (self.players[color].score + self.board.retrieve_num_fish(start_row, start_col))},
                 **{"penguins": [
                     Coordinate(end_row, end_col)
                     if penguin.row == start_row and penguin.col == start_col
                     else penguin
                     for penguin in self.players[color].penguins
                 ]}
                 })
            if player.color == color
            else player
            for player in self.players.values()
        ]
        board = self.board.create_hole(start_row, start_col)
        return FishGameState(
            board=board,
            num_players=self.num_players,
            players=players,
            current_player=self.next_player(),
            phase=self.phase
        )

    def skip(self):
        return FishGameState(
            board=self.board,
            num_players=self.num_players,
            players=list(self.players.values()),
            current_player=self.next_player(),
            phase=self.phase
        )

    def kick_player(self, player_to_kick: Player):
        updated_players = [
            Player.from_dict({**player._asdict(), **{"penguins": []} })
            if player.color == player_to_kick.color
            else player
            for player in self.players.values()
        ]
        return FishGameState(
            board=self.board,
            num_players=self.num_players,
            players=updated_players,
            current_player=self.next_player(),
            phase=self.phase
        )

    def next_player(self):
        """
        Increment the current player to the next player in the ordered dict of Players based on the ordering of colors
        :return: Return the player whose turn is next for the current state, and will be current player for the next state.
        """
        current_player_index, = [idx for idx, color in enumerate(list(self.players.keys()))
                                 if self.current_player.color == color]
        next_player_index = (current_player_index + 1) % len(self.players)
        _, player = list(self.players.items())[next_player_index]
        return player

    def end_game(self):
        """
        check if the game is over(no player can move)
        :return: Updated state in OVER phase if over, original state otherwise
        """
        return FishGameState(
            board=self.board,
            num_players=self.num_players,
            players=list(self.players.values()),
            current_player=self.current_player,
            phase=GameStatePhase.OVER
        )


    def check_any_player_can_move(self):
        """
        Check if any of the players in this game can move
        :return: True if any penguin of any player can move, False otherwise
        """
        for _, player in self.players.items():
            if self.check_player_can_move(player):
                return True
        return False

    def check_player_can_move(self, player: Player):
        """
        Check if a specific player in this game can move
        :param player: The player who's penguins will be checked for movement
        :return: True if any penguin of this player can move, False otherwise
        """
        for penguin in player.penguins:
            reachable_tiles = self.board.get_reachable_tiles(penguin.row, penguin.col, [
                penguin for _, player in self.players.items() for penguin in player.penguins
            ])
            if len(reachable_tiles) > 0:
                return True
        return False

    def get_player_actions_from(self, player: Player) -> List[Action]:
        """
        For the given player, find all possible moves for each of this players penguins.
        :param player: The player whose possible moves will be calculated.
        :return: List[Action] representing all possible moves for this Player's penguins
        """

        if player is None:
            return None

        if player == 0:
            return None

        player_actions = []
        for penguin in player.penguins:
            reachable_tiles = self.board.get_reachable_tiles(penguin.row, penguin.col, [
                penguin for _, player in self.players.items() for penguin in player.penguins
            ])
            potential_actions = []
            for reachable_tile in reachable_tiles:
                potential_actions.append(
                    Action(Coordinate(penguin.row, penguin.col), Coordinate(reachable_tile.row, reachable_tile.col),
                           player.color))
            player_actions.extend(potential_actions)
        return player_actions

    def get_player_color(self, row, col):
        """
        Get the player color for the penguin at this row and column
        :param row: The row of the penguin to be ckecked
        :param col: The col of the penguin to be ckecked
        :return: Return the color of the penguin at this location if it exists, -1 if it does not
        """
        for color, player in self.players.items():
            for penguin in player.penguins:
                if penguin.row == row and penguin.col == col:
                    return player.color
        return ""

    def validate_input(self, color, row, col) -> Tuple[bool, str]:
        """
        Check if this is a valid color, row, and col. Will return a boolean representing if the information is valid
        and error message if it not valid. an input is considered invalid if the color is not in the valid range,
        the row and column is not a valid combination, the row and column is a hole, or the tile already has a penguin
        on it.
        :param color: The color of the penguin to be ckecked
        :param row: The row of the penguin to be ckecked
        :param col: The col of the penguin to be ckecked
        :return: Tuple[Whether input valid, reason why message is invalid]
        """
        if color not in PENGUIN_COLORS:
            return False, "Player color does not exist"
        elif not self.board.valid_row_and_col(row, col):
            return False, "Row and column do not exist in this board"
        elif not self.board.is_tile(row, col):
            return False, "Row and column is a hole"
        elif self.has_penguin(row, col):
            return False, "This tile already has a penguin"
        return True, ""

    def is_equal(self, other):
        return self.num_players == other.num_players and \
               self.num_penguins == other.num_penguins and \
               self.players == other.players and \
               self.current_player == other.current_player and \
               self.board.is_equal(other.board)