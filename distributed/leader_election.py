import socket

from distributed import host

#Sort IP addresses in ascending order to form a ring.
def form_ring(members):
    
    # Convert IP addresses to their binary forms, sort, and then convert back to their standard notation.
    sorted_binary_ring = sorted(socket.inet_aton(member) for member in members)
    return [socket.inet_ntoa(node) for node in sorted_binary_ring]


#Find the neighbouring server in the ring based on the specified direction.
def get_neighbour(members, current_member_ip, direction='left'):
    
    try:
        current_index = members.index(current_member_ip)
        # Calculate next index for 'left' or previous index for 'right' direction with wrapping.
        next_index = (current_index + 1) % len(members) if direction == 'left' else (current_index - 1) % len(members)
        return members[next_index]
    except ValueError:
        # Current member IP not in members list.
        return None

#Initiate the leader election process among servers.
def start_leader_election(server_list, leader_server):
   
    ring = form_ring(server_list)
    # Use 'right' direction to find the next server in the ring as the neighbour.
    neighbour = get_neighbour(ring, leader_server, 'right')
    # Determine if the current host is the leader.
    return None if neighbour == host.myIP else neighbour
