# annettasouth

The overall purpose of this project is to develop a full implementation of a Fish Dot Game, from running individual
games to building a whole remote tournament system for the game that plugs AI players into it. For now, the basic
pieces of the game (board, tile, avatars) have been developed as well as a game state representation combining
those components. We also have developed a game tree representation of the game as well as some player
strategy components and a referee to run the games.

## Directory Structure

In the `Planning` folder, it contains a number of files. We will list them in order of milestone:
1. Our milestones and system overview (in `milestone.pdf` and `system.pdf` respectively).
2. The `game-state.md` specification of game states, as well as our self-written explanation of coordinates
`double_height.pdf`.
3. `games.md` specification of games
4. `player-protocol.md` and `protocol.PNG` which spell out our player_protocol and 
contain a picture of the protocol.
5. `referee.md`, which is our specification of referees . 
6. `manager-protocol.md` contains our tournament manager specification and uses the image files `xxx_tourney_manager.png`
where xxx is a different components email.

Now we will break down each other folder that actually contains the code for our implementation

- In the `Common` folder it contains our code for all of the representations of the common ontology of the game.
    
    - In the `unit_test` folder it contains our various unit_tests for different pieces of the game we have built
        - `avatar_unit_test.py, board_test.py, pieces_view_test.py and tile_test.py` test the boards and the tiles
        - `create_state_test.py, game_state_test.py, player_info.py` test our game state representation
        - `game_tree_test.py` tests our implementation of a game tree.
    - On the top level of `Common/` it also contains the `board.PP (board.py)` and `state.PP (state.py)` files which inform
      you where to find our board and state representations respectively, which is in the representations folder explained below.
    - The `representations` folder contain the actual data representations for pieces of a fish game, up to and including
      the pieces created for Milestone 3 (game state):
        - On the top level of this folder, `fish_board.py`, `fish_tile.py` and `fish_avatar.py` are data representations
          of the board, tile and avatar in a Fish game. Boards contain tiles. The avatar class is currently only used
          to draw avatars and may be removed soon.
        - Also on the top level of this folder `game_state.py` and `player_info.py `contain the representations for a game state and internal
          player data for those game state. A game state contains a board which has tiles. It also contains info about players and turns. 
          `game_error.py` contains the logical errors that can be thrown from a game state.
        - Misc Files:
            - `types.py` contain type definitions that are used throughout our representations
            - In the `/enumerations` folder, `directions_enum.py`, `player_color_enum.py`, and `game_phase.py` represent enumerations
              for directions on a hex board and player colors and game phase respectively. Directions are used
              in the board and game state representation and player color and game phase are used in teh game
              state representation.
    - On the top level of `Common/` it contains the `game_tree.PP (game_tree.py)` which contains our representation
      of a game tree, which uses game states to create trees of legal moves and of a whole game.
    - It also contains `player_interface.py` which spells out our player interface for players of the Fish game 
      to implement.
    - In the `views/` folder, it contains our `pieces_view.py` file as well as our `state_view.py` file for visually rendering
      the board representation and the state representation
    - In the `demonstration` folder it contains a python file that will demonstrate drawing the board.
      It also contains a Python script to demonstrate drawing the board state.

- In the `Player` folder, it contains our code related to player components.
    - `strategy.py`contains our implementation of a strategy component. This will find
      moves that a player can execute. It is an implementation of the `strategy_interface.py` we have defined in
      the same folder.
    - `player.py` contains an implementation of the a player using the interface from `Common` and the strategies
      defined in `strategy.py`
    - The `unit_test` folder contains our unit tests for the player component, including tests for the
      strategy and our player implementation.

- In the `Admin` folder we have the code related to administrators of games such as the referee and tournament managers.
    - `referee.py` contains our implementation of a referee, which use game states and trees to do rule-checking
    for a passed in list of players that we run a game for. It uses the error class `runtime_error.py` for custom
    errors that the class uses and the `kicked_player_type.py` file for an enumeration for player type.
    - `manager_interface.py` contains our interface for the tournament manager.
    - `unit_test` as contains our tests for the referee.

The `Other/` folder contains one file for code that translates between the integration test data definitions and
our internal data definitions.

Finally `xtest` on the top level of `Fish/` also represents a script that can
be run to run all of our unit tests for our codebase.


## Testing the code

For running our unit tests in Fish, cd to the Fish/ top-level folder and run
the script `xtest` with the command:

`./xtest`

You can also go into the unit_test folder inside `Common/` or `Player/` or `Admin`
and run each individual group of tests in the folder with this command:

`python3 -m unittest {file_name}`

### Test Harness Tests

To run unit tests for translating our test harness for milestone 3, navigate into 
~/3/Other with cd and run the following command:

`python3 -m unittest test_xboard.py`

Similarly, to run unit tests for translating our test harness for milestone 4, navigate into 
~/4/Other with cd and run the following command

`python3 -m unittest test_xstate.py`

Similarly, to run unit tests for translating our test harness for milestone 4, navigate into 
~/5/Other with cd and run the following command

`python3 -m unittest test_xtree.py`

For the 6th milestone, the harness covered code that we had already tested in our internal representation and was
a trivial transformation, so there is only a `Tests/` and `xstrategy` file.

### Visual Demonstrations

To run our demonstration of the visual representation of the board, navigate
to Fish/Common/demonstration (using the cd command) amd run the following command:

`python3 board_view_demo.py`

To see our state representation, be in the same directory and run:

`python3 state_view_demo.py`
