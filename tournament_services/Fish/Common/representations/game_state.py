import copy
from typing import List, Dict, Tuple, Optional

from Fish.Common.representations.game_state_error import PenguinPlacementError, PenguinMovementError
from Fish.Common.representations.types import Coordinate

from Fish.Common.representations.enumerations.game_phase import GamePhase
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor

from Fish.Common.representations.fish_board import FishBoardModel
from Fish.Common.representations.player_info import PlayerInfo

"""
A PlayerOrder is a list containing values from the PlayerColor enumeration
INTERPRETATION: The list contains as many elements as the amount of players and 
lists those in increasing order
"""
PlayerOrder = List[PlayerColor]


class FishGameState(object):
    """
    A GameState is,
    {
    CurrentPhase: GamePhase,
    Board: FishBoardModel,
    Players: Dictionary<PlayerColor, PlayerInfo>,
    PlayerOrder: PlayerOrder,
    Turn: PlayerColor
    }
    INTERPRETATION: Represents a complete state for a game of Fish, containing information about
    the board and the players.

    The GameState contains a board representation, which we defined in our FishBoardModel class. This is the board on
    which the game will be played (tiles removed, players placing or moving penguins, etc.)

    Additionally, a GameState contains the current phase the game is in, which is one of:
    -Place Penguins (where players initially place the penguins on a board)
    -Move Penguins (where players move their penguins to different tiles on a board and collect fish)
    -End Game (where none of the players can make a valid move and winners can be determined)
    A state must save the phase information in order to determine what moves are valid in the current state

    The GameState contains a dictionary mapping the player color to our internal representation of that players data, represented by the PlayerInfo
    class. This class contains information relating to the players' penguins as well as the player's total number of fish collected.
    It also contains the player's color, which is used to differentiate each player from the others.

    The GameState also contains a sorted list of the order of the players where the player at the beginning of the list goes first
    and the player at the end of the list goes last. Players are represented by their color in this list as well.

    Finally, The GameState contains a Turn, which is a PlayerColor object that represents the color of the player whose turn
    it currently is, tracked using the PlayerOrder variable.

    """

    def __init__(self, board: FishBoardModel, player_colors: List[PlayerColor]):
        """
        Purpose: Initialize a game state for Fish in its beginning state
                 Note: This will not add the players, need to call initalizae players function
        Signature: FishBoardModel -> FishGameState
        :param board: The instance of the board representation that we
                      will be using for this game state
        :param player_colors: List of player colors in the order that the players play.
                              This will encode the order
        """
        self._game_board: FishBoardModel = board
        self._players: Dict[PlayerColor, PlayerInfo] = dict()
        self._game_phase: GamePhase = GamePhase.PLACE_PENGUINS
        self.initialize_players(player_colors)
        self._player_order = player_colors
        self._turn = self._player_order[0]

    def initialize_players(self, player_colors: List[PlayerColor]) -> None:
        """
        Purpose: Initialize the players in a Fish game, creating an order and adding
                 them to our internal representation.
        Signature: List[int] -> Void
        :param player_colors: List of player colors in the order in which they play
        :return: Returns an array that maps the original list of ages
                 to the color for each of those ages
        """
        if len(player_colors) > len(PlayerColor):
            raise ValueError('At max {}} players (only {}} colors)'.format(len(PlayerColor), len(PlayerColor)))
        if len(player_colors) < 2:
            raise ValueError('Need at least 2 players')

        # each player gets 6 - N penguins where N is the amount of players
        amount_penguins = 6 - len(player_colors)
        for color in player_colors:
            self._players[color] = PlayerInfo(color, amount_penguins)

    def remove_color_from_game(self, color):
        """
        Purpose: Remove a player of a certain color from a Fish game. This takes them out of the order of players
        and also removes their information from the game.
        Signature: PlayerColor -> None
        :param color: Color that we want to remove from this Fish game.
        """
        if color not in self._player_order:
            raise ValueError('Color must be in game')
        # Remove from player info, update turn to next player and remove from order
        del self._players[color]
        if self.get_current_turn() == color:
            self.increase_turn()
        self._player_order.remove(color)

    def get_board(self) -> FishBoardModel:
        """
        Purpose: Return a copy of the board for a game state
        Signature: Void -> FishBoardModel
        :return: A copy of the board for a game state, so that originally state is not modified
        """
        return copy.deepcopy(self._game_board)

    def get_player_order(self) -> List[PlayerColor]:
        """
        Purpose: Return a list of the players order for a game state
        Signature: Void -> [PlayerColor]
        :return: Returns the order of the players
        """
        return self._player_order

    def get_current_turn(self) -> PlayerColor:
        """
        Purpose: Get the current turn for this game state
        Signature: Void -> PlayerColor
        :return: Player color representing whose turn it is
        """
        return self._turn

    def set_turn(self, color: PlayerColor):
        """
        Purpose: Set the players turn to a specific value
        Signature: PlayerColor -> Void
        """
        if color not in self._player_order:
            raise ValueError('Cant set turn to a player not in the game')
        else:
            self._turn = color

    def get_penguins_for_player(self, player_color) -> Optional[List[Coordinate]]:
        """
        Purpose: Return a list of the penguins for a certain players color
        Signature: PlayerColor -> Optional[List[Coordinate]]
        :param player_color: Player we are getting the penguin coordinates for
        :return: List of coordinates for a player or None if no player of that color
        """
        player = self._players.get(player_color)
        if player:
            return player.get_penguin_posns()
        else:
            return None

    def get_fish_for_player(self, player_color) -> Optional[int]:
        """
        Purpose: Return amount of fish for a certain players color
        Signature: PlayerColor -> Optional[int]
        :param player_color: Player we are getting the amount of fish for
        :return: Amount of fish for player or None if no player of that color
        """
        player = self._players.get(player_color)
        if player:
            return player.get_fish()
        else:
            return None

    def get_game_phase(self):
        """
        Purpose: Get the game phase for a game state
        Signature: None -> GamePhase
        :return: The game phase for a given game state,.
        """
        return self._game_phase

    def set_game_phase(self, game_phase: GamePhase) -> None:
        """
        Purpose: Set the phase of the game to a certain phase
        Signature: GamePhase -> Void
        :param game_phase: the phase of the game that we are setting the game to.
        """
        self._game_phase = game_phase

    def add_fish_to_player(self, color: PlayerColor, fish_amount: int) -> None:
        """
        Purpose: Add fish amount to a certain player
        Signature: PlayerColor Int -> Void
        :param color: Color of player that we are adding fish to
        :param fish_amount: Amount of fish that we are adding to the player
        """
        if fish_amount < 0:
            raise ValueError('Fish amount must be positive')
        self._players[color].add_fish(fish_amount)

    def check_penguin_amount(self, amount_players: int,
                             placed_penguins: Dict[PlayerColor, List[Coordinate]], should_all_be_placed: bool) -> None:
        """
        Purpose: Check properties of lists of penguins that are going to be create.
                 This can be used to check during the initialization state,
                 or during the moving state
        Signature: Int Dict[Color, List[Coordinate]] Boolean -> Void
        :param amount_players: Amount of players in the certain game
        :param placed_penguins: Dictionary containing all player colors in the game and checking
                                mapping to the coordinate of the penguin placed for each player
        :param should_all_be_placed: Whether all of the penguins for a player should be placed already
                                     or not
        :return: Raise ValueError if any of the data is invalid (different amount of players passed
                 in then penguins, too many penguins, wrong amount placed).
        """
        if not len(self._player_order) == len(placed_penguins):
            raise ValueError('Needs to be same amount of players as penguins')
        # A valid state placement of penguins take at most 6 - N penguins
        if not all(len(penguin_list) <= 6 - amount_players for penguin_list in placed_penguins.values()):
            raise ValueError('Each player can at most have 6 - {} penguins placed.'.format(self._player_order))
        amount_placed = [len(placed_penguins[color]) for color in self._player_order]
        if should_all_be_placed:
            is_correct_amount_placed = all(amount == 6 - amount_players
                                           for amount in amount_placed)
        else:
            is_correct_amount_placed = all(amount == amount_placed[0] or amount == amount_placed[0] - 1
                                           for amount in amount_placed)

        if not is_correct_amount_placed:
            raise ValueError('Amount of penguins placed is not allowed')

    def _enforce_game_phase(self, phase: GamePhase):
        """
        Purpose: Enforce a certain game phase, throwing an error if not in that phase
        Signature: GamePhase -> Void
        :param phase: The certain game phase we want to enforce.
        """
        if self._game_phase != phase:
            raise ValueError('Game phase must be in {} for this action to occur'.format(phase))

    def _enforce_turn(self, color):
        """
        Purpose: Enforce that turn is a certain color. Used for checking if players
        can make an action on the current state
        Signature: PlayerColor -> Void
        """
        if self.get_current_turn() != color:
            raise ValueError('Turn should be equal to this players color')

    def increase_turn(self):
        """
        Purpose: Helper method to increase a turn in a game
        Signature: Void -> VOid
        """
        player_index = self._player_order.index(self._turn)
        if player_index != len(self._player_order) - 1:
            player_index += 1
        else:
            player_index = 0
        self._turn = self._player_order[player_index]

    def place_penguin(self, color: PlayerColor, place_pos: Coordinate, increase_turn: bool = True) -> None:
        """
        Purpose: Place a penguin on behalf of a player
        Signature: PlayerColor Coordinate -> Void
        :param color: Color of player we are placing the penguin on behalf of
        :param place_pos: Position we are placing the penguin
        :param increase_turn: Whether the turn should be increased when the move completes
        """
        self._enforce_turn(color)
        self._enforce_game_phase(GamePhase.PLACE_PENGUINS)
        # check if on board
        try:
            tile = self._game_board.get_tile_at_coord(*place_pos)
        # Catch error from game board itself to throw more specific error
        except ValueError:
            raise PenguinPlacementError('column and row in coordinate given is off of board')
        if not tile:
            raise PenguinPlacementError("Cannot place penguin at {}, there is no tile here!".format(place_pos))
        # check if penguin there
        if self._is_penguin_at_pos(place_pos):
            raise PenguinPlacementError('Cant place penguin at '
                                        '{}, there is already a penguin there'.format(place_pos))
        # place on board
        self._players[color].place_new_penguin(place_pos)
        if increase_turn:
            self.increase_turn()

    def move_penguin(self, color: PlayerColor,
                     penguin_pos: Coordinate, move_to_pos: Coordinate) -> None:
        """
        Purpose: Move a penguin on behalf of a player
        Signature: PlayerColor Coordinate Coordinate -> Void
        :param color: Color player we are moving on behalf of
        :param penguin_pos: Position of penguin we want to move
        :param move_to_pos: Position that we want to move the penguin to
        """
        self._enforce_turn(color)
        self._enforce_game_phase(GamePhase.MOVE_PENGUINS)
        # check if player has penguin at position
        if not self._players[color].has_penguin_at_pos(penguin_pos):
            raise PenguinMovementError('Cannot move penguin because no penguin for player {} at '
                             'initial position {}'.format(color, penguin_pos))
        # check if player can move to tile that they want to
        if move_to_pos not in self.find_valid_moves_from_pos(penguin_pos):
            raise PenguinMovementError('That is not a valid move to move '
                                       'your penguin to position {}'.format(move_to_pos))
        self._players[color].move_penguin_at_pos(penguin_pos, move_to_pos)
        self.add_fish_to_player(color, self._game_board.get_tile_at_coord(*penguin_pos).num_fish)
        self._game_board.remove_tile(*penguin_pos)
        self.increase_turn()

    #TODO maybe add a game over method using this
    def can_any_player_move(self) -> bool:
        """
        Purpose: Check if any player can move
        Signature: Void -> Boolean
        :return: boolean representing which player can move an avatar
        """
        can_move = False
        for player in self._players.values():
            for penguin_pos in player.get_penguin_posns():
                moves = self.find_valid_moves_from_pos(penguin_pos)
                if moves:
                    can_move = True
                    break
        return can_move

    def _is_penguin_at_pos(self, pos: Coordinate) -> bool:
        """
        Purpose: Check if any player has a penguin at a given position
        Signature: Coordinate -> Boolean
        :param pos: Position we are are checking for a player penguin
        :return: Boolean representing whether any player has a penguin at a given position
        """
        penguin_at_pos = False
        for player in self._players.values():
            if player.has_penguin_at_pos(pos):
                penguin_at_pos = True
        return penguin_at_pos

    def find_valid_moves_from_pos(self, pos: Coordinate) -> List[Coordinate]:
        """
        Purpose: Find all the possible valid moves from a coordinate
        Signature: Coordinate -> List<Coordinate>
        :param pos: Coordinate that we are checking valid moves for
        :return: A list of possible valid moves from a coordinate, where valid moves mean straight lines get stopped
                 by penguins
        """
        lines = self._game_board.find_straight_line_positions(*pos)
        moves: List[Coordinate] = []
        for direction, straight_line in lines.items():
            straight_line = self._stop_straight_line_at_penguin(straight_line)
            moves += straight_line
        return moves

    def _stop_straight_line_at_penguin(self, line: List[Coordinate]) -> List[Coordinate]:
        """
        Purpose: Change a straight line to only return all straight lines from a penguin
        Signature: List<Coordinate> -> List<Coordinate>
        :param line: Straight line of points in a certain direction
        :return: line edited if a penguin was in a list of straight line coordinates to not include anything past
        that penguin
        """
        penguin_stop: int = len(line)
        for i, coordinate in enumerate(line):
            if self._is_penguin_at_pos(coordinate):
                penguin_stop = i
                break
        return line[:penguin_stop]


