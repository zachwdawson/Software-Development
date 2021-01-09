from typing import List, Dict

from Fish.Admin.kicked_player_type import KickedPlayerType

class ManagerInterface(object):
    """
    This is an interface that will need to be implemented for a tournament manager
    in a Fish game. It provides a number of methods that a referee or game observer or
    a player can access in order to successfully communicate to run a tournament.
    """

    # Observer -> Manager Methods:
    def subscribe_tournament_observer(self, observer) -> None:
        """
        Purpose: This method subscribes a tournament observer to this
        tournament manager instance. The observer will be added to this
        tournament managers list of observers and will be able to receive updates
        from the tournament manager on individual games, rounds, and overall results
        of the tournament. We have not implemented FishGameObserver, but it will
        have its own interface which contains an update method that the tournament
        manager must call.
        Signature: FishGameObserver -> Void
        """
        raise NotImplemented

    # Ref -> Manager Methods:
    def report_game_results(self, winners: List[int], kicked_players: Dict[KickedPlayerType, int]) -> None:
        """
        Purpose: This is a method that reports the results of a single Fish game back to the tournament
        manager. This is used by the referee and will identify the players by their age rather than
        by their color in the game, so that the tournament manager knows what has happened to the players.
        Signature: [Int] Dict[KickedPlayerType, int] -> Void
        :param winners: List of winners denoted by the player age so that the tournament manager
        can know who won and lost
        :param kicked_players: List of players who have been kicked, broken into cheating and failing
        """
        raise NotImplemented

#TODO Consider removing from interface
    '''
    # Player -> Manager Methods:
    def player_enter_tournament(self, player: PlayerInterface) -> int:
        """
        Purpose: This method allows a player to enter a tournament with a given
        implementation of a player. This will make games be played that include their player
        until the player is eliminated by loss or kicked from the game. It will return back
        age, which can be used by the player to uniquely identify themselves in any results coming
        from the tournament.
        :param player: Implementation of a player that is being entered into the tournament.
        :return: An integer representing the players age, which will be incremented for each player
        entered and will uniquely identify the player.
        """
        raise NotImplemented
    '''

    # Misc methods:
    def run_tournament(self) -> None:
        """
        Purpose: This method begins a tournament for a Fish game. This tournament will
        contain a number of players that have been signed up and possibly some observers.
        This will begin the tournament with the currently existing observers and players.
        Signature: Void -> Void
        """
        raise NotImplemented

