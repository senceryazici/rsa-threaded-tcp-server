import socket
import time
import json
loop_rate = 1000

host = "0.0.0.0"
port = 9090


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

# Request Connection
conn_req = {
    "id":"AAAACCCC",
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

foward_message = {
    "id":id,
    "to": ["AAAAAAAA", "BBBBBBBB"],
    "type":"CARRY_MESSAGE",
    "content":"THIS IS A MESSAGE FOR AAAAAAA AND BBBBBBBB"
}
client.send(json.dumps(foward_message) + "\n")
time.sleep(1)
def keep_alive(_client):
    dict = {
        "id":id,
        "type":"KEEP_ALIVE"
    }
    _client.send(json.dumps(dict) + '\n')
    return json.dumps(dict)

while True:
    print "KEEP_ALIVE:", keep_alive(client)
    time.sleep(2)
time.sleep(1000)
client.close()
