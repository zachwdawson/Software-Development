from typing import List
from Player.player import PlayerComponent
from Admin.referee import Referee

class TournamentManager(object):
    """
    Store the list of players who are still in the tournament. Run rounds of games where winners remain and losers
    are removed from the tournament. Run until only one person left and deem them the winner. Calculate statistics when
    necessary and return them to observers. All TournamentStructures, Observer, and StatisticType have not been defined yet.
    TournamentStructure will contain the logic for allocating players to rounds. It could potentially be a bracket,
    a round robin, or any type of tournament you can think of. The Observer will handle sending information to people
    watching the tournament, and the StatisticType is a placeholder for what type of tournament statistics will be
    important for viewers to know.
    """

    def __init__(self, players: List[PlayerComponent], tournament_structure: TournamentStructure):
        """
        Store the list of Players as those who are currently in the tournament
        :param players: List of PlayerComponents to start the tournament
        :param tournament_structure: TournamentStructure provides the functionality for allocating players to a game.
        Not currently implemented.
        """
        NotImplemented

    def run_tournament(self):
        """
        Runs the tournament starting off with the current list of players and building subsequent rounds with the previous
        round's winners until only one player remains.
        :return: PlayerComponent who won the tournament.
        """
        NotImplemented

    def build_round(self) -> List[Referee]:
        """
        Use the functionality within the tournament structure to allocate player's to referees.
        :return: List[Referee] that contain the start state of each game for the players allocated by the tournament structure
        """
        NotImplemented

    def register_observer(self, observer: Observer):
        """
        Register an observer for this tournament. An observer will receive event information about game play and the
        tournament status including winners and winning scores.
        :param observer: The observer that will begin to receive game play information
        :return:
        """
        NotImplemented

    def get_statistic(self, stat_type: StatisticType):
        """
        Calculate the requested statistic and serialize it in JSON.
        :param stat_type: Enum of StatisticType
        :return: Returns the requested statistic in the format of JSON.
        """
        NotImplemented

    def end_tournament(self):
        """
        Checks if the tournament is over and informs the winner that they won if it is over.
        :return: True if the tournament is over, False otherwise.
        """
