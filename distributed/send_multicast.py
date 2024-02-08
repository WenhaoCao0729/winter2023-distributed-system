import socket
import sys
import struct
import json

from time import sleep
from distributed import host, port

# Prepare the multicast address and port
multicast_address = (host.multicast, port.multicast_port)

def create_udp_socket():
    """Create a UDP socket configured for multicast with a set timeout and TTL."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    return sock

def sending_request_to_multicast():
    """Send server variables to multicast receivers (servers)."""
    sleep(1)  # Wait a bit before sending to ensure receivers are ready
    sock = create_udp_socket()

    message = json.dumps({
        'server_list': host.server_list,
        'leader': host.leader,
        'leader_crashed': host.leader_crashed,
        'replica_crashed': host.replica_crashed,
        'client_list': host.client_list
    }).encode()

    sock.sendto(message, multicast_address)
    print(f'\n[MULTICAST SENDER {host.myIP}] Sending data to Multicast Receivers {multicast_address}',
          file=sys.stderr)

    try:
        sock.recvfrom(host.buffer_size)
        print(f'[MULTICAST SENDER {host.myIP}] All Servers have been updated\n', file=sys.stderr)
        return True
    except socket.timeout:
        print(f'[MULTICAST SENDER {host.myIP}] Multicast Receiver not detected', file=sys.stderr)
        return False
    finally:
        sock.close()

def sending_join_chat_request_to_multicast():
    """Send a join chat request to the multicast group."""
    print(f'\n[MULTICAST SENDER {host.myIP}] Sending join chat request to Multicast Address {multicast_address}',
          file=sys.stderr)

    sock = create_udp_socket()
    message = json.dumps({'type': 'JOIN', 'data': ''}).encode()
    sock.sendto(message, multicast_address)

    try:
        data, _ = sock.recvfrom(host.buffer_size)
        decoded_data = json.loads(data.decode())
        host.leader = decoded_data['leader']
        return True
    except socket.timeout:
        print(f'[MULTICAST SENDER {host.myIP}] Multicast Receiver not detected -> Chat Server is offline.',
              file=sys.stderr)
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    # Example usage
    sending_request_to_multicast()
    # sending_join_chat_request_to_multicast() can be called based on the specific use case
