from enum import Enum


class GamePhase(Enum):
    """
    A GamePhase is a value in an enumeration
    INTERPRETATION: Represents the different phases of the Fish game.
    An explanation of what each phase is is left as a comment by each integer value in the
    enumeration
    """
    # This is the phase where players are placing their penguins initially
    PLACE_PENGUINS = 'penguin placing'
    # This is the phase where players penguins can be moved
    MOVE_PENGUINS = 'penguin moving'
    # This is the phase of the game once the game has been finished
    END_GAME = 'endgame'
