# this is a distributed Client on localhost for the chatroom

# import Modules
import socket
import threading
import os

from distributed import host, port

# create the TCP socket
# create own ip address
# bind the socket to the port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host_address = (host.get_ip(), port.multicast_server_port)




# function for sending messages to the Server
def send_message():
    while True:
        #get the message from the user
        message = input("Enter a message: ")
        #send the message to the Server
        sock.sendall(bytes(message, host.get_unicode()))
        #check if the user wants to quit
        if message == 'q':
            break

