# Game Memo

## Game :

### Overview:
A game will be represented as a decision tree of all possible actions taken from all possible states. Initial state is provided and will include a finite board size, and finite number of fish, a finite number of penguins. 
Within the state, this information should be accessible and fish & penguins will already be placed.

### Representation:
  The decision tree will be composed of states as nodes and branches as actions taken from that state. This decision tree will be 
  recursive. 
  
### Action:
  A action is a structure composed of starting row & column and end row and column.
  
### External Interface:

#### Note: These are all methods within a decision tree node.

possible_states_from(player_id, starting_node): compute all possible scenarios of the game based on what the player can take

is_game_over : whether the current node has no possible actions that can be taken.

contains(node) : does the given node exist within the decision tree

path(node) : provides a path from the current node to the requested node. None is return is no path exists. 

is_valid_action(Action): from the current node, is the requested action valid.

get_possible_game_states() From a node, return all possible game states that occur from it.

simulate(policy) : traverse the decision tree using the policy. The policy can be either a list of actions or a function
that takes a node and returns an action.




