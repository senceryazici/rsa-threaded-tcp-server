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

# The SocketServer and BasicChatServer Objects are constructed by Arbel Israeli on stackoverflow
# You can find the original structure at this link.
# https://stackoverflow.com/questions/17453212/multi-threaded-tcp-server-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

import socket
import thread
import time
import json
# TODO: Client id assignment - To get clients from id (Process id)
# TODO: Client user type assignmen - To check user priviledges

class Client():
    def __init__(self):
        self.client = None
        self.id = None

    def send(self, arg):
        self.client.send(arg)

    def recv(self, arg):
        self.client.recv(arg)

    def close(self):
        self.client.close()

class SocketServer(socket.socket):

    def __init__(self):
        socket.socket.__init__(self)
        #To silence- address occupied!!
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.bind(('0.0.0.0', 9090))
        self.listen(5)
        self.clients = []

    def run(self):
        print "Server started"
        try:
            self.accept_clients()
        except Exception as ex:
            print ex
        finally:
            print "Server closed"
            for client in self.clients:
                client.close()
            self.close()

    def accept_clients(self):
        while 1:
            (clientsocket, address) = self.accept()
            # print self.clients
            clientsocket.settimeout(self.client_timeout)
            #Adding client to clients list

            self.clients.append(clientsocket) # FIXME
            #Client Connected
            self.onopen(clientsocket)

            conn_info = {
                "timeout": self.client_timeout,
                "id": "A2X9J1H8",
                "rsa-public-key": "AAA",
                "type":"CONNECTION_INFO"
            }

            clientsocket.send(json.dumps(conn_info))
            #Receiving data from client
            thread.start_new_thread(self.recieve, (clientsocket,))

    def recieve(self, client):
        # CHANGED: time_step = 0.1
        timeout_flag = False
        while not timeout_flag:
            try:
                data = client.recv(1024)
                if data == '':
                    break
                #Message Received
                data = data.replace("\r\n", "")
                data = data.replace("\n", "")
                data = data.replace("\r", "")
                self.onmessage(client, data)
            except socket.timeout:
                timeout_flag = True
                print "Timeout reached, Client disconnecting"

        #Removing client from clients list
        self.clients.remove(client)
        #Client Disconnected
        self.onclose(client)
        #Closing connection with client
        client.close()
        #Closing thread
        thread.exit()

    def send_to_specific_client(self, client, message):
        # Sending message only to a client
        for c in self.clients:
            if c == client:
                c.send(message)
    def send_to_all_except(self, client, message):
        # Sending message to all except a client
        for c in self.clients:
            if c != client:
                c.send(message)

    def broadcast(self, message):
        #Sending message to all clients
        for client in self.clients:
            client.send(message)

    def onopen(self, client):
        pass

    def onmessage(self, client, message):
        pass

    def onclose(self, client):
        pass



class BasicChatServer(SocketServer):
    def __init__(self, on_message, client_timeout=100):
        self.on_message = on_message
        self.client_list = []
        self.client_timeout=client_timeout
        SocketServer.__init__(self)

    def onmessage(self, client, message):

        self.on_message(client, message)
        # print "Received From Client: " + str(message)
        #Sending message to all clients
        # self.send_to_all_except(client, message)
        # self.broadcast(message)

    def onopen(self, client):
        print "Client Connected"

    def onclose(self, client):
        print "Client Disconnected"
