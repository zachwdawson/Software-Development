#!/usr/bin/env python3
import argparse
import json
import os
import socketserver
import sys

# PATH configuration so we can add code from C: Add overall directory to PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import C.Other.xjson as xjson

# get default hostname
SERVER_HOSTNAME = '127.0.0.1'
TIMEOUT_SECONDS = 3


class XTCPJSONHandler(socketserver.StreamRequestHandler):
    """Custom class to handle requests to our TCP server"""

    def handle(self):
        """
        Purpose: Reads, processes, and writes back a JSON object as well as the count of the sequence to send over TCP.
        Signature: Void -> Void
        """
        # Read the JSON from the connection
        data_string = ''
        for line in self.rfile:
            data_string += line.decode('utf-8')

        # Process JSON with functions from C
        result_list = xjson.parse_json_objects(data_string)
        count_seq_object = xjson.create_count_seq_object(result_list)
        json_list = xjson.create_json_list(result_list)

        # Write back JSON string
        count_seq_bytes = json.dumps(count_seq_object).encode('utf-8')
        json_list_bytes = json.dumps(json_list).encode('utf-8')
        self.wfile.write(count_seq_bytes)
        self.wfile.write(json_list_bytes)


class XTCPServer(socketserver.TCPServer):
    """Subclass default TCPServer class to throw our specific error on timeout"""

    def __init__(self, *args):
        super(XTCPServer, self).__init__(*args)
        self.timeout = TIMEOUT_SECONDS

    def handle_timeout(self):
        sys.exit('Error: Client did not connect in {} seconds'.format(str(TIMEOUT_SECONDS)))


def parse_port_arg():
    """
    Parse the port from the command line arguments
    Signature: Void -> String
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('tcp_port', help='TCP port that server will be on', nargs='?', type=int, default=4567)
    args = parser.parse_args()
    port = args.tcp_port
    return port


def main():
    """
    Parse the command line argument and then run the TCP server
    """
    port = parse_port_arg()
    server_address = (SERVER_HOSTNAME, port)
    with XTCPServer(server_address, XTCPJSONHandler) as server:
        # handle a single request
        server.handle_request()


if __name__ == '__main__':
    main()
