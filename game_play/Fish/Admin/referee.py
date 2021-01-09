from Common.state import FishGameState
from Common.board import FishBoard
from structures import Action, Player, GameStatePhase
from Player.player import PlayerComponent
from typing import List
from const import PENGUIN_COLORS


class Referee(object):

    def __init__(self, players: List[PlayerComponent], num_rows: int, num_cols: int):
        """
        A Referee handles the gameplay of a Fish game. A gameplay consists of
        requesting players for penguin placements, the players' movements, kicking players
        for invalid moves, and notify players of notable events - kicking, endgame, and winners.
        A Referee is provided a list of players and the board dimensions from the tournament manager.
        """
        board = FishBoard(num_rows=num_rows, num_cols=num_cols)
        state_players = [
            Player(color=color, age=0, score=0, penguins=[]) for color in PENGUIN_COLORS[:len(players)]
        ]

        self.players = {
            player.color: component for component, player in zip(players, state_players)
        }

        self.state = FishGameState(board=board, num_players=len(players),
                                   players=state_players, current_player=state_players[0],
                                   phase=GameStatePhase.INITIAL)

    def notify_player_placement(self):
        """
        Notify the current player to place one of its penguin.
        :return: N/A
        """
        player_to_notify = self.players[self.state.current_player.color]
        placement_coordinate = player_to_notify.get_penguin_placement(self.state)
        is_valid, _ = self.state.can_add_penguin(
            row=placement_coordinate.row,
            col=placement_coordinate.col,
            color=self.state.current_player.color)

        if is_valid:
            self.state = self.state.add_penguin(
                row=placement_coordinate.row,
                col=placement_coordinate.col,
                color=self.state.current_player.color)
        else:
            self.notify_player_kicked(player_to_notify)
            self.state = self.state.kick_player(self.state.current_player)

    def end_penguin_placement(self):
        """
        Transitions the game from placing penguin phase to moving penguin phase.
        """
        self.state = self.state.finalize()

    def notify_players_movement(self):
        """
        Notify the current player that is their turns to move a penguin.
        :return: N/A
        """
        player_to_notify = self.players[self.state.current_player.color]
        player_action = player_to_notify.get_penguin_movement(self.state)
        is_valid, _ = self.state.can_move_penguin(
            color=self.state.current_player.color,
            start_row=player_action.start.row,
            start_col=player_action.start.col,
            end_row=player_action.end.row,
            end_col=player_action.end.col)

        if is_valid:
            self.state = self.state.move_penguin(color=self.state.current_player.color,
                                                 start_row=player_action.start.row,
                                                 start_col=player_action.start.col,
                                                 end_row=player_action.end.row,
                                                 end_col=player_action.end.col)

        else:
            self.notify_player_kicked(player_to_notify)
            self.state = self.state.kick_player(self.state.current_player)

    def notify_player_kicked(self, player: PlayerComponent):
        """
        Notifies the given player that they've been kicked from the game for cheating.
        :return: N/A
        """
        player.notify_kicked()

    def notify_winners(self):
        """
        notify winners that they won the game.
        :return: N/A
        """
        sorted_players = sorted(list(self.state.players.values()), key=lambda player: player.score, reverse=True)
        max_players = [
            player for player in sorted_players if player.score == sorted_players[0].score
        ]

        for winner in max_players:
            self.players[winner.color].notify_winner()

    def end_game(self):
        """
        Notify all's the player left in the game that the game has been concluded.
        :return: N/A
        """
        self.state = self.state.end_game()
        for _, player in self.players.items():
            player.notify_game_over()
