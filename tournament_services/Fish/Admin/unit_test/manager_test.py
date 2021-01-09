import os
import sys
import unittest
from unittest.mock import MagicMock

# relative path importing
from Fish.Admin.manager import Manager
from Fish.Player.player import BasicPlayer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


class ManagerTests(unittest.TestCase):
    """
    This is a class that will run different tests to unit-test our manager
    """
    # Creates a list of logical players

    def test_assign_players_max(self):
        """
        Purpose: Test assigning the players with the maximum number of players in a game, 4
        Signature: Void -> Void
        """
        player_list = []
        for i in sorted(range(0, 14)):
            interface = BasicPlayer()
            player_list.append((interface, i))

        manager = Manager(player_list)
        assignments = manager.assign_players(manager.player_pool)

        for assignment in assignments:
            self.assertNotEqual(len(assignment), 1)
            self.assertNotEqual(len(assignment), 0)

        self.assertEqual(len(assignments[0]), 4)
        self.assertEqual(len(assignments[len(assignments) - 1]), 2)

    def test_assign_players_non_default(self):
        """
        Purpose: Test assigning the players with less than the default (4) players allowed per a single game.
        Signature: Void -> Void
        """
        player_list = []
        for i in sorted(range(0, 4)):
            interface = BasicPlayer()
            player_list.append((interface, i))

        manager = Manager(player_list)
        assignments = manager.assign_players(manager.player_pool, max_players=2)
        for assignment in assignments:
            self.assertNotEqual(len(assignment), 1)
            self.assertNotEqual(len(assignment), 0)

    def test_assign_players_under_max(self):
        """
        Purpose: Test assigning the players when the player pool is less than than maximum number of players per game
        Signature: Void -> Void
        """
        player_list = []
        for i in sorted(range(0, 2)):
            interface = BasicPlayer()
            player_list.append((interface, i))

        manager = Manager(player_list)
        assignments = manager.assign_players(manager.player_pool, max_players=4)
        self.assertEqual(len(assignments), 1)

    def test_passing_small_pool(self):
        """
        Purpose: Tests passing a pool of players that is less than enough to run a game
        Signature: Void -> Void
        """
        with self.assertRaises(ValueError):
            player_list = []
            for i in sorted(range(0, 1)):
                interface = BasicPlayer()
                player_list.append((interface, i))
            manager = Manager(player_list)

    def test_assign_players_7(self):
        player_list = []
        for i in sorted(range(0, 7)):
            interface = BasicPlayer()
            player_list.append((interface, i))

        manager = Manager(player_list)
        assignments = manager.assign_players(manager.player_pool)
        self.assertEqual(len(assignments[0]), 4)
        self.assertEqual(len(assignments[1]), 3)

    def test_assign_players_5(self):
        player_list = []
        for i in sorted(range(0, 5)):
            interface = BasicPlayer()
            player_list.append((interface, i))

        manager = Manager(player_list)
        assignments = manager.assign_players(manager.player_pool)
        self.assertEqual(len(assignments[0]), 3)
        self.assertEqual(len(assignments[1]), 2)

    def test_run_tournament(self):
        """
        Purpose: Runs a tournament round given a list of passed players. Checks that the tournament has finished at the
        end, and checks if the remaining player pool is less than or equal to the starting pool.
        Signature: Void -> Void
        """
        player_list = []
        for i in sorted(range(0, 3)):
            interface = BasicPlayer()
            player_list.append((interface, i))
        manager = Manager(player_list)
        manager.run_tournament()
        # Checks that the winning player pool is less than or equal to the initial passed pool
        self.assertTrue(len(player_list) >= len(manager.player_pool))
        # Checks if rounds advanced
        self.assertTrue(manager.round > 0)

    def test_run_tournament_large(self):
        """
        Purpose: Runs a tournament round given a list of passed players. Checks that the tournament has finished at the
        end, and checks if the remaining player pool is less than or equal to the starting pool.
        Signature: Void -> Void
        """
        player_list = []
        for i in sorted(range(0, 20)):
            interface = BasicPlayer()
            player_list.append((interface, i))
        manager = Manager(player_list)
        manager.run_tournament()
        # Checks if minimum amount of rounds has passed
        self.assertTrue(manager.round >= 2)

    def test_is_tournament_over_duplicate_round_winners(self):
        """
        Purpose: Checks to determine if a tournament has reached the end condition.
        Signature: Void -> Void.
        """
        player_list = []
        for i in sorted(range(0, 8)):
            interface = BasicPlayer()
            player_list.append((interface, i))

        manager = Manager(player_list)
        manager.get_winners_and_cheaters = MagicMock(return_value=(player_list,[]))
        manager.last_round_winners = player_list
        manager.run_tournament()
        # get last round winners to equal current round winners
        self.assertEqual(manager.round, 1)

    def test_is_tournament_over_one_remaining_player(self):
        player_list = []
        for i in sorted(range(0, 8)):
            interface = BasicPlayer()
            player_list.append((interface, i))

        manager = Manager(player_list)
        manager.get_winners_and_cheaters = MagicMock(return_value=([player_list[0]],[]))
        # manager.get_winners = MagicMock(return_value=[player_list[0]])
        manager.run_tournament()
        # make only one winner
        self.assertEqual(manager.round, 1)

    def test_is_tournament_over_4_remaining_players_with_tie(self):
        player_list = []
        for i in sorted(range(0, 4)):
            interface = BasicPlayer()
            player_list.append((interface, i))

        manager = Manager(player_list)
        manager.get_winners_and_cheaters = MagicMock(return_value=([player_list[0], player_list[1]],[]))
        manager.run_tournament()
        #have ties with 4 players left
        self.assertEqual(manager.round, 2)
        self.assertEqual(manager.last_round_winners, [player_list[0], player_list[1]])

    def test_is_tournament_over_3_remaining_players_with_tie(self):
        player_list = []
        for i in sorted(range(0, 3)):
            interface = BasicPlayer()
            player_list.append((interface, i))

        manager = Manager(player_list)
        manager.get_winners_and_cheaters = MagicMock(return_value=([player_list[0], player_list[1]], []))
        manager.run_tournament()
        #have ties with 4 players left
        self.assertEqual(manager.round, 2)
        self.assertEqual(manager.last_round_winners, [player_list[0], player_list[1]])

    
