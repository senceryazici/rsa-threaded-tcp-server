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
from DataTypes.Types import *

loop_rate = 1000

host = "0.0.0.0"
port = 9090


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

# Request Connection
conn_req = {
    "id":"AAAACCCC",
    "type": RequestTypes.CONNECTION_REQUEST
}
print "sending",json.dumps(conn_req)
client.send(json.dumps(conn_req) + "\n")

# Receive Status
json_str = client.recv(1024)
print "Received Board Info: ", json_str
connection_info = json.loads(json_str)

if connection_info["type"] == InfoTypes.CONNECTION_INFO:
    client.settimeout(connection_info["timeout"])
    id = connection_info["id"]
    # client.id = connection_info["ID"]
    server_public_key = connection_info["rsa-public-key"]
elif connection_info["type"] == ConfirmationTypes.CONNECTION_REFUSED:
    print "WOW"
    pass

foward_message = {
    "id":id,
    "to": ["AAAAAAAA", "BBBBBBBB"],
    "type":MessageTypes.CARRY_MESSAGE,
    "content":"THIS IS A MESSAGE FOR AAAAAAA AND BBBBBBBB"
}
client.send(json.dumps(foward_message) + "\n")
time.sleep(1)
def keep_alive(_client):
    dict = {
        "id":id,
        "type":TcpTypes.KEEP_ALIVE
    }
    _client.send(json.dumps(dict) + '\n')
    return json.dumps(dict)

while True:
    print "KEEP_ALIVE:", keep_alive(client)
    time.sleep(2)
time.sleep(1000)
client.close()
