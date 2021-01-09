import socket
import json
from typing import List, Union

from Fish.Common.player_interface import PlayerInterface
from Fish.Common.representations.enumerations.player_color_enum import PlayerColor
from Fish.Common.representations.game_state import FishGameState
from Fish.Common.representations.types import Coordinate, Action
from Fish.Other.test_harness_transformation import TestHarnessTransformationHelper as THHelper


class PlayerProxy(PlayerInterface):
    """
    Player proxy component that implements the player interface. Handles the six Method Call Formats defined at
    https://www.ccs.neu.edu/home/matthias/4500-f20/remote.html (start, playing-as, etc.) utilizing a socket passed
    to them by the server that they can use to communicate with the client. The player proxy component responds to
    the manager and referee by sending a message of the format specified above to the client via the socket given on
    initialization and waiting on the client's response, then using the response to respond to the manager or referee
    in the internal player format.
    """

    def __init__(self, sock: socket):
        """
        Initializes a PlayerProxy instance with the given client socket for communicating with the client associated
        with this proxy
        @param sock: The socket connection for this PlayerProxy to send and receive information with the client
        """
        self.color = None
        self.other_colors = []
        self.winners = []
        self.sock = sock
        self.sock.settimeout(10)
        try:
            self.name = sock.recv(1024).decode('utf-8')
        except socket.timeout:
            self.name = None
            self.sock.close()
            return

        if not len(self.name) > 0 or not len(self.name) <= 12:
            self.name = None
            self.sock.close()
            return

    def start(self) -> bool:
        """
        Informs this PlayerProxy's associated client that the tournament is starting and returns whether or not the
        client provided a valid response
        @return: True if the client responded correctly, False otherwise.
        """
        message = json.dumps(["start", [True]]).encode('utf-8')
        self.sock.sendall(message)
        try:
            response = self.sock.recv(1084).decode('utf-8')
            if response == "void":
                return True
            else:
                return False
        except socket.timeout:
            return False

    def end(self, is_winner: bool) -> bool:
        """
        Informs this PlayerProxy's associated client that the tournament has ended and whether or not the client won
        the tournament, and returns whether or not the client provided a valid response
        @param is_winner: True if this PlayerProxy's client won the tournament, False otherwise
        @return: True if the client responded correctly, False otherwise.
        """
        message = json.dumps(["end", [is_winner]]).encode('utf-8')
        self.sock.sendall(message)
        try:
            response = self.sock.recv(1084).decode('utf-8')
            if response == "void":
                return True
            else:
                return False
        except socket.timeout:
            return False

    def assign_color(self, color: PlayerColor) -> bool:
        """
        Informs this PlayerProxy's associated client that they are playing in a game of Fish as the given color and
        returns whether or not the client provided a valid response
        @param color: The color that this PlayerProxy's client is playing as in the game
        @return: True if the client responded correctly, False otherwise.
        """
        self.color = color
        message = json.dumps(["playing-as", [color.value]]).encode('utf-8')
        self.sock.sendall(message)
        try:
            response = self.sock.recv(1084).decode('utf-8')
            if response == "void":
                return True
            else:
                return False
        except socket.timeout:
            return False

    def player_place_penguin(self, state: FishGameState) -> Union[Coordinate, bool]:
        """
        Given the current state of the game, constructs a JSON representation of the game state and sends that to this
        PlayerProxy's associated client and waits on a response in the form of a JSON list with two ints representing
        the position on the game board to place their penguin.
        @param state: the current state of the game
        @return: False if self.sock times out waiting on a response from the client, otherwise the Coordinate that the
                 client returned
        """
        state_json = THHelper.convert_state_to_json(state)
        message = json.dumps(["setup", [state_json]]).encode('utf-8')
        self.sock.sendall(message)
        try:
            coordinate = json.loads(self.sock.recv(1084).decode('utf-8'))
            coordinate = THHelper.convert_to_double_height(coordinate[0], coordinate[1])
        except socket.timeout:
            return False
        return coordinate

    def player_move_penguin(self, state: FishGameState) -> Union[Action, bool]:
        """
        Given the current state of the game, constructs a JSON representation of the game state and sends that to this
        PlayerProxy's associated client and waits on a response in the form of a JSON list of two lists each containing
        two ints representing the position to move this client's penguin from and the position to move this client's
        penguin to
        @param state: the current state of the game
        @return: False if self.sock times out waiting on a response from the client, otherwise the Acton that the client
        returned
        """
        state_json = THHelper.convert_state_to_json(state)
        message = json.dumps(["take-turn", [state_json, []]]).encode('utf-8')
        self.sock.sendall(message)
        try:
            action = json.loads(self.sock.recv(1084).decode('utf-8'))
            from_coord = THHelper.convert_to_double_height(action[0][0], action[0][1])
            to_coord = THHelper.convert_to_double_height(action[1][0], action[1][1])
            action = (from_coord, to_coord)
        except socket.timeout:
            return False
        return action

    def show_other_players_colors(self, colors: List[PlayerColor]):
        """
        Informs this PlayerProxy's associated client that they are playing in a game of Fish with a number of clients
        represented by the given colors and returns whether or not the client provided a valid response
        @param colors: The colors that the other clients in the game are playing as
        @return: True if the client responded correctly, False otherwise.
        """
        self.other_colors = colors
        message = json.dumps(["playing-with", [color.value for color in colors]]).encode('utf-8')
        self.sock.sendall(message)
        try:
            response = self.sock.recv(1084).decode('utf-8')
            if response == "void":
                return True
            else:
                return False
        except socket.timeout:
            return False

    def inform_of_winners(self, winners: List[PlayerColor]) -> bool:
        """
        Function called by referee to inform internal players that they have won a single game of Fish.
        Since this is not an interaction specified by the remote proxy pattern, this function simply returns True
        without communicating with the client
        @param winners: The players who won the game of Fish
        @return: True to indicate that the client would've responded correctly
        """
        self.winners = winners
        return True

    def receive_message(self, message: str, message_id: int) -> bool:
        #TODO message will be delivered to user through the communication layer
        #print('Message Received: ', message)
        return True
