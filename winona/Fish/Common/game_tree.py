from state import *
from structures import Action
from typing import Generator, Callable, Any


class GameStateTree(object):
    """
    A Game Tree Represents a State of a game, the previous move that got to that state, and all the possible nodes that
    can be reached from a legal movement. Each of these child node's 'move_required' field can be used to determine which
    move from the current state will achieve the state of that node. Game state's allow users to get nodes one step and
    many steps away from the start node, all of which are lazily loaded. GameStateTree's also allow for actions to be
    done to states if moves are valid, otherwise an error message is returned. Lastly, GameStateTree can apply
    policies that represent strategies to all the children of a state, allowing for advanced planning.
    """

    def __init__(self, state: FishGameState, previous_action: Action = None):
        """
        Create a GameStateTree for the given state by getting all of the children node starting from this state. Save
        previous action for this state, which also acts as a next action for the children nodes.
        :param state: The GameState of this node. Used to determine all possible children from this state.
        :param previous_action: The Action that took the previous state to the current state | None if start node
        """
        self.state = state
        self.previous_action = previous_action
        self.descendants = self.get_descendants()

    def get_children(self):
        """
        Get all the nodes one step away from the state of this GameTreeNode
        :return: Generator of Nodes that are reachable one step away from the current state, allowing for the output to
        be lazily evaluated
        """
        if self.state.phase == GameStatePhase.OVER:
            return []
        actions = self.state.get_player_actions_from(self.state.current_player)
        # skip person
        if len(actions) == 0 and self.state.check_any_player_can_move():
            yield GameStateTree(self.state.skip(), self.previous_action)
        # end game if no one can move
        elif len(actions) == 0 and not self.state.check_any_player_can_move():
            yield GameStateTree(self.state.end_game(), self.previous_action)
        for action in actions:
            yield GameStateTree(self.state.move_penguin(
                color=self.state.current_player.color,
                start_row=action.start.row,
                start_col=action.start.col,
                end_row=action.end.row,
                end_col=action.end.col
            ),
                action
            )

    def get_descendants(self):
        """
        Get all the nodes at all the levels that are reachable from the current state.
        :return: Generator of GameStateTrees that allow for reachable nodes to be lazily evaluated.
        """
        for node in self.get_children():
            """
            Note:
                "Yield from" is different than normal yield in that it will iterate through the iterable
                until exhaustion before continuing on. This means, that this particular method is doing a 
                pre-order traversal of the descendents tree (We move from the left-most node -> to the right
                most node.
            """
            yield from node.get_descendants()
            yield node

    def take_action(self, action: Action) -> FishGameState:
        """
        Take Action on state in this node and return resulting state if possible.
        :param action: Action that represents the move to be tried.
        :return: Resulting GameState if move is legal, error string if the move is illegal.
        """
        is_valid, err = self.state.is_valid_move(
            color=action.player_color,
            start_row=action.start.row,
            start_col=action.start.col,
            end_row=action.end.row,
            end_col=action.end.col
        )
        if not is_valid:
            return err

        return self.state.move_penguin(
            color=action.player_color,
            start_row=action.start.row,
            start_col=action.start.col,
            end_row=action.end.row,
            end_col=action.end.col
        )

    def apply_fn_recursive(self,
                           node,
                           policy: Callable[[FishGameState], Any],
                           accumulator: List[Any]) -> List[Any]:
        """

        :param node: Start GameStateTree who's children will have the policy applied to.
        :param policy: Callable that is applied to the children of the node.
        :param accumulator: The List[Any] that accumulates the results of policy on the nodes
        :return: List[Any] that accumulates results for this node's children and all of the other children.
        """

        for next_node in node.get_children():
            accumulator = self.apply_fn_recursive(node=next_node, policy=policy, accumulator=accumulator)

        accumulator = accumulator + [policy(node.state)]

        return accumulator

    def apply_fn(self, policy: Callable[[FishGameState], Any]):
        """
        Apply the policy to the head node and all reachable nodes from head.
        :param policy: Callable that maps a FishGameState to a list of the policy's output
        :return: List[Any] representing the output of the policy on each node where Any is the same return type of the Callable
        """
        return self.apply_fn_recursive(node=self, policy=policy, accumulator=[])
