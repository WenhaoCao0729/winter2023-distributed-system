import socket

# get own ip address
def get_own_ip(target_server="8.8.8.8", target_port=80):
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect((target_server, target_port))
        return sock.getsockname()[0]

# initialize connection variables
def initialize_connection_variables():
    
    buffer_size = 1024
    unicode = 'utf-8'
    return buffer_size, unicode

# initialize global variables
def initialize_global_variables():
    
    multicast = '224.0.0.0'
    leader = ''
    neighbour = ''
    server_list = []
    client_list = []
    client_running = False
    network_changed = False
    leader_crashed = ''
    replica_crashed = ''
    return multicast, leader, neighbour, server_list, client_list, client_running, network_changed, leader_crashed, replica_crashed

# get own ip address
myIP = get_own_ip()

# initialize variables
buffer_size, unicode = initialize_connection_variables()
multicast, leader, neighbour, server_list, client_list, client_running, network_changed, leader_crashed, replica_crashed = initialize_global_variables()


