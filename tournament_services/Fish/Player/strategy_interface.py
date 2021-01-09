from Fish.Common.game_tree import Action
from Fish.Common.representations.game_state import FishGameState
from Fish.Common.representations.types import Coordinate


class StrategyInterface(object):
    """
    This is class representing an interface for a Strategy that can be used by player to execute actions within a game
    of Fish. The find_next_placement method is for the initial phase and is for producing a valid position to place a penguin,
    while the find_next_move method is for producing a valid action of moving a penguin.
    """
    def find_next_move(self, state: FishGameState) -> Action:
        """
        Purpose: To find a next move for the player whose current turn it is in the given state. This assumes that
        the state will never be passed to be skipped (it will always be a valid move).
        Signature: FishGameState -> Action
        """
        raise NotImplemented

    def find_next_placement(self, state: FishGameState) -> Coordinate:
        """
        Purpose: To find the next valid placement for a player whose turn it is to place a penguin in the given state.
        Signature: FishGameState -> Coordinate
        """
        raise NotImplemented

