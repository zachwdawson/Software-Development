# Game State Memo

## Game State:

### Tiles
Game state would require us to keep track of the most important aspects of a single game. One of if not the most important part of a game of Fish is the board. The board contains a two dimensional array of tiles, each of which keeping track of its own state. A tiles state includes row, column, whether or not it is a hole, the number of fish, maximum number of fish possible, and its neighbors that are directly adjacent to it on all six sides.

### Players
Another major piece of any game is the players in the game. The important pieces of data for a player are a player id, locations of the player’s penguins within the board (represented as an array of row and column tuples), the age of the player, and the number of fish it has collected.

### Miscellaneous
There are other values that would be necessary to run a game properly. These include whose turn it is (represented by a player id), the maximum number of fish on a tile, a game id,  and potentially the money to be awarded to the winner.

### Representation
The way we will be representing the tiles is a two dimensional array of named tuples. Named tuples allows us to easily serialize to JSON as well as have the opportunity to use linting to ensure certain data types are being passed. This same approach will be taken for the array of players. This will allow for easily readable and transferable data when we incorporate a server client interaction later on down the road.


## External Interface:

get_game_state(): Will return a serialized game state as described above. This will provide the players or referees with all the necessary information about the state of a game.

move_penguin(r1,c1,r2,c2, player_id): Will allow player with player id = player_id to make a move from tile 1 to tile 2 if the given move is valid. This will call on the get_reahable_tiles method that was previously defined.

collect_fish(row, col, player_id): Remove fish from tile at (row, column) and award the fish to the player with player_id.
remove_tile(row,col): Remove tile at (row, column), turning it into a hole.

add_fish(row, col, number_fish): Potentially useful for the refere to add fish to a specific tile. Obviously inaccessible to the players.

tile_has_valid_move(row, column): Check to see if the tile at (row, column) has a valid move within this board.

player_has_valid_move(player_id): check all of the player’s penguins locations to see if that player can make a valid move, if false this player is out of the game.

is_game_over(): Check all of the players within the game to see if any can make a move, if none can the game is over.
