import socket
import datetime
import json
from typing import List
from Fish.Remote.player_proxy import PlayerProxy
from Fish.Admin.manager import Manager


class TCPServer:
    """
    Represents the Fish tournament server that accepts a certain number of client connections and then conducts a Fish
    tournament by creating PlayerProxy components and handing those to the tournament manager, which interacts with the
    player proxies as if they were internal players. The PlayerProxy component handles direct communication with the
    associated client.
    """

    def __init__(self, host, port):
        """
        Initializes a TCPServer instance with the given host and port number for creating a socket via self.configure_server()
        @param host: The host IP address to connect to
        @param port: The port number to use for connection
        """
        self.host = host            # Host address
        self.port = port            # Host port
        self.sock = None            # Connection socket
        self.tournament_manager = None
        self.clients = []

    def configure_server(self) -> None:
        """
        Initializes this TCPServer's self.sock, connects it to (self.host, self.port), and sets its timeout to 30 seconds
        @return: None
        """
        # create TCP socket with IPv4 addressing
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind server to the address
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(30) # set listen timeout to 30

    def wait_for_client(self, last_try=False) -> List[int]:
        """
        This TCPServer attempts to initiate a tournament. It listens on self.sock for 30 seconds or until 10 clients
        connect, creating a PlayerProxy for each client that connects. Then, if at least 5 clients have connected, it
        initializes self.tournament_manager and initiates a tournament via self.run_tournament()
        @param last_try: If, after initially waiting 30 seconds, less than 4 clients have connected, the function
                         tries again with last_try set to True. If last_try is True and less than 4 clients connect
                         before timeout, the function exits without trying again.
        @return: A List of the format [int, int], where the first element is the number of players that won the tournament
                 and the second element is the number of players that failed or cheated during the tournament
        """
        try:
            self.sock.listen(10) # 10 clients before server refuses connections

            while len(self.clients) < 10:
                client_sock, client_address = self.sock.accept()
                player_client = PlayerProxy(client_sock)
                if player_client.name:
                    self.clients.append(player_client)

        except socket.timeout:
            if len(self.clients) < 5 and not last_try:
                self.wait_for_client(True)
            elif len(self.clients) >= 5:
                self.tournament_manager = Manager(list(zip(self.clients, [i for i in range(len(self.clients))])))

        except KeyboardInterrupt:
            self.shutdown_server()

        if len(self.clients) < 5 and not last_try:
            self.wait_for_client(True)
        elif len(self.clients) >= 5:
            self.tournament_manager = Manager(list(zip(self.clients, [i for i in range(len(self.clients))])))

        if self.tournament_manager:
            return self.run_tournament()

    def run_tournament(self) -> List[int]:
        """
        Calls this TCPServer's tournament manager to run a tournament and returns the results.
        @return: AList of the format [int, int], where the first element is the number of players that won the tournament
                 and the second element is the number of players that failed or cheated during the tournament
        """
        self.tournament_manager.run_tournament()
        self.shutdown_server()
        return [len(self.tournament_manager.player_pool), len(self.tournament_manager.cheaters)]

    def shutdown_server(self) -> None:
        """
        Closes this TCPServer's self.sock
        @return: None
        """
        self.sock.close()
