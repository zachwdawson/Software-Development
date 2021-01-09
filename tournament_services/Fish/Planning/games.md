# Data Representation of Games:

The data structure will be an n-ary tree where the parent of the tree will be the whole game and each child will be a new state of the game

It will be constructed with the following data structures:

```
GeneratedGameStateTree = {
max_depth: int
tree: GameStateTree
}
```
```
GameStateTree = { 
node: GameState
children: [GameStateTree]
turn: PlayerColor
}
```

`Coordinate = (int, int)`: where each int represents a x and y coordinate in our double-height or any hex coordinate system

`PenguinMove`: (Coordinate, Coordinate)

`PlayerColor` = Enumeration of possible player colors RED, WHITE, BLACK, and BROWN

`ChosenMoves = [PenguinMoves]`

The interpretation of the above data structure is that GameState is a construction of our game state, containing the current placement of penguins, understanding of the player order, etc. The children are either a list of other possible GameStateTrees or an empty list in the case that we are in an endgame state.

In order to get from a node to its children the GameStateTree will take in a PenguinMove which is a tuple representing a position on the board and that move can be checked to see if it creates one of the valid children of the GameStateTree.

The children of a GameStateTree will be None when there is no longer any valid moves

Once a valid move is chosen, we can safely limit our subtree to the subtree that is contained in the chosen child since all valid moves must proceed from that chosen move. However, we can keep track of the edges (PenguinMoves) chosen in the ChosenMoves data structure which gives us a record with which we could verify a game.

Due to the vastness of creating states for whole games, we have also created a GeneratedGameState object, which creates a game state to a certain depth where depth is the amount of turns that have been taken.

# External Interface:

`generate_tree_from_point(GameState state, int depth)`:

- Purpose: Generate a tree of all possible moves from some GameState from some depth, used by players for look-ahead
- Signature: GameState Int &rarr; GeneratedGameStateTree

`player_next_states(PlayerColor player_color, int rounds_ahead)`:

- Purpose: Get possible states for a player in the next round (or rounds\_ahead rounds ahead where rounds\_ahead is a positive integer, used by players for looking ahead
- Signature: PlayerColor Int &rarr; [GameState]

`is_valid_next_move(GameStateTree tree, PenguinMove move)`:

- Purpose: Check if a move is valid for the current game state configuration, used by players and refs
- Signature: GameStateTree PenguinMove &rarr; Boolean

`is_valid_list_of_moves(List[PenguinMoves] list_of_moves)`:

- Purpose: Check if a list of moves would be a valid sequence of moves, could be used by ref to check whole game or by players to try and follow a sequence of moves (i.e a whole game)
- Signature: [PenguinMove] &rarr; Boolean

`is_possible_state(GameState state)`:

- Purpose: Check if a certain state in the future is a possible state given the current state, could be used by players or by the referee
- Signature: GameState &rarr; Boolean