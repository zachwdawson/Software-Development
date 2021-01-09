import copy
from typing import List

from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.game_state import Coordinate


class PlayerInfo(object):
    """
    A PlayerInfo is {
    PenguinPositions: [Coordinate],
    NumFish: Int,
    Color: PlayerColor,
    AmountPlaceable: Int
    }
    INTERPRETATION: Represents all info you need to know about a player in a Fish game
    and NumFish is the amount of fish a player has (> 0). Color is the color of the player and PenguinPositions is
    the list of coordinates that a player has penguins at. Amount placeable is the max amount
    of penguins a player can place in a game.
    """

    def __init__(self, color: PlayerColor, amount_penguins_placeable: int):
        """
        Purpose: Initialize a PlayerInfo instance, representing internal info about
                 the player
        Signature: Int PlayerColor Int -> PlayerInfo
        :param age: Age of the player
        :param color: Color that the player has been given
        :param amount_penguins_placeable: Max amount of penguins a player can palce
        """
        self._color: PlayerColor = color
        self._penguin_posns: List[Coordinate] = []
        self._num_fish: int = 0
        self._amount_penguins_placeable = amount_penguins_placeable

    def get_fish(self) -> int:
        """
        Purpose: Get amount of fish for this player instance
        Signature: Void -> Int
        :return: the number of fish for this player instance
        """
        return self._num_fish

    def get_color(self) -> PlayerColor:
        """
        Purpose: Get color of certain player in Fish game
        Signature: Void -> PlayerColor
        :return: the color of this player instance
        """
        return self._color

    def add_fish(self, fish_amnt: int) -> None:
        """
        Purpose: Add fish for when penguin collects fish
        Signature: Int -> None
        :param fish_amnt: Amount of fish that are being added to fish total
        """
        self._num_fish += fish_amnt

    def get_penguin_posns(self) -> List[Coordinate]:
        """
        Purpose: Return the list of penguin positions for a player
        Signature: Void -> List<Coordinate>
        :return: List of positions for a given player
        """
        return copy.deepcopy(self._penguin_posns)

    def place_new_penguin(self, pos: Coordinate) -> None:
        """
        Purpose: Place a new penguin to a certain position
        Signature: Coordinate -> Void
        :param pos: Position to place penguin at
        """
        self._penguin_posns.append(pos)

    def move_penguin_at_pos(self, init_pos: Coordinate, final_pos: Coordinate) -> None:
        """
        Purpose: Move a penguin at a certain position to another position
        Signature: Coordinate Coordinate -> Void
        :param init_pos: Initial position penguin is at
        :param final_pos: Final position penguin is moved to
        """
        pos_check = self.has_penguin_at_pos(init_pos)
        if pos_check:
            penguin_index = self._penguin_posns.index(init_pos)
            self._penguin_posns[penguin_index] = final_pos

    def has_penguin_at_pos(self, pos: Coordinate) -> bool:
        """
        Purpose: Check if there is a penguin at a given position
        Signature: Coordinate -> Boolean
        :param pos: Position that you are checking if there is a penguin at
        :return: Returns a boolean representing whether there is a penguin at a given position
        """
        return pos in self._penguin_posns
