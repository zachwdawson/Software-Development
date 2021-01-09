#!/usr/bin/env python3
import json
import fileinput

# relative path importing so that it can be used as a script
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  '..')))

from Fish.Other.test_harness_transformation import TestHarnessTransformationHelper as THHelper


def parse_and_create_output(state_json):
    """
    Purpose: Parses the State object from the input and creates an output for the integration testing handle
    Signature: State -> Void
    :param state_json: State object as specified converted into Python object
    :return: Prints out state object after moving a direction or False if no direction works
    """
    players = state_json['players']
    game_state = THHelper.create_state(state_json)
    first_player_first_peng = game_state.get_penguins_for_player(game_state.get_current_turn())[0]
    neighbors = THHelper.find_coord_neighbors(first_player_first_peng)
    could_move = try_moves(first_player_first_peng, game_state, neighbors)
    if could_move:
        # update players, board and cycle players to back
        update_player_list(game_state, players)
        cycle_players(players)
        state_json['board'] = THHelper.convert_board_to_json(game_state.get_board())
        print(json.dumps(state_json))
    else:
        print(json.dumps(False))


def try_moves(first_player_first_penguin, game_state, neighbors):
    """
    Purpose: Try moving first players first penguin in all the 6 cardinal directions
    Signature: Coordinate GameState -> Boolean
    :param first_player_first_penguin: Coordiante of first players first penguin
    :param game_state: GameState that we are modifying
    :param neighbors: All the neighbor coordinates that we want to try out in order
    :return: boolean representing whether a move happened or not
    """
    could_move = False
    for neighbor in neighbors:
        did_error = False
        try:
            game_state.move_penguin(game_state.get_current_turn(), first_player_first_penguin, neighbor)
        except ValueError:
            did_error = True
        finally:
            if not did_error:
                could_move = True
                break
    return could_move


def update_player_list(game_state, players):
    """
    Purpose: Update the players after move has been made
    Signature: GameState Player* -> Void
    :param game_state: Game state that has been modified with a move
    :param players: Players object needs updated score for player
    """
    first_player_color = game_state.get_player_order()[0]
    new_score = game_state.get_fish_for_player(first_player_color)
    penguins = game_state.get_penguins_for_player(first_player_color)
    players[0]['score'] = new_score
    # convert representation back
    players[0]['places'] = [THHelper.convert_back_to_posn(pos[0], pos[1]) for pos in penguins]


def cycle_players(players):
    """
    Purpose: Cycle players to back of list
    """
    player1 = players.pop(0)
    players.append(player1)


if __name__ == '__main__':
    state = json.loads(THHelper.read_from_stdin())
    parse_and_create_output(state)
