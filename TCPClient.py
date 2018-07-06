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
from Client import SocketClient

host = "0.0.0.0"
port = 9090

def callback(data):
    pass

client = SocketClient(host, port, raw_input("username\n"), callback)
client.establish_connection()

# These 2 functions are called as threaded in establish_connection().
# client.keep_alive()
# client.receive()
while True:
    # Keep main thread alive
    dict = {
        "type": "None",
        "id": client.id,
        "content": "TEST-MESSAGE"
    }
    client.send_encrypted(json.dumps(dict))
    time.sleep(0.01)
