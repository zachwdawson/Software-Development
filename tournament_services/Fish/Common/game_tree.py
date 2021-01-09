from typing import List, Callable, Any

from Fish.Common.representations.enumerations.game_phase import GamePhase
from Fish.Common.representations.game_state import FishGameState
import copy

from Fish.Common.representations.types import Coordinate, Action

class FishGameTree(object):
    """
    A FishGameTree is: {
        state: FishGameState,
        possible_moves: [Action],
        depth: int,
        parent_action: Action | None,
        end_game_state: Boolean
    }
    INTERP: This represents a tree of all possible game states in a particular Fish game starting from a particular
    state where players can move a penguin.

    The state parameter contains the starting state for this node of this Fish game tree. This state contains all
    the pertinent information about the game (the board, the players and their penguins), which can be used to see
    at what point in the specific game we are at.

    The possible_moves parameter will contain all the moving actions for a penguin (which are moves from one coordinate
    in our coordinate system explained in FishBoardModel to another coordinate). This is how a transition will happen
    from one node to another. If there are no possible moves for a player, then they can either be in a stuck state,
    where there is a transition to a next player of the same color or the end-game state where there are no further
    transitions to be done.

    The depth parameter represents how deep this specific node is in the tree. This can be used to see how deep
    we are in a specific tree.

    The parent_action parameter represents the Action that the parent took to get to this particular
    node in the tree. This can help nodes further
    in the tree reconstruct what happened earlier in the tree.

    Finally, the end_game_state variable notes whether this node we are at is an end game state, which means a state
    where no players can make further moves.

    NOTE on Generation:

    The functions which start with generate_... in this class use a generator, which is a concept for lazy computation.
    Basically the yield statement in the functions returns objects from the function one at a time instead of returning
    a whole list at once. When using these functions you can get all the results by using a for loop, or use the
    next() function to lazily return the nodes one at a time. The generate_children and generate_children_preorder
    methods are used for generating large parts of the tree, while generate_direct_children is helpful to expand specifc
    parts of the tree.

    """

    def __init__(self, state: FishGameState, depth: int = 0,
                 parent_action: Action = None):
        """
        Purpose: Initialize a game state tree. Has a certain state and turn color plus all
                 of the turns for a certain player, also controls information about the other nodes
                 it may be related to
        Signature: FishGameState PlayerColor -> FishGameTree
        :param state: the state that we are initializing this tree with
        :param depth: How deep in the tree this node of the tree is
        :param parent_action: What action was taken by the parent to get to this node
        """
        if not state.get_game_phase() == GamePhase.MOVE_PENGUINS:
            raise ValueError('Must be in moving penguins phase')
        self.state: FishGameState = state
        self.possible_moves: List[Action] = self.find_actions()
        self.depth: int = depth
        self.parent_action = parent_action
        self.end_game_state = False
        if not self.possible_moves:
            self.end_game_state = not state.can_any_player_move()

    def generate_children(self, depth: int = 1):
        """
        Purpose: Generate children in a breadth-first-search order
        (i.e all children of depth 1, then 2, then 3 and so on). This function creates a generator object which
        can be used to retrieve the children "lazily". What this means is that this function will return an object
        that has a next method or can be used in a for loop, and will return the children one at a time, without
        trying to generate the whole tree to a certain depth. It is up to the user how many nodes they want to generate
        but it will generate as many nodes as they want in this BFS-order.
        Signature: Int -> Generator[FishGameTree]
        :param depth: How many moves down from the parent the generator should generate
        :return: A generator as described which can be used to lazily fetch nodes in breadth-first-search order.
        """
        if not self.end_game_state:
            trees_list = [self]
            next_tree_list = []
            while depth > 0:
                depth -= 1
                while trees_list:
                    tree = trees_list.pop(0)
                    if not tree.is_end_game_state():
                        for next_tree in tree.generate_direct_children():
                            yield next_tree
                            next_tree_list.append(next_tree)
                trees_list = next_tree_list
                next_tree_list = []

    def generate_children_preorder(self, depth: int = 1):
        """
        Purpose: Generate the children of a certain depth in pre-order order (left subtree than root than right subtree)
        This is a generator like the generate_children function above, which means that it lazily suspends computation
        of the next node until you call the next() method in the generator, which can also use a for-loop. This just
        uses a different way of generation than above.
        Signature: Int -> Generator[FishGameTree]
        :param depth: How many moves down from the parent the generator should generate
        :return: Generator that can return the children in pre-order order. This allows "lazy" computation and doesn't
        need to generate the whole tree at once.
        """
        if not self.end_game_state:
            if depth > 0:
                for child in self.generate_direct_children():
                    yield child
                    # yield from expands the iterator that is returned recursively
                    yield from child.generate_children_preorder(depth - 1)

    def generate_direct_children(self):
        """
        Purpose: Generate the direct children of a given tree. This creates a generator that can generate
        as many children as needed. The generator has a next() method or can be used in a for loop to get all of
        the direct children of a node. This is the preferred method if you have a specfic node path that you want to
        travel down.
        Signature: Void -> Generator[FishGameTree]
        :return: Returns a generator that can be iterated through with the next and for loop methods
                 for generating each of the direct children of a tree
        """
        if not self.end_game_state:
            if self.get_children_moves():
                for action in self.get_children_moves():
                    from_pos, to_pos = action
                    new_state = self.create_moved_state(self.state, from_pos, to_pos)
                    new_tree = FishGameTree(new_state, self.depth + 1, action)
                    yield new_tree
            else:
                new_tree = self._create_next_color_child()
                yield new_tree

    def _create_next_color_child(self):
        """
        Purpose: Create a child that has a different color for the next node in the tree, but
                 with everything else the same. This is used for "stuck" nodes, which means that a
                 player can't play so the game is over.
        Signature: Void -> FishGameTree
        :return: A new tree with the next player in the order's color but with everything else
                 the same
        """
        state_copy = self.get_state()
        state_copy.increase_turn()
        new_tree = FishGameTree(state_copy, depth=self.get_depth() + 1)
        return new_tree

    def get_children_moves(self):
        """
        Purpose: Get the successors of a FishGameTree
        Signature: Void -> List[Action]
        """
        return self.possible_moves

    def get_depth(self):
        """
        Purpose: Return the depth of this tree starting from some other state
        Signature: Void -> Int
        """
        return self.depth

    def is_end_game_state(self):
        """
        Purpose: Check if the node is in an end-game state.
        Signature: Void -> Bool
        """
        return self.end_game_state

    def get_parent_action(self):
        """
        Purpose: Return the action that got to this node from further up in the tree
        Signature: Void -> Action
        """
        return self.parent_action

    def get_state(self) -> FishGameState:
        """
        Purpose: Get a copy the state of a fish game tree
        Signature: Void -> FishGameState
        """
        return copy.deepcopy(self.state)

    def get_turn_color(self):
        """
        Purpose: Get the color of which players turn it is for this fish game tree
        Signature: Void -> PlayerColor
        """
        return self.state.get_current_turn()

    def apply_to_successors(self, apply_func: Callable[[FishGameState], Any]) -> [Any]:
        """
        Purpose: Apply a function to all successors of a certain fish game state
        Signature: (FishGameState -> X) -> [X]
        :param apply_func: Function that is applied to the successors of a certain fish game state
        :return: List of successors with the function that is passed in applied
        """
        if not isinstance(apply_func, Callable):
            raise TypeError('Must be function passed into this variable')
        direct_state = [tree.state for tree in self.generate_direct_children()]
        value_list = list(map(apply_func, direct_state))
        return value_list

    def validate_and_apply_action(self, action: Action) -> FishGameState:
        """
        Purpose: To validate an action and return a new State with the action applied.
        Signature: Action -> Optional[State]
        :param action: Action that we are checking for a given state
        :return: State if state application works, else it returns None
        """
        if action in self.possible_moves:
            from_position, to_position = action
            applied_state = self.create_moved_state(self.state, from_position, to_position)
        else:
            raise ValueError('This move cannot be made')
        return applied_state

    def validate_and_compute_node(self, action: Action):
        """
        Purpose: To validate a move and return the tree that results from validating the move.
                 This allows a tree to be expanded only along the nodes it needs to be expanded along.
        Signature: Action -> FishGameTree
        :param action: Action that we want to validate and apply to the tree to compute
                       new tree.
        """
        new_state = self.validate_and_apply_action(action)
        return FishGameTree(new_state, self.depth + 1, action)

    @staticmethod
    def create_moved_state(state: FishGameState, from_pos: Coordinate, to_pos: Coordinate) -> FishGameState:
        """
        Purpose: Create a state for moving a penguin from a given state
        Signature: FishGameState PlayerColor Coordinate Coordinate -> FishGameState
        :param state: State that we are applying move from
        :param from_pos: Coordinate we are moving penguin from
        :param to_pos: Coordinate we are moving penguin to
        :return: New state with the given penguin move applied for the given player
        """
        state_copy = copy.deepcopy(state)
        state_copy.move_penguin(state_copy.get_current_turn(), from_pos, to_pos)
        return state_copy

    def find_actions(self) -> List[Action]:
        """
        Purpose: Find the list of possible actions for a given state (i.e. movement of penguiin
                 from one state to another for a specific color)
        Signature: Void -> [Action]
        :return: List of actions for a given state, used to initialize actions for a given state
        """
        penguin_posns = self.state.get_penguins_for_player(self.state.get_current_turn())
        action_list: List[Action] = []
        if penguin_posns:
            for posn in penguin_posns:
                move_to_places = self.state.find_valid_moves_from_pos(posn)
                for place in move_to_places:
                    action = posn, place
                    action_list.append(action)
        return action_list
