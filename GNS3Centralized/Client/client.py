# DESCRIPTION:
# INPUTS:
# RETURNS:
# NOTES:

import os
import socket

ORCHESTRATOR_IP = "192.168.0.100"
SERVER_IP = "192.168.0.101"


# get client's IP address
ifconfig_info = os.popen('ifconfig eth0 | grep "inet" | cut -d: -f2').read()
IP = ifconfig_info.split()[1]
PORT = 23456

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))

while True:
    server_socket.listen()
    connection, client_address = server_socket.accept()
    data, address = connection.recv(1024)
    connection.sendall(data)
    connection.close()

    # listen for patient id from orch

    # get data for that patient

    # send data & start timer

    # listen for diagnosis from server

    # stop timer

    # send results to orch
