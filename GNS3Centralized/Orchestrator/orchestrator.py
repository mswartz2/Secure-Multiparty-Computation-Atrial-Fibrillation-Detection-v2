# DESCRIPTION:
# INPUTS: fold_n - the fold to use for testing (0-9)
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
    CLIENT_PORTS.append(31000 + ip)
    CLIENT_PORTS.append(32000 + ip)

# Set up sockets
orch_client_sockets = []
for orch_client_port in CLIENT_PORTS:
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind((ORCHESTRATOR_IP, orch_client_port))
    orch_client_sockets.append(temp_socket)

orch_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Test for each of the test folds
for testing_fold in range(10):
    # make server connection
    orch_server_socket.connect((SERVER_IP, SERVER_PORT))
    # send testing_fold to server
    server_msg = {"testing_fold": testing_fold}
    data = json.dumps(server_msg)
    orch_server_socket.sendall(bytes(data, encoding="utf-8"))

    received = orch_server_socket.recv(1024)
    received = received.decode("utf-8")
    print(received)

    # make client connection

    # count number of patients in testing_fold

    # send number of patients to server

    # send patient # to clients

    # wait for replies
    # while True:
    #     server_socket.listen()
    #     connection, client_address = server_socket.accept()
    #     data, address = connection.recv(1024)
    #     connection.sendall(data)
    #     connection.close()
