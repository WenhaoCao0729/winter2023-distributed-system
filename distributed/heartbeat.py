import socket
import sys
from time import sleep
import host, port, leader_election

def establish_connection(address):
    """Attempt to establish a TCP connection to the given address."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(0.5)
        try:
            sock.connect(address)
            return True
        except socket.error:
            return False

def handle_neighbour_failure(neighbour):
    """Handle the failure of a neighbour server."""
    host.server_list.remove(neighbour)
    if host.leader == neighbour:
        print(f'[HEARTBEAT] Server Leader {neighbour} crashed', file=sys.stderr)
        host.leader_crashed = True
        host.leader = host.myIP  # Assign own IP address as new Server Leader
        host.network_changed = True
    else:
        print(f'[HEARTBEAT] Server Replica {neighbour} crashed', file=sys.stderr)
        host.replica_crashed = 'True'

def start_heartbeat():
    """Periodically checks the availability of the server's neighbour."""
    while True:
        sleep(3)  # Wait before each heartbeat check to reduce network congestion
        
        # Get the server's neighbour using the leader election algorithm.
        neighbour = leader_election.start_leader_election(host.server_list, host.myIP)
        if neighbour:
            host_address = (neighbour, port.server)
            if not establish_connection(host_address):
                handle_neighbour_failure(neighbour)

if __name__ == "__main__":
    start_heartbeat()
