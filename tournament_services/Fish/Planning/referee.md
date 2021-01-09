A data representation for a Referee component demands a number of things. It will
need internal methods in order to set up, run rounds of the game and shut down the game. It will need external methods for other components to interface with this component. Finally, it will need some data internally
to run those internal methods on the game state. We will start with the data it has internally then talk about its internal methods and finally talk about its external methods (used by other components).

# Data Needed Internally:

A Referee is 
```
{
	players: [(Age, PlayerID, Player)]
	master_game_state: GameState
	master_game_tree: GameTree
	kicked_players: [(PlayerID)]
	observers: [FishGameObserver]
}
```
### Explanation of Fields:

The above shows the fields that a referee would consist of. We will explain how these fields are used and needed
by the referee.

The `players` fields will be a tuple of `Age` which is a postive integer representation
of a players age in years and `PlayerID` which is some identifiable string for a player (such as the alias they signed up to the tournament with),
and `Player` which is the logical component that a referee can actually reach out
to to request moves and transmit information to. This field overall will be used to keep track of and communicate with
players for setup through to the end of the game.

The `master_game_state` and `master_game_tree` fields are the source-of-truth for game interpretation in the game and use our internal representations of a `GameTree` and `GameState`. This will be constructed by the referee in the beginning of the game, and can be referenced by anyone who needs that source-of-truth throughout the game.

The `kicked_players` field keeps track of unique IDs for each player that is kicked for whatever reason from the game.

Finally, the `observers` field keeps track of a list of observers that subscribe to a Fish game. These will be observers that seek to know
information about the game and will updated by the referee after they subscribe to the game.


# Internal Methods (these are used internally by referees, not by other components):

A Referee will need some internal methods to conduct a full fish game. We will enumerate these internal methods here. These will
not be called by other components, but will be internal to the Referee component. They can be broken down into 3 phases (game set-up in which the player info is first received, round-running in which rounds of the game proceed, and end-game in which the game has reached a result) which we will split the methods up into here. These methods help to provide detail for a successful referee implementation, but an implementer need not create these methods explicity if they satisfy the external interface. 

- Game Set-Up:
	- `board_set_up(players, rows, columns)` &rarr; `Void`
		- Signature: `[(Age, PlayerID, Player)] PosInt PosInt` &rarr; `Void`
		- Purpose:  This will create holes in the board if the referee decides to and
			  will create a board with the specific number of rows and columns. After the board is set up, players
			  will be assigned colors and given the specified number of penguins and the `GameState` and `GameTree` can be in their
			  initial state and the referee can start running rounds of the game.
- Round-running:
	- `run_round()` &rarr; `Void`
		- Signature: `Void` &rarr; `Void`
		- Purpose: This will be an internal method to run one round of the Fish game. In a round a player
					   is skipped if they have no valid moves and asked for a move if not. Misbehaving players are kicked.
	- `run_placement_turn()` &rarr; `Void`
		- Signature: `Void` &rarr; `Void`
		- Purpose: This is an internal method to run a placement turn (i.e. a player placing a single penguin) for a player.
			  This will interface with the Player component to ask for a penguin placement and will either place that penguin or
			  kick a misbehaving player. 
	- `run_movement_turn()` &rarr; `Void`
		- Signature: `Void` &rarr; `Void`
		- Purpose: This is an internal method similar to the above method, but this is used after all penguins have been placed to 
			  move a single penguin for a player. This will interface with the Player component to ask for a penguin move and will
			  either move the specified penguin or will kick a misbehaving player
	- `kick_player(color)` &rarr; `Void`
		- Signature: `PlayerColor` &rarr; `Void`
		- Purpose: This internal method will kick out a misbehaving player of the given color in the game. This will interface
					   with the Tournament Manager to let them know that a player has been kicked from the game.
	- `notify_observers()` &rarr; `Void`
		- Signature: `Void` &rarr; `Void`
		- Purpose: This is a method that will interface with game observers to let them know that a move has been made or a round has been
					   played in a game of Fish. It will notify all observers.
- End-game:
	- `report_winners()` &rarr; `Void`
		- Signature: `Void` &rarr; `Void`
		- Purpose: This method will interface with the tournament manager and observers to let them know that a game is over and declare
					   the winners to them. In the case where all the players have been kicked, no winner is reported
	- `report_kicked_players()` &rarr; `Void`
		- Signature: `Void` &rarr; `Void`
		- Purpose: This method will interface with the tournament managers to report when players have been kicked.


# External Methods:

A Referee will also need some external methods that are used by external components to interface with the referee in various ways. We have broken those components down into the Tournament Manager (which runs entire tournaments of Fish), the Player (which is playing the Fish game the referee is reffing) and the observer, which observes moves happening in the game of Fish. This is the external API to which other components may call into the Referee component. 

- Used by Tournament Manager:
	- `run_game(players, row, columns)` &rarr; `GameID`
		- Signature: `[(PlayerID, Age, Player)] PosInt PosInt` &rarr; `GameID`
		- Purpose: This is the method that a Tournament Manager will use to get a Referee component to run the game.
					   It will pass in the player information needed to assign player turns and start a game as well as the row and column
					   information needed to start a game. After the Referee receives this, they should run the game and are responsible for reporting
					   back to the Tournament manager once the game is over. This will also return a GameID to the Tournament Manager which the Tournament
					   Manager could use to track the game. A `GameID` will be some unique string.
	- `check_game(game_id)` &rarr; `RefereeInfo`
		- Signature: `GameID` &rarr; `RefereeInfo`
		- Purpose: This will allow a tournament manager to check the state of a specific game. Using this method, a tournament manager will
					   get back `RefereeInfo` which is a copy of the internal information of the referee we are querying on.
- Used By Players in the Referees game:
	- `request_state()` &rarr; `GameState`
		- Signature: `Void` &rarr; `GameState`
		- Purpose: This can be used by a player in a specific game to interface with the referee to receive a deep copy 
					   of the current game state. From that, the player can strategize about the game even when it is not their turn.
	- `request_tree()` &rarr; `GameTree`
		- Signature: `Void` &rarr; `GameTree`
		- Purpose: This can be used by a player in a specific game to interface with the referee to receive a deep copy of the current
					   game tree. From that, the player can strategize about the game even when it is not their turn.
	- `check_placement(coordinate, color)` &rarr; `Boolean`
		- Signature: `Coordinate PlayerColor` &rarr; `Boolean`
		- Purpose: This can be used by a player in a specific game to see if making a placement at the given coordinate for their color would be a valid placement.
	- `check_move(move, color)` &rarr; `Boolean`
		- Signature: `Move PlayerColor` &rarr; `Boolean`
		- Purpose: This can be used by a player in a specific game to see if making a move from the given position to the given position (represented by `Move`) is valid.
- Used By Observers:
	- `subscribe_observer(observer, game_id)` &rarr; `Nonce`
		- Signature: `Observer GameID` &rarr; `Nonce`
		- Purpose: This subscribes observers to a referee to receive updates for a specific game. After using this method the observer should see turn and round updates by the Referee component. It returns a nonce (a random number of strings), so that the observer has some secure way to unsubscribe themselves.
	- `unsubscribe_observer(nonce, game_id)` &rarr; `bool`
		- Signature: `Nonce GameID` &rarr; `Boolean`
		- Purpose: This is called by an observer of the Referee to unsubscribe the observer with the given nonce for the given game if the observer no longer wishes to observe
		the game.