from game_tree import GameStateTree
from state import FishGameState
from math import inf
from structures import Player, Action, GameStatePhase, Coordinate
from typing import Tuple, List

"""
This file provides the functionality for strategy within a game of Fish. This functionality includes placing penguins
in a zig-zag pattern that starts in the top left corner and moves down each row in the given states board. It also
allows a user to move the penguin based on a minimal maximum score strategy, where the given state maximizes the 
score of the current player while assuming the others will attempt to minimize this player's score.
"""


class GenericStrategyComponent(object):
    """
    A simple strategy component for deciding how to place / move penguins.
    Placing is done by placing its penguin in the first available place
    in a zig-zag pattern. A movement is decided by selecting an action that
    maximizes the score of the the worse case scenario.
    """

    @staticmethod
    def place_penguin(state: FishGameState) -> Coordinate:
        """
        Place a penguin in the next available place in the given state's board according to a zig-zag pattern that begins
        in the top left corner.
        :param state: The state that will have penguins added to it.
        :return: The updated state after adding the penguin in the correct place.
        """
        for r, row in enumerate(state.board.board):
            for c, col in enumerate(row):
                if state.validate_input(state.current_player.color, r, c)[0]:
                    return Coordinate(r, c)

        raise ValueError("No available tiles for penguin placement.")

    @staticmethod
    def choose_action(tree: GameStateTree, num_turns: int = inf) -> Action:
        """
        Choose the optimal action for the current player of the given state considering the next n turns. The optimal action
        is defined as the action that offers the best gain after N turns is the highest score a player can make
        after playing the specified number of turns—assuming that all opponents pick one of the moves that minimizes
        the player’s gain
        :param tree: The current tree of the game
        :param num_turns: Optional amount of turns to look ahead when deciding which turn to use.
        :return: The updated state after making the move that was decided upon with the decision algorithm.
        """
        maximizing_player = tree.state.current_player
        optimal_move = GenericStrategyComponent.minimax(tree, num_turns, maximizing_player)[1]
        return optimal_move

    @staticmethod
    def choose_action_from_state(state: FishGameState, num_turns: int = inf) -> Action:
        """
        Similar to choose_action with the exception that rather than taking a tree, it takes in a state.
        :param state: The current state of the game
        :param num_turns: Optional amount of turns to look ahead when deciding which turn to use.
        :return: The updated state after making the move that was decided upon with the decision algorithm.
        """
        tree = GameStateTree(state=state)
        return GenericStrategyComponent.choose_action(tree=tree, num_turns=num_turns)

    @staticmethod
    def minimax(tree: GameStateTree, num_rounds: int, maximizing_player: Player) -> Tuple[int, Action]:
        """
        Called recursively on various nodes of the GameStateTree to determine the maximum move for the maximizing player
        and the minimizing move for any player that is not the maximizing player.
        :param tree: The game state tree that will be examined to determine the optimal moves.
        :param num_rounds: The number of rounds each player will play within the decision algorithm
        :param maximizing_player: The player that is being maximized, all other players will attempt to minimize this player.
        :return: The Tuple(optimal_score, optimal_action) that will take place in this round of the minimax algorithm.
        """

        if num_rounds == 0 and tree.state.current_player.color == maximizing_player.color:
            return tree.state.current_player.score, tree.previous_action
        elif tree.state.phase == GameStatePhase.OVER and tree.state.current_player.color == maximizing_player.color:
            return tree.state.current_player.score, tree.previous_action
            # if we reach the end and it is the maximizing players turn return the maximizing players score
        elif tree.state.phase == GameStatePhase.OVER and tree.state.current_player.color != maximizing_player.color:
            return -inf, None
            # if we reach the end and it is not the maximizing players turn return the -inf so
            # the next node up the chain will be greater than it
        elif tree.state.current_player.color == maximizing_player.color:  # maximize this player
            children = [child for child in tree.get_children()]
            return GenericStrategyComponent.handle_maximum(
                children=children, num_rounds=num_rounds, maximizing_player=maximizing_player)
        elif tree.state.current_player.color != maximizing_player.color:
            # minimize the maximizing player for all other player
            children = [child for child in tree.get_children()]
            return GenericStrategyComponent.handle_minimum(
                children=children, num_rounds=num_rounds, maximizing_player=maximizing_player)

    @staticmethod
    def handle_maximum(children: List[GameStateTree], num_rounds: int, maximizing_player: Player):
        """
        Find the maximal possible move in the given list of children for the maximizing player.
        :param children: List of GameStateTree to explore for potential maximum moves
        :param num_rounds: The number of moves down to explore in each of the children.
        :param maximizing_player: The player that is being maximized
        :return:
        """
        value = -inf
        max_child = None
        matching_outcomes = []
        for child in children:

            if max_child is None:
                max_child = child

            minimax_value, _ = GenericStrategyComponent.minimax(child, num_rounds - 1, maximizing_player)

            if minimax_value == value:
                matching_outcomes.append(child)
            elif minimax_value > value:
                matching_outcomes = [child]
                max_child = child

            value = max(minimax_value, value)

        optimal_move = GenericStrategyComponent.break_tie(matching_outcomes) if len(matching_outcomes) > 1 else max_child.previous_action

        return value, optimal_move

    @staticmethod
    def handle_minimum(children: List[GameStateTree], num_rounds: int, maximizing_player: Player):
        """
        Find the minimal possible move in the given list of children that is minimizing for the maximizing player.
        :param children: List of GameStateTree to explore for potential maximum moves
        :param num_rounds: The number of moves down to explore in each of the children.
        :param maximizing_player: The player that is being maximized
        :return:
        """
        value = inf
        min_child = None
        matching_outcomes = []
        for child in children:

            if min_child is None:
                min_child = child

            minimax_value, _ = GenericStrategyComponent.minimax(child, num_rounds, maximizing_player)
            if minimax_value == value:
                matching_outcomes.append(child)
            elif minimax_value < value:
                matching_outcomes = [child]
                min_child = child

            value = min(minimax_value, value)

        return value, None

    @staticmethod
    def break_tie(matching_outcomes: List[Action]):
        """
        If multiple actions can be taken that are considered to be 'optimal' return the move for the penguin that has the
        lowest row number for the place from which the penguin is moved and, within this row, the lowest column number.
        In case this still leaves the algorithm with more than one choice, the process is repeated for the target
         field to which the penguins will move.
        :param matching_outcomes: The list of moves that the minimax algorithm determined to be optimal.
        :return: The action that is decided upon by the previously described rules.
        """
        best_action: Action = matching_outcomes[0].previous_action
        for outcome in matching_outcomes[1:]:
            # if the new outcome's row is less than the previous best, update to this outcome
            if outcome.previous_action.start.row < best_action.start.row:
                best_action = outcome.previous_action
                continue
                # if they have the same row check col
            elif best_action.start.row == outcome.previous_action.start.row:
                # if the new outcome has lower col update best_action
                if outcome.previous_action.start.col < best_action.start.col:
                    best_action = outcome.previous_action
                    continue
                    # if they have the same row and col check end
                elif outcome.previous_action.start.col == best_action.start.col:
                    # if the new outcome has a lower end row update
                    if outcome.previous_action.end.row < best_action.end.row:
                        best_action = outcome.previous_action
                        continue
                        # if they have the same end row and the new outcome has a lower col update
                    elif outcome.previous_action.end.row == best_action.end.row and \
                            outcome.previous_action.end.col < best_action.end.col:
                        best_action = outcome.previous_action
                        continue

        return best_action
