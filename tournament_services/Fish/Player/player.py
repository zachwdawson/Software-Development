from typing import List

from Fish.Common.representations.types import Action
from Fish.Common.player_interface import PlayerInterface
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.game_state import FishGameState
from Fish.Common.representations.types import Coordinate
from Fish.Player.strategy import FishBasicStrategy


class BasicPlayer(PlayerInterface):
    """
    Class that implements a Player Interface, using the basic strategy defined in strategy.py.
    This strategy we have defined uses a basic penguin-placing algorithm as well as a basic maximin
    algorithm that we have defined. This class basically just reuses that strategy to be able
    to execute moves.
    """
    def __init__(self, depth=1, name=None):
        """
        Purpose: Initialize basic parameters of this player. such as Color, other players color,
        winners and the strategy. Note that for now, we are doing the maximin at a depth of 1
        in order to run quick games, but may switch to using different depths in the future.
        This component may need to encode other things such as a players age in the future, but
        we are not sure of that yet, so we are leaving it out of the implementation for now.
        """
        self.color = None
        self.other_colors = []
        self.winners = []
        self.strategy = FishBasicStrategy(depth)
        self.name = name
        self.started = False
        self.finished = False

    def assign_color(self, color: PlayerColor) -> bool:
        self.color = color
        return True

    def player_place_penguin(self, state: FishGameState) -> Coordinate:
        coordinate = self.strategy.find_next_placement(state)
        return coordinate

    def player_move_penguin(self, state: FishGameState) -> Action:
        action = self.strategy.find_next_move(state)
        return action

    def show_other_players_colors(self, colors: List[PlayerColor]) -> bool:
        self.other_colors = colors
        return True

    def inform_of_winners(self, winners: List[PlayerColor]) -> bool:
        self.winners = winners
        return True

    def start(self) -> bool:
        self.started = True
        return True

    def end(self, is_winner: bool) -> bool:
        self.finished = True
        return True

    def receive_message(self, message: str, message_id: int) -> bool:
        #TODO message will be delivered to user through the communication layer
        #print('Message Received: ', message)
        return True
