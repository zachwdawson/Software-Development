from Fish.Common.representations.enumerations.player_color_enum import PlayerColor


class FishAvatar(object):
    """Class representing a fish avatar"""

    def __init__(self, color):
        """
        Purpose:Initialize a fish avatar of a certain color
        Signature: PlayerColor -> FishAvatar
        :param color: Color to create the player avatar with
        :return: instance of a FishAvatar
        """
        self.color = color

    @property
    def color(self):
        """
        Purpose: Get the color of a Fish avatar
        Signature: Void -> PlayerColor
        :return: a player color string
        """
        return self.__color

    @color.setter
    def color(self, value):
        """
        Purpose: Set color of a Fish avatar
        Signature: Any -> Void
        :param value: value you are trying to set the color value to
        :return: Sets the player color
        """
        if value not in {PlayerColor.BLACK, PlayerColor.BROWN, PlayerColor.WHITE, PlayerColor.RED}:
            raise ValueError('Color must be one of black, brown, white or red')
        self.__color = value
