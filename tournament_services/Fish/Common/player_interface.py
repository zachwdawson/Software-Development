from typing import List, Union

from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.game_state import FishGameState
from Fish.Common.representations.types import Coordinate, Action


class PlayerInterface(object):
    """
    This is a class representing an interface for a player that can be used by
    the referee to communicate with the player. There is no formal interface keyword in python
    so this contains method stubs that just "pass" or do nothing until the interface is implemented
    """

    def assign_color(self, color: PlayerColor) -> bool:
        """
        Purpose: This method will assign a player a color from the referee
                 This is to initialize the player with a certain color at the beginning of the game,
                 so the player knows what color it is playing as.
        Signature: PlayerColor -> Void
        This will do some initialization inside each player that assigns the player that color
        """
        raise NotImplemented

    def show_other_players_colors(self, colors: List[PlayerColor]) -> bool:
        """
        Purpose: This will show the player the color of all of the other players in the game.
                 This is so it can keep track of how many and which players are in the game.
                 This may be called be the ref multiple times if a player is kicked from
                 the game to give the player the necessary information to make a move
        Signature: List[PlayerColor] -> Void
        """
        raise NotImplemented

    def player_place_penguin(self, state: FishGameState) -> Union[Coordinate, bool]:
        """
        Purpose: This method informs a player about the current state of the board and
                 where penguins have been placed and then waits to receive a coordinate
                 representing where the player wants to place a given penguin.
        Signature: FishBoardModel List[Coordinate] -> Coordinate
        :param state: A copy of the state which contains the info needed for the player
                      about the board and about the players and their penguins on the board.
                      This gives the player enough information to find a coordinate to place a penguin.
                      Modifying this state will not modify the actual state of the game.
        :return: A player coordinate for where the given player wants to place their next penguin
        """
        raise NotImplemented

    def player_move_penguin(self, state: FishGameState) -> Union[Action, bool]:
        """
        Purpose: This method informs a player about the current state of the board
                 and checks to see what move the player communicates back
        Signature: FishBoardModel List[Coordinates] -> Action
        :param state: A copy of the state which contains the info needed for the player
                      about the board and about the players and their penguins on the board.
                      This gives the player enough information to find a coordinate to move a penguin.
                      Modifying this state will not modify the actual state of the game.
        :return: An Action which is a tuple of coordinates representing a move of a penguin
                 from one position to another that the player is returning to the referee
        """
        raise NotImplemented

    def inform_of_winners(self, winners: List[PlayerColor]) -> bool:
        """
        Purpose: This method informs a player about the winners of a game of Fish after that game is over.
                 Multiple players could have the same amount of Fish so the winners is a list. The player can save
                 this internally
        Signature: List[PlayerColor] -> Void
        :param winners: The list of winners for a current game of Fish
        """
        raise NotImplemented

    def start(self) -> bool:
        raise NotImplemented

    def end(self, is_winner: bool) -> bool:
        raise NotImplemented

    def receive_message(self, message: str, message_id: int) -> bool:
        """
        Purpose: Accept a message and awknowledge that the message has been accepted
        """
        raise NotImplemented
