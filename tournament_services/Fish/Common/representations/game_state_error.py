
class GameStateError(Exception):
    """
    This is an error class representing errors that can happen when moves happen on a game state, which
    is a players penguin being placed and a player moving a penguin. This captures that logical error
    in a more specific sense than just throwing a ValueError
    """
    pass


class PenguinMovementError(GameStateError):
    """
    This is an error class that represents the set of errors that can happen when a player tries to
    move a penguin from one spot on the board to another, but cannot (another penguin is where they want to go,
    they have no penguin at the initial spot, etc.), because the action cannot be executed legally.
    """
    pass


class PenguinPlacementError(GameStateError):
    """
    This is an error class that represents the set of errors that can happen when a player tries to
    place a penguin on a spot on the board, but cannot (another penguin is at that spot,
    spot is not on the board, etc.), because the action cannot be executed legally.
    """
    pass
