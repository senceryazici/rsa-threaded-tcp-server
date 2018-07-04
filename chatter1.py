import socket
import time
import json
import thread
import random, string
loop_rate = 1000

host = "0.0.0.0"
port = 9090


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

# Request Connection
_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
conn_req = {
    "id": _id,
    "type":"CONNECTION_REQUEST"
}
print "sending",json.dumps(conn_req)
client.send(json.dumps(conn_req) + "\n")

# Receive Status
json_str = client.recv(1024)
print "Received Board Info: ", json_str
connection_info = json.loads(json_str)

if connection_info["type"] == "CONNECTION_INFO":
    client.settimeout(connection_info["timeout"])
    id = connection_info["id"]
    # client.id = connection_info["ID"]
    server_public_key = connection_info["rsa-public-key"]
elif connection_info["type"] == "CONNECTION_REFUSED":
    print "WOW"
    pass


def keep_alive(_client):
    dict = {
        "id":id,
        "type":"KEEP_ALIVE"
    }
    _client.send(json.dumps(dict) + '\n')
    return json.dumps(dict)



def recv_thread():
    while True:
        json_str = client.recv(2048)
        json_str.replace("\n", "")
        dictionary = json.loads(json_str)
        if dictionary["from"] != id:
            print dictionary["from"] + ":", dictionary["content"]

        time.sleep(0.01)

thread.start_new_thread(recv_thread, ())
print "YOU ARE SIGNED IN AS", id
while True:
    data = raw_input("-$")
    if not ":" in data:
        targets = ["@all"]
        msg = data
    else:
        data_arr = data.split(":")
        msg = data_arr[1]
        target = data_arr[0]
        targets = target.split(",")

    dict = {
        "id": id,
        "type": "CARRY_MESSAGE",
        "to": targets,
        "content": msg
    }
    client.send(json.dumps(dict) + "\n")
client.close()
