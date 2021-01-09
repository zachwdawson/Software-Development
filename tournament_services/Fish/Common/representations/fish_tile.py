class FishTile(object):
    """
    Class representing a single tile in the game Fish
    """

    # maximum amount of fish allowed on 1 tile
    MAX_AMOUNT_FISH = 5

    def __init__(self, num_fish: int = MAX_AMOUNT_FISH):
        """
        Purpose: Initialize a FishGameTile with a number of fish
        Signature: Int -> FishTile
        :param num_fish: amount of fish on a tile (must be a positive natural number > 0)
        :return: an instance of a FishTile
        """
        self.num_fish = num_fish

    @property
    def num_fish(self) -> int:
        """
        Purpose: Return the amount of fish on a tile
        Signature: Void -> Int
        :return: returns the amount of fish on a give tile
        """
        return self.__num_fish

    @num_fish.setter
    def num_fish(self, value: int) -> None:
        """
        Purpose: Sets the amount of fish on 1 tile
        Signature: Any -> Void
        :param value: Value that you are trying to set number of fish too
        :return: Sets the number of fish in the FishTIle object or throws Type or ValueError on incorrect input.
        """
        if not isinstance(value, int):
            raise TypeError('Number of fish must be an integer')
        if value <= 0:
            raise ValueError('Number of fish must be > 0 for a tile')
        if value > FishTile.MAX_AMOUNT_FISH:
            raise ValueError('Number of fish must be <= the max amount of fish')
        else:
            self.__num_fish = value
