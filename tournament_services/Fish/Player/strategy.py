from typing import List

from Fish.Common.representations.types import Action
from Fish.Common.game_tree import FishGameTree
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.game_state import FishGameState
from Fish.Common.representations.types import Coordinate
from Fish.Player.strategy_interface import StrategyInterface


class FishBasicStrategy(StrategyInterface):
    """
    This is a helper class for strategy that helps to find a strategy for penguin placement and
    movement for a player. This is an implementation of our overall strategy interface which has two methods: find_next_move and
    find_next_placement. These methods both take in a state and produce the desired result for a player trying to make a move.

    For placing a penguin find_next_placement returns
    a coordinate, which is represented as a Coordinate in our internal data representation.

    For moving a penguin, find_next_move returns an action, which consists of a move from one coordinate
    to another coordinate.

    Together, using these two methods a Fish player could play a whole entire game.
    """

    def __init__(self, look_ahead_turns: int):
        """
        Purpose:
        Signature: -> FishStrategy
        :param look_ahead_turns: The amount of turns we want to look ahead for a certain player
        """
        self.look_ahead_turns = look_ahead_turns

    def find_next_move(self, state: FishGameState) -> Action:
        """
        Purpose: Find best move for player whose turn it is in the current state
        after going N turns ahead for that player in the current turn, or as many possible.
        This assumes that a player using this will have at least 1 possible move on their
        turn. This holds because the referee would never ask for a move for a player who
        has a turn skipped. N turns ahead means that we will look at the current players moves for that many
        turns ahead. We could, and in some cases should look at their opponents move for that final turn where
        turn=N, but for this particular maximin evaluation we only have to look to the depth where the player
        we are checking has made their Nth move and not look at their opponents moves also.

        This is because the evaluation function only checks the amount of fish that the maximizing player has, which means that
        the opponents moves in the Nth round cannot impact the amount of fish that the strategizing player has,
        and thus is wasted computation. If we had another maximin evaluation function that took into account other
        factors that could change turn-by-turn, we would also checks the opponents moves in the Nth round.
        Signature: FishGameState Int -> Action
        :param state: The state for which we are looking for a move. This state includes the current
                      turn so we know which player to look for
        :return: The action representing a from and to position that is the player best
                 move according to the maximin algorithm
        """
        game_tree = FishGameTree(state=state)
        max_value = float("-inf")
        best_children = []
        for child in game_tree.generate_direct_children():
            # we have already gone one turn down, so
            # depth is amount of players there are * the number of turns - 1
            depth = (self.look_ahead_turns - 1) * len(state.get_player_order())
            minimax_value = FishBasicStrategy._find_maximin_value(child, False,
                                                                  depth,
                                                                  game_tree.get_turn_color())
            if minimax_value > max_value:
                best_children = [child]
                max_value = minimax_value
            elif minimax_value == max_value:
                best_children.append(child)
        if len(best_children) == 1:
            best_action = best_children[0].parent_action
        else:
            best_action = FishBasicStrategy._break_ties([tree.get_parent_action() for tree in best_children])
        return best_action


    @staticmethod
    def _break_ties(best_actions: List[Action]) -> Action:
        """
        Purpose: Run tiebreaker from lowest row and lowest column for from position
                 to lowest row and column for to position
        Signature: List[Action] -> Action
        :param best_actions: List of all possible actions a player could take that
                             are considered best by the maximin algorithm
        :return: The action (using tiebreaker criteria) that the player should take
        """

        from_pos_list = [from_pos for from_pos, to_pos in best_actions]
        sorted_from_pos = sorted(from_pos_list, key=lambda position: (position[1], position[0]))
        best_from_posns = [(from_pos, to_pos) for from_pos, to_pos in best_actions if from_pos == sorted_from_pos[0]]
        if len(best_from_posns) == 1:
            return best_from_posns[0]
        else:
            to_pos_list = [to_pos for from_pos, to_pos in best_from_posns]
            sorted_to_pos = sorted(to_pos_list, key=lambda position: (position[1], position[0]))
            return [(from_pos, to_pos) for from_pos, to_pos in best_actions if to_pos == sorted_to_pos[0]
                    and from_pos == sorted_from_pos[0]][0]

    @staticmethod
    def _find_maximin_value(tree: FishGameTree, maximizing_player: bool, depth: int,
                            maximizing_player_color: PlayerColor) -> int:
        """
        Purpose: Find the maximin value for a certain game tree to a certain depth.
                 This maximizes the amount of fish when a the player whose turn it is is playing
                 and minimizes the amount of fish with its moves when all other players are playing,
        Signature: FishGameTree Bool Int PlayerColor -> Int
        :param tree: The tree which we are searching for the best moves on for a certain player
        :param maximizing_player: Whether it is the maximizing players turn
        :param depth: How many nodes down in the tree we have to go before returning the value
        :param maximizing_player_color: The color of the player who is trying to maximize their value
        :return: Returns an integer representing the maximum value that a player is guaranteed to get
                 from that position in the tree
        """
        # if we have gone N turns or hit an end game state
        if depth == 0 or tree.is_end_game_state():
            return tree.get_state().get_fish_for_player(maximizing_player_color)

        if maximizing_player:
            compare_val = float("-inf")
            compare_func = max
        else:
            compare_val = float("inf")
            compare_func = min

        for child in tree.generate_direct_children():
            maximizing_player = child.get_turn_color() == maximizing_player_color
            compare_val = compare_func(compare_val, FishBasicStrategy._find_maximin_value(
                child, maximizing_player, depth - 1, maximizing_player_color
            ))
        return compare_val

    def find_next_placement(self, state: FishGameState) -> Coordinate:
        """
        Purpose: To find the next valid coordinate where a player can place a penguin, going left to right on the board
        rows
        Signature: FishGameState -> Coordinate
        :param state: The current state of the game
        :return: Coordinate representing a position where a penguin can be placed
        """
        board = state.get_board()
        sorted_coords = board.get_coords_sorted_by_row()
        for coord in sorted_coords:
            if not FishBasicStrategy._any_player_has_penguin(state, coord):
                return coord
        raise ValueError("Board cannot accommodate all penguins.")

    @staticmethod
    def _any_player_has_penguin(state: FishGameState, coord: Coordinate) -> bool:
        """
        Purpose: To check if any of the players have a penguin on a given valid coordinate on the board
        Signature: FishGameState Coordinate -> Boolean
        :param state: The current state of the game
        :param coord: A valid coordinate on the board in the state
        :return: Boolean representing if any of the players have a penguin in the given coord
        """
        for player in state.get_player_order():
            penguins = state.get_penguins_for_player(player)
            if penguins:
                if coord in penguins:
                    return True
        return False


