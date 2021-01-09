import socket
import sys
import json
from typing import List, Union

from Fish.Common.representations.game_state import FishGameState
from Fish.Player.strategy import FishBasicStrategy
from Fish.Other.test_harness_transformation import TestHarnessTransformationHelper as THHelper


class TCPClient:
    """
    Represents a remote player that connects to the Fish tournament server via TCP and plays games of Fish by sending
    JSON representations of its intents to the server in response to queries for placements or movements.
    """

    def __init__(self, host: str, port: int, name: str):
        """
        Initializes a TCPClient instance and connects to the specified host on the given port using a socket, then sends
        the given name over the socket.
        @param host: The host IP address to connect to
        @param port: The number of the port to use for the connection
        @param name: The name to send via the socket created
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10) # conservative estimate based off 1 second interactions with 4 players
        self.sock.connect((host, port))
        self.sock.sendall(json.dumps(name).encode('utf-8'))

        # The present implementation for the strategy component takes too long to compute moves for a depth of
        # 2 to be possible given the specified timeouts
        self.strategy = FishBasicStrategy(1)

    def play_tournament(self) -> None:
        """
        Enters this TCPClient into active tournament-playing mode. The client continually waits on self.sock to receive
        messages from the server and calls its associated functions for depending on the message type received.
        The message types are:
            - start: client is being informed that the tournament is starting
            - playing-as: client is being informed that it is playing a Fish game as the given color
            - playing-with: client is being informed how many other players it is playing a Fish game with
            - setup: client is being asked to submit a position for penguin placement
            - take-turn: client is being asked to sumbit an action for penguin movement
            - end: client is being informed that the tournament has ended
        """
        while True:
            try:
                message = self.sock.recv(2048).decode('utf-8')
                if message == "":
                    break
                received = json.loads(message)
            except socket.timeout:
                sys.stderr.write("Server timeout")
                sys.exit(1)
            except json.JSONDecodeError:
                sys.stderr.write("Malformed message received")
                sys.exit(1)

            if received:
                function = received[0]

                if function == "start":
                    self.start(received[1][0])
                elif function == "playing-as":
                    self.playing_as(received[1][0])
                elif function == "playing-with":
                    self.playing_with(received[1][0])
                elif function == "setup":
                    self.setup(THHelper.create_state(received[1][0]))
                elif function == "take-turn":
                    self.take_turn(THHelper.create_state(received[1][0]), received[1][1])
                elif function == "end":
                    self.end(received[1][0])
                else:
                    sys.stderr.write(f"Unknown Function Received {function}")

    def start(self, starting: bool) -> None:
        """
        Sends the appropriate response to a 'start' message on this TCPClient's socket
        @param starting: Boolean value; always true
        @return: None
        """
        self.sock.sendall("void".encode("utf-8"))

    def end(self, ending: bool) -> None:
        """
        Sends the appropriate response to an 'end' message on this TCPClient's socket
        @param ending: Boolean value; always true
        @return: None
        """
        self.sock.sendall("void".encode("utf-8"))

    def playing_as(self, color: str) -> None:
        """
        Sends the appropriate response to a 'playing-as' message on this TCPClient's socket
        @param color: The color that this client is playing as in the game
        @return: None
        """
        self.sock.sendall("void".encode("utf-8"))

    def playing_with(self, colors: List[str]) -> None:
        """
        Sends the appropriate response to a 'playing-with' message on this TCPClient's socket
        @param colors: The colors that the other clients in the game are playing as
        @return: None
        """
        self.sock.sendall("void".encode("utf-8"))

    def setup(self, state: FishGameState) -> None:
        """
        Given the current state of the game, which is assumed to be in penguin placement phase, find the ideal placement
        position via the strategy component and send it as a response on self.sock
        @param state: The current FishGameState
        @return: None
        """
        position = self.strategy.find_next_placement(state)
        position = THHelper.convert_back_to_posn(position[0], position[1])
        self.sock.sendall(json.dumps(position).encode("utf-8"))

    def take_turn(self, state: FishGameState, previous_moves: List[Union[bool, List[List[int]]]]) -> None:
        """
        Given the current state of the game, which is assumed to be in penguin movement phase, find the ideal action to
        take via the strategy component and send it as a response on self.sock
        @param state: The current FishGameState
        @param previous_moves: Optionally used by clients for strategy; represents the actions taken since the previous
                               move that this client took.
        @return: None
        """
        action = self.strategy.find_next_move(state)
        from_position = THHelper.convert_back_to_posn(action[0][0], action[0][1])
        to_position = THHelper.convert_back_to_posn(action[1][0], action[1][1])
        action = [from_position, to_position]
        self.sock.sendall(json.dumps(action).encode("utf-8"))
