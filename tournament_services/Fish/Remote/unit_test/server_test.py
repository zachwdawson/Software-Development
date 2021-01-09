import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


import unittest
import socket
from unittest.mock import MagicMock
from Fish.Remote.server import TCPServer
from Fish.Player.player import BasicPlayer
from Fish.Admin.manager import Manager


class ServerTest(unittest.TestCase):

    def test_server_fail(self):
        server = TCPServer(1234, '127.0.0.1')
        with self.assertRaises(TypeError):
            server.configure_server()

    def test_run_tournament(self):
        server = TCPServer('127.0.0.1', 1234)
        server.configure_server()
        player_list = []
        for i in sorted(range(0, 3)):
            interface = BasicPlayer()
            player_list.append((interface, i))
        manager = Manager(player_list)
        server.tournament_manager = manager
        self.assertEqual(server.run_tournament(), [1,0])

if __name__ == '__main__':
    unittest.main()
