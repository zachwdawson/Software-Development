import copy
from collections import OrderedDict
from typing import Tuple, List, Dict, Optional

from Fish.Admin.kicked_player_type import KickedPlayerType
from Fish.Admin.runtime_error import FishRuntimeException, NotWellFormedReturnValue, PlayerInternalException
from Fish.Common.game_tree import FishGameTree
from Fish.Common.player_interface import PlayerInterface
from Fish.Common.representations.enumerations.game_phase import GamePhase
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.game_state import FishGameStateFactory, FishGameState
from Fish.Common.representations.game_state_error import PenguinMovementError, PenguinPlacementError
from Fish.Common.representations.types import Coordinate, Action, coordinate_type_check, action_type_check

"""
This represents a logical player, which is a tuple containing a player interface, the interface through which we can 
interact with a player and their age, which is used to sort how players play in a game. This is what the tournament
manager will pass in to the referee. They will pass in a list of this in sorted order, which will allow a ref to create
the order fo the game.
"""
LogicalPlayer = Tuple[PlayerInterface, int]


class Referee(object):
    """
    This is a class representing a referee in the Fish game. It contains a number of fields that keep track of a single
    Fish game.

    the players instance variable represent the logical players that we have in our game. Each of these players have a
    color in the game, plus an interface we interact with to request moves from them. We save this as an ordered
    dictionary, which keeps track of the order with which the current players play in the Fish game.

    the amount_penguins_per_player variable notes the max amount of penguins each player which will get which is 6 - N where
    N is the number of players. This is useful for the placement phase, where players are placing down their penguins

    the current_game_state variable notes what the current game state of a game is. Before a referee has a game, this
    variable is None, representing that no game has been started. This will be updated, when the referee performs actions
    in the game.

    the current_game_tree represents a tree keep tracking of the current game state once the movement phase of the game
    has begun. this is used for rule checking and for keeping track of the current game state as well.

    kicked players is a dictionary representing which players have been kicked for misbehavior from the game. we keep
    track of "cheating" players, those which have made a bad logical move such placement on a square with another
    players penguins as well as failing players, which throw some abnormal runtime error. This could be a player
    returning an incorrect type or a player throwing an exception within their code.

    NOTE: We saved the following misbehavior cases for when remote play is involved:
    - A player takes too long. We think this case will happen in remote play because a player is much more likely to
    have a communication channel fall apart in remote play.
    - A player throws an internal error when they are assigned a color or told of other players color.
    This functionality is very basic with local players and as such is unlikely to create any errors, but may remotely.

    Finally, the winners variable keeps track of a list of colors representing the winners of the game.

    The component contains one public method initialize and run game, with which a tournament manager or someone else
    could spin up a referee and run a game using. The rest of the methods build on one another with an initial board
    set up method and then the phases being run in a series of rounds which each contain turns. At the end, the winners
    and kicked players are reported.
    """

    def __init__(self):
        """
        Purpose: Initialize a referee instance that could run games. This creates a referee without a game initially,
        which can then be assigned a game using initialize_and_run_game(). This sets reasonable defaults
        for variables that can then be overridden later on for an actual game.
        Signature: Void -> Void
        """
        self.players: OrderedDict[PlayerColor, PlayerInterface] = OrderedDict()
        self.amount_penguins_per_player: int = 0
        self.current_game_state: Optional[FishGameState] = None
        self.current_game_tree: Optional[FishGameTree] = None
        self.kicked_players: Dict[KickedPlayerType, List[PlayerColor]] = {KickedPlayerType.CHEATING: [],
                                                                          KickedPlayerType.FAILING: []}
        self.winners: List[PlayerColor]

    def initialize_and_run_from_game_state(self, players: List[LogicalPlayer], state: FishGameState):
        """
        Purpose: Runs a complete game of fish. This will go through every stage of the game from beginning to completion
        and inform the players and tournament manager at the phases they need to be informed in the game.
        Signature: List[LogicalPlayer] FishGameState -> Void
        :param players: List of players that will be playing this game. This includes the player components as well
                        as the age of each specific player. This list is passed in in sorted order which will allow
                        the referees to create an ordering in the game itself. The age could be used at the end
                        of the game to note back to the tournament manager that the player with this age won
                        or was kicked.
        :param state: The start state of the game to be run.
        """
        if state.get_game_phase() != GamePhase.PLACE_PENGUINS:
            raise ValueError("Must provide state that is in penguin placement state.")
        self.current_game_state = state
        self._init_board(state.get_board().rows, state.get_board().columns, players)
        self.current_game_state = state
        self._run_placement_phase()
        if not self.current_game_state.get_game_phase() == GamePhase.END_GAME:
            self._run_movement_phase()
        # Report winners and report failing and cheating players
        self._report_winners()
        self._report_kicked_players()

    def initialize_and_run_game(self, rows: int, columns: int, players: List[LogicalPlayer]):
        """
        Purpose: Runs a complete game of fish. This will go through every stage of the game from beginning to completion
        and inform the players and tournament manager at the phases they need to be informed in the game.
        Signature: Int Int List[LogicalPlayer] -> Void
        :param rows: Amount of rows in this game.
        :param columns: Amount of columns in this game.
        :param players: List of players that will be playing this game. This includes the player components as well
                        as the age of each specific player. This list is passed in in sorted order which will allow
                        the referees to create an ordering in the game itself. The age could be used at the end
                        of the game to note back to the tournament manager that the player with this age won
                        or was kicked.
        """
        self._init_board(rows, columns, players)
        self._run_placement_phase()
        if not self.current_game_state.get_game_phase() == GamePhase.END_GAME:
            self._run_movement_phase()
        # Report winners and report failing and cheating players
        self._report_winners()
        self._report_kicked_players()


    def _run_placement_phase(self):
        """
        Purpose: Run the placement phase (where players place 6 - N penguins sequentially)
        for the players in the game and update the game state accordingly.
        This will also keep track of kicked players as well as move into the move penguins state when this state is done.
        Signature: Void -> Void
        """
        players_left = True
        for _ in range(self.amount_penguins_per_player):
            self._run_placement_round()
            if len(self.players) == 0:
                players_left = False
                break
        if players_left:
            # Set phase to movement and move until nobody can
            self.current_game_state.set_game_phase(GamePhase.MOVE_PENGUINS)
            self.current_game_tree = FishGameTree(copy.deepcopy(self.current_game_state))
        else:
            self.current_game_state.set_game_phase(GamePhase.END_GAME)

    def _run_movement_phase(self):
        """
        Purpose: Run the movement phase of the game, where players can move their penguins and update
        to end game phase when no one can move or 1 or 0 players.
        Signature: Void -> Void
        """
        can_any_move = self.current_game_state.can_any_player_move()
        while can_any_move:
            self._run_movement_round()
            if len(self.players) == 0:
                break
            can_any_move = self.current_game_state.can_any_player_move()

        # set the game to end_game
        self.current_game_state.set_game_phase(GamePhase.END_GAME)

    def _init_board(self, rows: int, cols: int, players: List[LogicalPlayer]):
        """
        Purpose: Initialize a game board state for a number of players. This notes the turn of players, how many
        penguins each player can place and encodes that in the game state. The board created will have a random amount
        of fish on each tile and will have no holes. This uses the DEFAULT_COLOR_ORDER array that we have created
        which specifies that the turn order of players for a game will be 'red', 'white', 'brown', 'black' with all
        used for a for player game and only N where N is the number of players used for a game with less players.
        Signature: Int Int List[LogicalPlayer] -> Void
        :param rows: How many rows this game board will have
        :param cols: How many columns this game board will have
        :param players: A sorted list of the logical player components we can use to form our turn order. It is
                        sorted by age, which will not be used in game, but can be used to report back to the
                        tournament manager.
        """
        for idx, (player, _) in enumerate(players):
            color = FishGameStateFactory.DEFAULT_COLOR_ORDER[idx]
            self.players[color] = player
        self._init_players()
        self.amount_penguins_per_player = 6 - len(self.players)
        self.current_game_state = FishGameStateFactory.create_game_state_with_dimensions(rows, cols,
                                                                                         list(self.players.keys()))

    def _init_players(self):
        """
        Purpose: Tell each player which color they are and what color the other players are. Kick players who do not respond.
        Signature: Void -> Void
        """
        player_colors_to_kick = []
        for color, player in self.players.items():
            response = player.assign_color(color)
            if not response:
                player_colors_to_kick.append(color)

        for color in player_colors_to_kick:
            self._add_kicked_player(color, self.current_game_state.get_game_phase(), False)
        self._tell_players_of_colors()

    def _tell_players_of_colors(self):
        """
        Purpose: Tells each player the color of all of the other players. Kick players who do not respond
        Signature: Void -> Void
        """
        player_colors_to_kick = []
        for color, player in self.players.items():
            colors = list(self.players.keys())
            colors.remove(color)
            response = player.show_other_players_colors(colors)
            if not response:
                player_colors_to_kick.append(color)

        for color in player_colors_to_kick:
            self._add_kicked_player(color, self.current_game_state.get_game_phase(), False)

    def _add_kicked_player(self, color: PlayerColor, game_phase: GamePhase, cheating: bool=True):
        """
        Purpose: Remove kicked player from game and note why player was kicked. This updates all parts of the game
        (game tree/state).
        Signature: PlayerColor, bool -> Void
        """
        self.current_game_state.remove_color_from_game(color)
        if game_phase == GamePhase.MOVE_PENGUINS:
            self.current_game_tree = FishGameTree(copy.deepcopy(self.current_game_state))
        del self.players[color]
        if cheating:
            self.kicked_players[KickedPlayerType.CHEATING].append(color)
        else:
            self.kicked_players[KickedPlayerType.FAILING].append(color)

    def _run_placement_round(self):
        """
        Purpose: Runs a whole placement round, which is when each player places a penguin in the beginning of a game.
                 A player can be kicked during a placement round and the turn will continue to the next player.
        Signature: Void -> Void
        """
        for i in range(len(self.players)):
            self._run_placement_turn()
            if len(self.players) == 0:
                break

    def _run_placement_turn(self):
        """
        Purpose: Asks a player whose turn it is for penguin placement position,
        tries to execute the move and kicks player if invalid placement is passed or player fails to produce
        a well-formed move
        Signature: Void -> Void
        """
        turn = self.current_game_state.get_current_turn()
        try:
            placement_pos = self._check_player_runtime_error(turn, GamePhase.PLACE_PENGUINS)
            self.current_game_state.place_penguin(turn, placement_pos)
        except PenguinPlacementError:
            self._add_kicked_player(turn, GamePhase.PLACE_PENGUINS, cheating=True)
        except FishRuntimeException as e:
            self._add_kicked_player(turn, GamePhase.PLACE_PENGUINS, cheating=False)

    def _check_player_runtime_error(self, turn: PlayerColor, game_phase: GamePhase):
        """
        Purpose: This will check runtime errors for getting a player return value to take some action in the game of
        Fish. The errors we are checking right now are getting the right type of value back (a coordinate for placement/
        two coordinates for an action) and if the player throws some internal exception. We are saving a player taking
        too long for the remote phase, as remote communication is more likely to lead players to encounter that error.
        Signature: PlayerColor GamePhase -> Boolean
        """
        try:
            if game_phase == GamePhase.PLACE_PENGUINS:
                player_return_val = self.players[turn].player_place_penguin(copy.deepcopy(self.current_game_state))
                is_well_formed = coordinate_type_check(player_return_val)
            else:
                player_return_val = self.players[turn].player_move_penguin(copy.deepcopy(self.current_game_state))
                is_well_formed = action_type_check(player_return_val)
            if not is_well_formed:
                raise NotWellFormedReturnValue
        except Exception as e: # We want to catch any exception the player throws in runtime
            raise PlayerInternalException
        return player_return_val

    def _run_movement_round(self):
        """
        Purpose: Runs a whole movement round for a game, which is when each player moves a penguin
        from one tile to another tile
        Signature: Void -> Void
        """
        for i in range(len(self.players)):
            self._run_movement_turn()
            if len(self.players) == 0:
                break

    def _run_movement_turn(self):
        """
        Purpose: Asks a player whose turn it is for a movement action, attempts to execute
        the movement action and kicks the player if an invalid movement is passed or the player
        fails to pass back a well-formed action. Skips turn if
        the player cannot make any moves or if the game is in an end-game state where no players can make moves.
        Signature: Void -> Void
        """
        turn = self.current_game_state.get_current_turn()
        if not self.current_game_tree.is_end_game_state():
            if not self.current_game_tree.get_children_moves():
                # Only thing that happens is that turn changes
                self.current_game_state.increase_turn()
                self.current_game_tree = list(self.current_game_tree.generate_direct_children())[0]
            else:
                try:
                    action = self._check_player_runtime_error(turn, GamePhase.MOVE_PENGUINS)
                    move_from_pos, move_to_pos = action
                    self.current_game_state.move_penguin(turn, move_from_pos, move_to_pos)
                    self.current_game_tree = self.current_game_tree.validate_and_compute_node(action)
                except PenguinMovementError:
                    self._add_kicked_player(turn, GamePhase.MOVE_PENGUINS, cheating=True)
                except FishRuntimeException:
                    self._add_kicked_player(turn, GamePhase.MOVE_PENGUINS, cheating=False)

    def _report_winners(self):
        """
        Purpose: Report winners of game to players/tournament manager/observers
        involved by passing a list of winners. A winner is a player
        who received the most fish. If multiple players have the same amount of Fish both win.
        The winners will be a list of PlayerColor representing the colors of the players who
        won. If all players are kicked, then an empty list of winners is a valid thing to pass.
        Signature: Void -> Void
        """
        winners = []
        max_fish_amnt = 0
        if len(self.players):
            for color, player in self.players.items():
                fish_amnt = self.current_game_state.get_fish_for_player(color)
                if fish_amnt > max_fish_amnt:
                    max_fish_amnt = fish_amnt
                winners.append((fish_amnt, color))
            winners = [color for fish_amnt, color in winners if fish_amnt == max_fish_amnt]
            self.winners = winners
        else:
            self.winners = []

        player_colors_to_kick = []
        for color, player in self.players.items():
            response = player.inform_of_winners(winners)
            if not response:
                player_colors_to_kick.append(color)

        for color in player_colors_to_kick:
            self._add_kicked_player(color, self.current_game_state.get_game_phase(), False)

            # TODO Tell tourney manager/observers of winners when implemented

    def _report_kicked_players(self):
        """
        Purpose: Report kicked players to tournament managers and observers.
        Signature: Void -> Void
        """
        # TODO tell tourney manager of kicked players, maybe players need to know?
        pass
