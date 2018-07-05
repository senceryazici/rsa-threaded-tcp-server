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
from DataTypes.Types import *


class Client(object):
    def __init__(self):
        self.socket = None
        self.id = None
        self.banned = False
        self.messages = []
        # Every connected client joins all group.
        self.groups = ["@all"]

    def info(self):
        print "Client", self.socket, "ID:", self.id

    def new_msg(self, msg):
        self.messages.append(msg)
        self.log(msg)

    def log(self, msg):
        file = open("ClientLogs/" + self.id + ".log", 'a+')
        file.write("[" + str(time.time()) + "]:[" + time.ctime() + "]:" + msg + "\n")
        file.close()

class SocketServer(socket.socket):
    def __init__(self):
        socket.socket.__init__(self)
        #To silence- address occupied!!
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.bind(('0.0.0.0', 9090))
        self.listen(5)
        self.clients = []
        self.blacklist = []
        self.status = True
        self.allow_new_connections = True
        self.groups = ["@all", "@todo"]
        self.shuttingdown = False

    def ok(self):
        return self.status

    def run(self):
        print "[ START ] Server started"
        self.load_blacklist()
        try:
            self.accept_clients()
        except Exception as ex:
            print "[ Exception ]", ex
        finally:
            for client in self.clients:
                client.socket.close()
            print "[ END ] Server closed"
            self.status = False
            self.close()
            thread.exit()

    def shutdown(self):
        self.allow_new_connections = False
        self.shuttingdown = True
        time.sleep(0.1)
        for client in self.clients:
            client.socket.close()
        self.close()
        thread.exit()


    def accept_clients(self):
        while self.allow_new_connections:
            (clientsocket, address) = self.accept()
            # print self.clients
            clientsocket.settimeout(self.client_timeout)
            #Adding client to clients list
            print "[ INFO ] Waiting Client Connection Request"
            data = clientsocket.recv(1024)
            data = data.replace("\r\n", "")
            data = data.replace("\n", "")
            data = data.replace("\r", "")

            conn_req = json.loads(data)
            print "[ INFO ] Client sent message:", conn_req

            if conn_req["type"] != RequestTypes.CONNECTION_REQUEST:
                print "[ INFO ] Client sent invalid message."
                continue
            else:
                if conn_req["id"] in self.blacklist:
                    conn_info = {
                        "id": conn_req["id"],
                        "type": ConfirmationTypes.CONNECTION_REFUSED
                    }
                    print "[ INFO ] ID:", conn_req["id"], "is banned."
                    client.socket.send(json.dumps(conn_info))
                    client.socket.close()
                else:
                    # Construct Client
                    client = Client()
                    client.socket = clientsocket
                    client.id = conn_req["id"]


                    self.clients.append(client)
                    conn_info = {
                        "timeout": self.client_timeout,
                        "id": client.id,
                        "rsa-public-key": "AAA",
                        "type": InfoTypes.CONNECTION_INFO
                    }

                    client.socket.send(json.dumps(conn_info))
                    self.onopen(client)
                    # Start listening
                    thread.start_new_thread(self.recieve, (client,))

    def recieve(self, client):
        connection = {
            "id": client.id,
            "type": InfoTypes.CONNECTION_STATUS,
            "content": True
        }

        client.log(json.dumps(connection))
        timeout_flag = False
        while not timeout_flag and not client.banned and not self.shuttingdown:
            try:
                data = client.socket.recv(2048)
                if data == '':
                    break
                #Message Received
                data = data.replace("\r\n", "")
                data = data.replace("\n", "")
                data = data.replace("\r", "")
                client.new_msg(data)
                data_dict = json.loads(data)

                # *** MAIN MESSAGE GROUPING *** #
                if data_dict["type"] == MessageTypes.CARRY_MESSAGE:
                    print "[ INFO ] Fowarding Message from:", data_dict["id"], "to", data_dict["to"]

                    for to in data_dict["to"]:
                        if str(to) in self.groups:
                            # Group fowarding algorithm
                            msg = {
                                "id": data_dict["id"],
                                "from": data_dict["id"],
                                "to": str(to),
                                "content": data_dict["content"],
                                "type": MessageTypes.TEXT_MESSAGE
                            }
                            group = to
                            self.send_to_groups(json.dumps(msg), group)
                        else:
                            self.foward_message(data_dict, to)

                elif data_dict["type"] == RequestTypes.SERVER_INFO_REQUEST:
                    print "[ INFO ]", data_dict["id"], "requested server status."
                    # TODO: Permission check
                    print "[ INFO ] Request Confirmed for", data_dict["id"]
                    msg = self.active_connections()
                    #msg["id"] = data_dict["id"]
                    self.send_to_client(data_dict["id"], json.dumps(msg))

                elif data_dict["type"] == TcpTypes.KEEP_ALIVE:
                    pass
                elif data_dict["type"] == RequestTypes.DISCONNECTION_REQUEST:
                    # Exit while loop
                    break
                else:
                    self.onmessage(client, data)
                # *** MAIN MESSAGE GROUPING *** #

            except socket.timeout:
                timeout_flag = True
                print "[ INFO ] Timeout reached, Client:", client.id, "disconnecting"


        # Disconnection Stage
        disconnection = {
            "id": client.id,
            "type": InfoTypes.CONNECTION_STATUS,
            "content": False
        }
        client.log(json.dumps(disconnection))
        #Removing client from clients list
        self.clients.remove(client)
        #Client Disconnected
        self.onclose(client)
        #Closing connection with client
        client.socket.close()
        #Closing thread
        thread.exit()

    def foward_message(self, message_received, target_client):

        dict = {
            "id": message_received["id"],
            "from": message_received["id"],
            "to": target_client,
            "content": message_received["content"],
            "type": MessageTypes.TEXT_MESSAGE
        }
        self.send_to_client(target_client, json.dumps(dict))

    def send_to_client(self, client_id, message):
        # Sending message only to a client
        for c in self.clients:
            if c.id == client_id:
                c.socket.send(message + "\n")
    def send_to_all_except(self, client, message):
        # Sending message to all except a client
        for c in self.clients:
            if c != client:
                c.socket.send(message)

    def send_to_groups(self, msg, group):
        for client in self.clients:
            if group in client.groups:
                client.socket.send(msg + "\n")

    def broadcast(self, message):
        #Sending message to all clients
        for client in self.clients:
            client.socket.send(message + "\n")

    def onopen(self, client):
        pass

    def onmessage(self, client, message):
        pass

    def onclose(self, client):
        pass

    def search_client_by_id(self, id):
        for client in self.clients:
            if client.id == id:
                return client
            else:
                return None

    def bann_client(self, id):
        client = self.search_client_by_id(id)
        if not client is None:
            client.banned = True
            print "[ INFO ] Active client with ID: ", id, " banned."
        else:
            pass
        print "[ INFO ] Client:", id, "Added to blacklist."
        if not id in self.blacklist:
            self.blacklist.append(id)
            self.save_blacklist()

    def load_blacklist(self):
        file = open("Blacklist/blacklist.json", 'r')
        json_str = file.read()
        file.close()
        dictionary = json.loads(json_str)
        arr = dictionary["clients"]

        self.blacklist = []
        for element in arr:
            self.blacklist.append(str(element))
        print "[ INFO ] Blacklist Loaded."

    def save_blacklist(self):
        file = open("Blacklist/blacklist.json", 'w')
        file.truncate()
        dictionary = {
            "clients": self.blacklist
        }
        # Stylize json string
        json_str = json.dumps(dictionary)
        json_str = json_str.replace(" ", "")
        json_str = json_str.replace("[", "[\n        ")
        json_str = json_str.replace("]", "\n    ]\n")
        json_str = json_str.replace("}", "}\n")
        json_str = json_str.replace("{", "{\n    ")
        json_str = json_str.replace(",", ",\n        ")
        json_str = json_str.replace(":", ":\n    ")
        file.write(json_str)
        file.close()
        print "[ INFO ] Blacklist database updated."

    def active_connections(self):
        dict = {
            "clients": map(lambda x : x.id, self.clients),
            "type": InfoTypes.SERVER_INFO
        }
        return dict



class BasicChatServer(SocketServer):
    def __init__(self, on_message, client_timeout=100):
        self.on_message = on_message
        self.client_list = []
        self.client_timeout=client_timeout
        SocketServer.__init__(self)

    def onmessage(self, client, message):
        self.on_message(client, message)

    def onopen(self, client):
        print "[ INFO ] Client Connected with ID: ", client.id

    def onclose(self, client):
        print "[ INFO ] Client Disonnected with ID: ", client.id
