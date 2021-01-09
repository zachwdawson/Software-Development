

## Data Representation of Game States:

We shall have 4 different game states for the game of Fish: _Ref\_Removal, Player\_Init, Game\_Turns, Game\_Over_ represented by an enumeration in our program. Each of these states will have different data they need to store as well as some common data.

The game state allows for the interfacing of referees and players. It allows for players to move and place penguins and the referee to monitor these actions to ensure they conform to the rules.

We will add a factory pattern to create game states of each of the above states. This will allow for easier testing and tournament management.

Common data structures:

- PlayerColor = string of one of &quot;white&quot;, &quot;brown&quot;, &quot;red&quot;, or &quot;black&quot; as shown in Fish specification
- Coordinates = (x, y) where it is a tuple with x and y are integer coordinates >= 0. We shall use the &quot;double-height&quot; hexagon coordinate system
as shown in Fish/Planning/double_height.pdf, but any possible coordinate system could be used
- Players = [(PlayerColor, Age), …] where Age is a positive integer and list is sorted in ascending order
- Turn = PlayerColor representing which color whose turn it is
- PlayerPenguins = dictionary mapping between PlayerColor and list of Coordinates (i.e penguins[&#39;red&#39;] = [(0, 0)])

_Ref\_Removal:_

- The _Ref\_Removal_ state shall have access to the board representation. During this state, the referee may modify this board and choose to remove a list of tiles from the board using a list of the Coordinates structure

_Player\_Init:_

- The referee shall create the Players structure in the beginning of this stage and store it
- The turn for a player shall be represented by a Turn variable
- The PlayerPenguins variable shall be updated as players place their penguins on the board
- Number of penguins for each player will also be stored with the 6 – N formula in the specification

_Player\_Turn:_

- This state will save a new Turn variable for player-movement turns
- The state will also modify the PlayerPenguins variable from the _Player\_Init_ phase as players move penguins
- The board representation will also be modified as players move and tiles are removed
- A new dictionary variable will be created mapping from PlayerColor to amount of fish as a positive integer (e.g amount\_fish[&#39;red&#39;] = 10) starting at 0 fish

_Game\_Over:_

- This state will use the amount of fish dictionary to compare fish for each player and will then save a variable that is a List of PlayerColors representing the winners

## External Interface for Player/Referee:

- `remove_tile(coord)`
  - Signature: Coordinate &rarr;  Void
  - Removes tile at given x, y position (only allowed use by referee)
- `whose_turn()`
  - Signature: Void &rarr; PlayerColor
  - Returns whose turn it is (referee in setup, or player in rest of game)
- `assign_player_color(color)`
  - Signature: PlayerColor &rarr; Void
  - Add a color into a Fish game
- `place_penguin(color, coordinates)`
  - Signature: PlayerColor Coordinates &rarr; Void
  - Adds player penguin with given color to board at coordinate also handling invalid cases
- `move_penguin(color, start_coord, end_coord)`
  - Signature: PlayerColor Coordinates Coordinates &rarr; Void
  - Moves player penguin of PlayerColor from starting coordinates to ending coordinates, also handling invalid cases. Also ends a player&#39;s turn
- `get_amount_fish(color)`
  - Signature: PlayerColor &rarr; Integer>=0
  - Return the amount of fish for a certain player
- `is_game_over()`
  - Signature: Void &rarr; Boolean [PlayerColor]
  - Return a boolean representing whether the game is over and list of player color winners if true
- `get_game_representation()`
  - Signature: Void &rarr;  [Coordinates] dict<PlayerColor, Coordinate>
  - Returns a list of the tiles in the game plus a dictionary mapping from player color to the coordinates of their specific penguins