from Common.state import FishGameState
from Player.strategy import GenericStrategyComponent


class PlayerComponent(object):

    def __init__(self, strategy=None):
        """
        A PlayerComponent implements a given strategy and is interacted with
        by the referee.
        """
        self.strategy = strategy if strategy is not None else GenericStrategyComponent()
        self.is_game_over = False
        self.is_kicked = False
        self.is_winner = False

    def get_penguin_placement(self, state: FishGameState):
        """
        Computes the placement to be taken on the given fish game state.
        :param state: the current fish game state.
        :return: A Coordinate to place the penguin.
        """
        return self.strategy.place_penguin(state=state)

    def get_penguin_movement(self, state: FishGameState):
        """
        Computes the action to be taken from the fish game state.
        :param state: the current fish game state.
        :return: An action to be taken.
        """
        return self.strategy.choose_action_from_state(state=state)

    def notify_game_over(self):
        """
        Handles the scenario in which the game is said to be over.
        """
        self.is_game_over = True

    def notify_kicked(self):
        """
        Handles the scenario in which the player is kicked.
        """
        self.is_kicked = True

    def notify_winner(self):
        """
        Handles the scenario in which the game is said to be over and is a winner.
        """
        self.is_winner = True
