# Copyright (c) 2017-2018 Sencer Yazici, https://github.com/senceryazici
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import socket
import time
import json
import thread
from DataTypes.Types import *

class SocketClient():

    def __init__(self, host, port, id, callback=None):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.listen = False
        self.on_received = callback
        self.id = id
        self.server_public_key = ""
        self.timeout = 0
        self.keep_alive_flag = False

    def receive(self):
        while self.listen:
            message_received = self.socket.recv(2048)
            self.on_received(message_received)
            print message_received
        thread.exit()

    def keep_alive(self):
        while self.keep_alive_flag:
            dict = {
                "id": self.id,
                "type": TcpTypes.KEEP_ALIVE
            }
            self.socket.send(json.dumps(dict) + '\n')
            time.sleep(self.timeout / 2)
        print "[ INFO ] Stopped Keep Alive Process."


    def establish_connection(self):
        # Request Connection
        conn_req = {
            "id": self.id,
            "type": RequestTypes.CONNECTION_REQUEST
        }
        print "sending", json.dumps(conn_req)
        self.socket.send(json.dumps(conn_req) + "\n")

        # Receive Status
        json_str = self.socket.recv(1024)
        print "Received Connection Info: ", json_str
        connection_info = json.loads(json_str)

        if connection_info["type"] == InfoTypes.CONNECTION_INFO:
            self.socket.settimeout(connection_info["timeout"])
            self.timeout = connection_info["timeout"]
            self.id = connection_info["id"]
            self.server_public_key = connection_info["rsa-public-key"]
            self.listen = True
            self.keep_alive_flag = True

            thread.start_new_thread(self.receive, ())
            thread.start_new_thread(self.keep_alive, ())

        elif connection_info["type"] == ConfirmationTypes.CONNECTION_REFUSED:
            print "Server Refused Connection."


    def request(self, request_type):
        dict = {
            "id": self.id,
            "type": request_type
        }
        self.socket.send(json.dumps(dict) + "\n")
        return self.socket.recv(2048)
