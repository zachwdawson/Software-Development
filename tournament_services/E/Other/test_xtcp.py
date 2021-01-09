import unittest
import socket
import sys
import os
from unittest.mock import patch
# insert overall directory structure into PATH so we can reference E
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import E.Other.xtcp as xtcp


SERVER_ADDRESS = ('127.0.0.1', 4567)


class TestXtcp(unittest.TestCase):

    def run_xtcpserver(self, send_string):
        """
        Purpose: Mock running the xtcp server so we can mock sending things to it
        Signature: Void -> String
        """
        with xtcp.XTCPServer(SERVER_ADDRESS, xtcp.XTCPJSONHandler) as serv:
            self.client = socket.create_connection(SERVER_ADDRESS)
            self.client.sendall(send_string.encode('utf-8'))
            self.client.shutdown(socket.SHUT_WR)
            serv.handle_request()
            result_string = ''
            while True:
                data = self.client.recv(1024)
                if data == b"":
                    break
                result_string += data.decode('utf-8')
            self.client.close()
            return result_string

    def test_basic_send(self):
        """
        Purpose: Test sending basic string using xtcp server
        Signature: Void -> Void
        """
        result = self.run_xtcpserver('1 2 3')
        self.assertEqual('{"count": 3, "seq": [1, 2, 3]}[3, 3, 2, 1]', result)

    def test_no_connection(self):
        """
        Purpose: Test that system exits with error when no connection within 3 seconds.
        Signature: Void -> Void
        """
        with self.assertRaises(SystemExit):
            with xtcp.XTCPServer(SERVER_ADDRESS, xtcp.XTCPJSONHandler) as serv:
                serv.handle_request()

    def test_default_port(self):
        """
        Purpose: Test getting the port from system arguments
        Signature: Void -> Void
        """
        testargs = ['./xtcp']
        with patch.object(sys, 'argv', testargs):
            port = xtcp.parse_port_arg()
        self.assertEqual(4567, port)


if __name__ == '__main__':
    unittest.main()
