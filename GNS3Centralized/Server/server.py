# DESCRIPTION:
# INPUTS:
# RETURNS:
# NOTES:

import socket
import json

ORCHESTRATOR_IP = "192.168.0.100"
SERVER_IP = "192.168.0.101"

ORCHESTRATOR_PORT = 33333
SERVER_PORT = 44444

# Get list of ports and ips to communicate with clients
CLIENT_IPS = []
CLIENT_PORTS = []
for i in range(5):
    ip = 100 + i
    CLIENT_IPS.append("192.168.1." + str(ip))
    CLIENT_IPS.append("192.168.2." + str(ip))
    CLIENT_PORTS.append(41000 + ip)
    CLIENT_PORTS.append(42000 + ip)

# Set up sockets
server_client_sockets = []
for server_client_port in CLIENT_PORTS:
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind((SERVER_IP, server_client_port))
    server_client_sockets.append(temp_socket)

server_orch_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_orch_socket.bind((SERVER_IP, SERVER_PORT))

while True:
    server_orch_socket.listen()
    connection, client_address = server_orch_socket.accept()
    data, address = connection.recv(1024)
    received = {"received": data, "status": "model-selected"}
    data = json.dumps(received)
    connection.sendall(data)
    connection.close()

    # listen for testing_fold from orch

    # listen for num clients from orch

    # select appropriate model

    # listen for data from clients

    # for each client, take data, put in model, get diagnosis, send to client

    # wait for next fold from orch
