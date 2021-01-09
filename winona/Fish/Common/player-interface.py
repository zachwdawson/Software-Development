from state import FishGameState, FishGameStateFactory
from typing import List
from structures import Action

#-----------------Auth------------------

def join_tournament(tournament_id, credit_card) -> dict:
    """
    Join the tournament with the given id and pay the entry fee with the given credit card.
    :param tournament_id: Integer tournament_id that will be joined.
    :param credit_card: Credit card that will be used to pay the entry fee.
    :return: Dictionary with players SHA token and color for this game.
    """
    NotImplemented

#-----------------Game Play-------------

def check_placement(user_token: str, row: int, col: int) -> bool:
    """
    Check whether or not the placement if valid for the player with this user_token. Must check that it is this users
    turn and that the tile is not already occupied, out of bounds, or a hole.
    :param user_token: SHA token that authenticates the user's identity
    :param row: The desired row for penguin placement
    :param col: The desired col for penguin placement
    :return: True if the placement is possible, false otherwise.
    """
    NotImplemented

def place_penguin(user_token: str, row: int, col: int) -> FishGameStateFactory:
    """
    Place the penguin for the user with this token at the given row and column. If the placement is invalid, kick this players
    penguin.
    :param user_token: SHA token that authenticates the user's identity
    :param row: The desired row for penguin placement
    :param col: The desired col for penguin placement
    :return: The updated state of the game after adding the placement of this game | an error string for invalid placements
    """
    NotImplemented


def check_move(user_token: str, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
    """
    Check whether the move from (start_row, start_col) to (end_row, end_col) is valid. Return true if the movement is
    possible, false otherwise. Moves are invalid if the start coordinate or end coordinate is outside the bounds or the
    board or is a hole. Moves are also invalid if they attempt to play out of turn, jump a hole, or jump a penguin.
    :param user_token: The user token of the player checking the move.
    :param start_row: The row of the penguin before the move.
    :param start_col: The col of the penguin before the move.
    :param end_row: The row of the penguin after the move.
    :param end_col: The col of the penguin after the move.
    :return: True if the move is valid, false otherwise.
    """
    NotImplemented


def move_penguin(user_token: str, start_row: int, start_col: int, end_row: int, end_col: int) -> FishGameState:
    """
    Make move for the player with the given user token starting at (start_row, start_col) and ending at (end_row, end_col).
    :param user_token: The user token of the player checking the move.
    :param start_row: The row of the penguin before the move.
    :param start_col: The col of the penguin before the move.
    :param end_row: The row of the penguin after the move.
    :param end_col: The col of the penguin after the move.
    :return: The updated state after the move | an error string if the move is invalid.
    """
    NotImplemented


def check_turn(user_token: str) -> str:
    """
    Check whose turn it is currently in the given game state.
    :param user_token:
    :return: The color of the player whose turn it is currently.
    """
    NotImplemented


def get_state(user_token: str) -> str:
    """
    Serialize the current state into the definition of state in player-protocol.md
    :param user_token: The users token who is making this request.
    :return: The string output of serializing a state.
    """
    NotImplemented


def get_possible_moves(user_token: str, color: str) -> List[Action]:
    """
    Get all possible moves for all of the penguins of the given color.
    :param user_token: The user token of the requester.
    :param color: The color whose moves will be checked.
    :return: Return a List[Action] that are all the possible moves for all of the penguins of the given color's penguins
    """
    NotImplemented

def get_moves_for_location(user_token: str, row: int, col: int) -> List[Action]:
    """
    Get all possible moves from this location.
    :param user_token: The user token of the requester.
    :param row: The start row of the moves to be checked.
    :param col: The end row of the moves to be checked.
    :return: List[Action] that represents all the possible moves that start at (row, col)
    """
    NotImplemented
    
    
def is_game_over(user_token: str):
    """
    Check whether any player in the given state can make a move.
    :param user_token: The user token of the requester.
    :return: Return true if there are no possible moves for any player in this game state, false otherwise
    """
    NotImplemented
