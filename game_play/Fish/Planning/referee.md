# Referee Memo

## Referee

### Overview:
The referee component is set with administrating and managing a set players for a single gameplay. It creates the board and interacts with 
the various player interfaces to retrieve information about the initial game state setup. Once the game is setup, it transition to a state
of gameplay - where the board cannot be mutated and players cannot place anymore penguins. Within gameplay, the referee will interact 
with each player to obtain their move information, as well as, share information about the current game state. The ordering of player's turn is based on their age. Players are expected to provide valid moves in the context of both the board (i.e a negative row/col is not valid) and the gamestate (i.e moves to holes are not valid). If a player violates these expectations they will be forfeited from the game. Rounds are played until all players cannot provide a valid move, thus the winners are awarded based on their scores, or a single player is left in the game.

The referee does not handle information about whom the players will be or how many players it will be managing. The referee also does not handle anything after the gameplay beyond informing the players of winners and the tournament administor of a shutdown game.

### Representation
The referee will be a single object that simply takes in a list of players and initializes a game state that will be used to place all penguins  After penguins have been placed, a decision tree is built to be used for the proceeding movements and validation.

### Protocol
After initialization, the first player is notified that it is their turn to place a penguin. We accept a placement and, if valid, will update the 
initial game state. This will be repeated for all players until all players have placed their penguins. Then the referee will then transition to a state
where the penguins can only be moved. The player movement will be repeated in the same fashion until the game is over, at which point we will notify the players that the game is over and the winners of their status.

## API

#-----------------Initialization--------

def init(players: Player):
    """
    Begins the initial phase of game where the board is setup and players 
    can only place penguins.
    """

#-----------------Game Play-------------

def notify_player_placement() -> void
    """
    Notify the current player to place one of its penguin.
    :return: N/A
    """

def accept_player_placement(player: Player, placement: Coordinate) -> void:
    """
    Accepts the players requested placement and performs the requested placement 
    given that the placement is valid and it is the given player's turn. Invalid 
    moves will result in the player being kicked.
    :return: N/A
    """

def end_penguin_placement() -> void: 
    """
    Transitions the game from placing penguin phase to moving penguin phase.
    """

def notify_players_movement() -> void
    """
    Notify the current player that is their turns to move a penguin.
    :return: N/A
    """

def notify_player_kicked(player: Player) -> void
    """
    Notifies the given player that they've been kicked from the game for cheating.
    :return: N/A
    """

def accept_player_movement(player: Player, movement: Action) -> void:
    """
    Accepts the players requested movement and performs the requested action given that
    the movement is valid and it's the given player's turn. Invalid moves will result in 
    the player being kicked.
    :return: N/A
    """

def get_state() -> str:
    """
    Provides a serialized form of the current game state.
    :return: The string output of serializing a state.
    """


def notify_winnters()  -> void::
    """
    notify winners that they won the game.
    :return: N/A
    """

def end_game()  -> void::
    """
    Notify all's the player left in the game that the game has been concluded. 
    :return: N/A
    """
