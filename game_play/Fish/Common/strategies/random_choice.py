from game_tree import GameStateTree
from state import FishGameState
from random import choice


class RandomChoice(object):

    def __init__(self, tree: GameStateTree):
        self.decision_tree = tree
        self.current_player = self.decision_tree.state.current_player

    def build_policy(self):
        def random_choice(s: FishGameState) -> GameStateTree:
            if s.current_player != self.current_player:
                raise ValueError("Not current players turn...")

            selected_action = choice(s.get_player_actions_from(s.current_player))
            return GameStateTree(
                state=s.move_penguin(
                    color=self.current_player.color,
                    start_row=selected_action.start.row,
                    start_col=selected_action.start.col,
                    end_row=selected_action.end.row,
                    end_col=selected_action.end.col)
            )

        return random_choice
