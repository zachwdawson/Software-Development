from typing import Tuple, Any

"""
A coordinate is an x, y tuple representing a coordinate in a double-height system,
where x is the amount of tiles the tile is over to the right and y is the amount of
tiles this coordinate is going downward. Look at double-height.pdf in the Planning
folder to see discrete examples and explanation of this coordinate system.
"""
Coordinate = Tuple[int, int]


def coordinate_type_check(val: Any) -> bool:
    """
    Purpose: Takes in a value and sees if this value is of our self-defined coordinate type
    Signature: Any -> Boolean
    """
    is_coordinate = False
    if isinstance(val, tuple):
        if len(val) == 2:
            column, row = val
            if isinstance(column, int) and isinstance(row, int):
                is_coordinate = True
    return is_coordinate


"""
An Action is (Coordinate, Coordinate)
INTERP: Action is a tuple of 2 coordinates from one penguin position 
        to another penguin position. This represents a possible action that can be taken in a game state.
"""
Action = Tuple[Coordinate, Coordinate]


def action_type_check(val: Any) -> bool:
    """
    Purpose: Takes in a value and sees if this value is of our self-defined Action type.
    Signature: Any -> Boolean
    """
    is_action = False
    if isinstance(val, tuple):
        if len(val) == 2:
            from_coord, to_cord = val
            if coordinate_type_check(from_coord) and coordinate_type_check(to_cord):
                is_action = True
    return is_action
