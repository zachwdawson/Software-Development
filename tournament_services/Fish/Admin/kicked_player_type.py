from enum import Enum


class KickedPlayerType(Enum):
    """
    This is an enumeration noting the type of players that have been kicked by our
    referee in a Fish game. We differentiate between CHEATING players (those who have made a move
    that is wrong due to the logic of the game) and FAILING players (those whole fail
    to produce well-formed input to the referee)
    """
    CHEATING = 'cheating'
    FAILING = 'failing'
