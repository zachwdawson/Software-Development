import copy
from collections import OrderedDict
from typing import Tuple, List, Dict, Optional

from Fish.Admin.kicked_player_type import KickedPlayerType
from Fish.Admin.manager_interface import ManagerInterface
from Fish.Admin.referee import LogicalPlayer, Referee
from Fish.Common.representations.enumerations.game_phase import GamePhase
from Fish.Common.representations.game_state import FishGameStateFactory


class Manager(ManagerInterface):
    """
    Class representing a tournament manager. A List of logical players gets passed to the manager. The messages variable
    keeps track of pushed messages to players and whether or not they accepted the message. The player pool is the currently
    active and non-eliminated players in a game. The entered is the list of logical players that originally entered. The rounds_active
    keeps track of the referee objects representing games in a current round. The last_round_winners keeps track of the winners of the last
    round in order to compare them to the current round's winners to determine if the game is over. The round keeps track of the
    current round.
    """
    def __init__(self, player_pool: List[LogicalPlayer]):
        self.messages = {}
        self.player_pool = player_pool
        self.entered = player_pool
        self.rounds_active = {}
        self.last_round_winners = []
        self.cheaters = []
        self.round = 0
        self.round_winners = []
        self.last_round = False
        if len(player_pool) < 2:
            raise ValueError('Cannot have less than 2 players in pool')

    def subscribe_tournament_observer(self, observer) -> None:
        #TODO: Implement tournament observer functionality.
        pass

    def run_tournament(self) -> None:
        """
        Purpose: This method begins a tournament for a Fish game. This tournament will
        contain a number of players that have been signed up and possibly some observers.
        This will begin the tournament with the currently existing observers and players.
        Signature: Void -> Void
        """
        self.inform_start(self.player_pool)

        while not self.is_tournament_over():
            self.round += 1
            player_allocations = self.assign_players(self.player_pool)
            self.rounds_active = self._create_round(player_allocations)
            self.round_winners, cheaters = self.get_winners_and_cheaters()
            self.cheaters.extend(cheaters)
            if self.round_winners == self.last_round_winners:
                break
            self.last_round_winners = self.round_winners
        losers = []
        for participant in self.entered:
            if participant not in self.player_pool:
                losers.append(participant)
        new_losers = self.inform_winner(self.player_pool)
        losers.extend(new_losers)
        for player in new_losers:
            self.player_pool.remove(player) #remove the losers because the winners are assumed to be those left at the end of the tournament
        self.inform_loser(losers)

    def is_tournament_over(self):
        """
        Purpose: Determines if a tournament has finished.
        Signature: Void -> bool
        """
        if len(self.last_round_winners) == 1 or self.last_round:
            return True
        else:
            if 0 < len(self.last_round_winners) <= 4:
                self.last_round = True
            return False

    def get_winners_and_cheaters(self):
        """
        Purpose: Determine the round winners once all games in the round are completed. Add them to a list and return
        them, which will be used later on in the next round creation. Also extract cheaters from each referee and
        return list of all cheaters from this round.
        Signature: Void -> List[LogicalPlayer], List[PlayerColor]
        """
        round_winners = []
        round_cheaters = []
        for i in self.rounds_active.keys():
            color_assignments = self.rounds_active[i].players
            round_winners += [color_assignments[i] for i in self.rounds_active[i].winners]
            round_cheaters += [player for kicked_type in self.rounds_active[i].kicked_players.values() for player in kicked_type] #combine lists of kicked players from kicked_player dictionary
        # from the pool, match the round winners with players from the pool
        round_winners = [i for i in self.player_pool if i[0] in round_winners]
        self.player_pool = round_winners
        round_winners = sorted(round_winners, key=lambda player: (player[1], player[0]))
        return round_winners, round_cheaters

    @staticmethod
    def assign_players(to_allocate: List[LogicalPlayer], max_players=4):
        """
        Purpose: Allocates players to a game based on the maximum amount of players in a single game. If a final allocation
        cannot be achieved, dissipates the last valid allocation game and tries to create another game.
        Signature: List[LogicalPlayers] int -> List[List[LogicalPlayers]]
        :param to_allocate: the players that need to be allocated
        :param max_players: the maximum amount of players in a game/allocation
        """
        if len(to_allocate) <= max_players:
            return [to_allocate]
        game_allocations = []
        while len(to_allocate) >= max_players:
            game_allocations.append(to_allocate[:max_players])
            to_allocate = to_allocate[max_players:]
        if len(to_allocate) > 0:
            if len(to_allocate) == 1:
                to_allocate = game_allocations[-1:][0] + to_allocate
                game_allocations.pop(len(game_allocations) - 1)
                while len(to_allocate) >= (max_players - 1):
                    game_allocations.append(to_allocate[:max_players - 1])
                    to_allocate = to_allocate[max_players - 1:]
                game_allocations.append(to_allocate)
            else:
                game_allocations.append(to_allocate)
        return game_allocations

    def inform_start(self, to_inform: List[LogicalPlayer]) -> List[LogicalPlayer]:
        missing_starters = []
        for player in to_inform:
            accepted_status = player[0].start()
            if not accepted_status:
                missing_starters.append(player)
        return missing_starters

    def inform_winner(self, to_inform: List[LogicalPlayer]) -> List[LogicalPlayer]:
        missing_winners = []
        for player in to_inform:
            accepted_status = player[0].end(True)
            if not accepted_status:
                missing_winners.append(player)
        return missing_winners

    def inform_loser(self, to_inform: List[LogicalPlayer]) -> List[LogicalPlayer]:
        missing_losers = []
        for player in to_inform:
            accepted_status = player[0].end(False)
            if not accepted_status:
                missing_losers.append(player)
        return missing_losers

    @staticmethod
    def _create_round(allocations):
        """
        Purpose: Creates and runs the round of the Fish game given player allocations. Creates multiple games,
        initializes them, and runs the games in order to get the winners/results.
        Signature: List[List[LogicalPlayers]] -> Dict[Referee]
        :param allocations: The determined player allocations for a single game
        :return rounds: Dictionary of referees that have finished each game
        """
        rounds = {}
        for i in range(len(allocations)):
            new_ref = Referee()
            state = FishGameStateFactory().create_game_state_with_num_fish(row=5, col=5, num_fish=2,
                                                                           player_colors=FishGameStateFactory.DEFAULT_COLOR_ORDER[:len(allocations[i])])
            new_ref.initialize_and_run_from_game_state(allocations[i], state)
            rounds[i] = new_ref
            if new_ref.current_game_state.get_game_phase() != GamePhase.END_GAME:
                raise ValueError("Game has not reached the end.")
        return rounds
