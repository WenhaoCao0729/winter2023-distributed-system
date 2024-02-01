# this is for all the host related functions
# this is the main file for the host

import socket


#get own ip address
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

#this is for all of the connection variables and  global IP variables and state variables
bufferSize = 1024
unicode = 'utf-8'
multicast = '224.0.0.0'
leader = ''
neighbour = ''
server_list = []
client_list = []



