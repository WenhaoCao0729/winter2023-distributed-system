# this is a distributed Server on localhost for the chatroom

# import Modules
import socket
import sys
import threading
import queue

from distributed import host, port

#create the TCP socket
#create own ip address
#bind the socket to the port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host_address = (host.get_ip(), port.multicast_server_port)

#create a Queue for the messages
FIFO_message_queue = queue.Queue()

#bind the socket to the port
sock.bind(host_address)
print("Server started on IP address: " + host.get_ip() + " and port: " + str(port.multicast_server_port))

#listen for incoming connections
sock.listen(5)

#this is the thread for the server
def server_thread():
    while True:
        #wait for a connection
        print("Waiting for a connection...")
        connection, client_address = sock.accept()
        try:
            print("Connection from: " + str(client_address))

            #receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(port.get_buffer_size())
                if data:
                    print("Received: " + str(data))
                    #put the data into the FIFO queue
                    FIFO_message_queue.put(data)
                else:
                    print("No more data from: " + str(client_address))
                    break

        finally:
            #clean up the connection
            connection.close()


            