class FishGameStateFactory(object):
    """
    This class represents a factory for creating all different intermediate Fish game states, at any
    point in any phase, from the referee removal phase to the end game phase. It enforces logical checks
    on whether you are passing in correct information to create those states as well.
    """

    """
    This represents the default color order in a game of Fish. For N amount of players, N amount
    of these colors will be used in order to delegate colors to players within the game.
    """
    DEFAULT_COLOR_ORDER = [PlayerColor.RED, PlayerColor.WHITE, PlayerColor.BROWN, PlayerColor.BLACK]

    @classmethod
    def convert_ages_to_penguin_order(cls, ages: List[int]) -> List[Tuple[int, PlayerColor]]:
        """
        Purpose: Convert a list of ages into an order for the color of penguins
        Signature: List[int] -> List[Tuple(int, PlayerColor)]
        :param ages: List of ages of players representing the age in integer value
        :return: Sorted list comparing the players age to their color to give to the referee
        """
        player_colors = cls.DEFAULT_COLOR_ORDER[:len(ages)]
        age_to_color = zip(ages, player_colors)
        sorted_by_age = sorted(age_to_color, key=lambda age_color: (age_color[0]))
        return sorted_by_age

    @classmethod
    def create_game_state_with_dimensions(cls, row: int, col: int,
                                          player_colors: List[PlayerColor]) -> FishGameState:
        """
        Purpose: Convenience method for creating a board with a certain number of rows and columns
                 and a random amount of fish on each tile
        Signature: Int Int -> FishGameState
        :param row: Amount of rows for the board
        :param col: Amount of columns for the board
        :param player_colors: Colors of the players in the order that they play. Initializes a state
                              where no penguins have been placed.
        :return: Game state ready for ref to remove tiles with random amount of fish on each tile
        """
        game_state = FishGameState(FishBoardModel.create_with_holes(row, col, set(), 0), player_colors)
        return game_state

    @classmethod
    def create_game_state_with_num_fish(cls, row: int, col: int, num_fish: int,
                                        player_colors: List[PlayerColor]) -> FishGameState:
        """
        Purpose: Convenience method for creating a board with a certain number of rows and columns
                 and a certain number of fish on each row. no holes.
        Signature: Int Int -> FishGameState
        :param row: Amount of rows for the board
        :param col: Amount of columns for the board
        :param num_fish: Amount of fish to add to each tiles.
        :param player_colors: Colors of the players in the order that they play. Initializes a state
                              where no penguins have been placed.
        :return: Game state ready for ref to remove tiles with correct amount of fish on each tile
        """
        game_state = FishGameState(FishBoardModel.create_with_same_fish_amount(row, col, num_fish), player_colors)
        return game_state

    @classmethod
    def create_place_penguins_state(cls, game_board: FishBoardModel,
                                    player_info: List[Tuple[PlayerColor, List[Coordinate]]],
                                    turn: PlayerColor = None,
                                    check_penguin_amount: bool = True) -> FishGameState:
        """
        Purpose: Create a game state in the player initialization phase, with 0 to 6 - N
                 (where N is the number of players) placed penguins
        Signature: FishBoardModel List[int, List[Coordinate]] -> FishGameState
        :param game_board: Game board representation to create state with
        :param player_info: Info about each player needed to initialize the state, namely the placement of penguins and
                            the amount of Fish, in order of which player color goes first
        :param check_penguin_amount: Whether to check the amount of penguins placed is valid according
        to the rules of Fish
        :param turn: Turn to set the game state to for creating the state
        :return: Game state of a game in the beginning/middle/end of the player initialization phase
                 (phase where player places penguins)
        """
        player_colors = [color for color, coordinate in player_info]
        game_state = FishGameState(game_board, player_colors)
        # add 0 for amount of fish to tuple
        for i, _ in enumerate(player_info):
            player_info[i] += (0,)
        game_state = FishGameStateFactory._add_fish_and_penguins(game_state, player_info, False, check_penguin_amount)
        if turn:
            game_state.set_turn(turn)
        return game_state

    @classmethod
    def create_move_penguins_state(cls, game_board: FishBoardModel,
                                   player_info: List[Tuple[PlayerColor, List[Coordinate], int]],
                                   turn: PlayerColor = None,
                                   check_penguin_amount: bool = True):
        """
        Purpose: Create a game state in the penguin moving phase, with all placed penguins
                 and players with some amount of fish 0 or greater
        Signature: FishBoardModel List[int, List[Coordinate], int] -> FishGameState
        :param game_board: Game board representation to create state with
        :param player_info: List of information needed to create each players state, namely
                            the age, the coordinates of the penguins and the amount of fish
        :param turn: Turn to set the game state to for creating the state
        :param check_penguin_amount: Whether we should check the amount of penguins we are placing
        :return: Game state of a game in the beginning/middle/end of the player movement phase (where players
                 go in turns of moving their penguins)
        """
        # need to have 6 - N penguins for each player and penguins can't be on same spot
        player_colors = [color for color, coordinate, fish in player_info]
        game_state = FishGameState(game_board, player_colors)
        game_state = FishGameStateFactory._add_fish_and_penguins(game_state, player_info, True,
                                                                 check_penguin_amount)
        game_state.set_game_phase(GamePhase.MOVE_PENGUINS)
        if turn:
            game_state.set_turn(turn)
        return game_state

    @classmethod
    def _add_fish_and_penguins(cls, game_state: FishGameState,
                               player_info: List[Tuple[PlayerColor, List[Coordinate], int]],
                               all_pengs_placed,
                               check_peng_amount) -> FishGameState:
        """
        Purpose: Add fish and penguins to a game state to move it into a certain phase
        Signature: FishGameState [(PlayerColor, [Coordinate], int] Boolean  -> FishGameState
        :param game_state: Current game state we are adding fish and penguins to
        :param player_info: List of information needed to create each players state, namely
                            the player color, the coordinates of the penguins and the amount of fish.
                            In order of the order of players
        :param all_pengs_placed: Whether all penguins should be placed
        :param check_peng_amount: Whether we are checking the penguin amount we place on the board
        :return: GameState with fish and penguins added to it
        """
        # initialize dictionaries to add to board and check that penguins being placed are valid
        penguin_placement_dict = {}

        # turn into penguin placement dictionary
        for color, coordinates, _ in player_info:
            penguin_placement_dict[color] = coordinates

        if check_peng_amount:
            game_state.check_penguin_amount(len(player_info), penguin_placement_dict, all_pengs_placed)

        # place penguins and add fish
        game_state.set_game_phase(GamePhase.PLACE_PENGUINS)
        FishGameStateFactory._place_all_penguins(game_state, penguin_placement_dict)
        for player, _, fish_amount in player_info:
            game_state.add_fish_to_player(player, fish_amount)
        return game_state

    @classmethod
    def create_end_game_state(cls, game_board: FishBoardModel,
                              player_info: List[Tuple[PlayerColor, List[Coordinate], int]]) -> FishGameState:
        """
        Purpose: Create a game state in the penguin moving phase, with all placed penguins
                 and players with some amount of fish 0 or greater
        Signature: FishBoardModel List[int, List[Coordinate], int] -> FishGameState
        :param game_board: Game board representation to create state with
        :param player_info: List of information needed to create each players state, namely
                            the player color, the coordinates of the penguins and the amount of fish.
                            In order of the order of players
        :return: Game state of a game in the endgame phase, (where no more penguins can be moved)
        """
        game_state = FishGameStateFactory.create_move_penguins_state(game_board, player_info)
        game_state.set_game_phase(GamePhase.END_GAME)
        if game_state.can_any_player_move():
            raise ValueError('Must be no players to move for end game state')
        return game_state

    @staticmethod
    def _place_all_penguins(game_state: FishGameState, penguins_by_color: Dict[PlayerColor, List[Coordinate]]):
        """
        Purpose: Place multiple penguins for multiple different colors all at once
        Signature: FishGameState Dict[PlayerColor, [Coordinate]] -> Void
        :param game_state: The game state we are adding the penguins to
        :param penguins_by_color: Dictionary mapping the color to the list of penguins that should be placed
                                  for that color
        """
        original_turn = game_state.get_current_turn()
        for color, penguins in penguins_by_color.items():
            for penguin in penguins:
                game_state.set_turn(color)
                game_state.place_penguin(color, penguin, increase_turn=False)
        game_state.set_turn(original_turn)
