import socket
import struct
import json
import sys

from distributed import host, port

def create_udp_socket():
    """Create a UDP socket configured for multicast."""
    multicast_ip = host.multicast
    server_address = ('', port.multicast_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(multicast_ip)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock

def process_received_data(data, address, sock):
    """Process the data received from the multicast group."""
    print(f'\n[MULTICAST RECEIVER {host.myIP}] Received data from {address}\n', file=sys.stderr)
    decoded_data = json.loads(data.decode())
    host.server_list.append(address[0])
    print(host.myIP)
    print(host.server_list)
    print(host.leader)
    print('aaaaaaa' + address[0])
    # print(type(host.myIP))
    # print(type(host.server_list[0]))
    # print('1')

    message_type = decoded_data.get('type')
    # access safety 'type'

    # if host.leader == host.myIP and decoded_data['type'] == 'JOIN':
    # if host.leader == host.myIP == 'JOIN':
    if host.leader == host.myIP and message_type == 'JOIN':
        handle_join_request(address, sock)
        print(host.server_list[0])
    elif 'servers' in decoded_data and not decoded_data['servers']:
        handle_server_join(address, sock)
        print('2')
    elif decoded_data.get('leader') and host.leader != host.myIP or decoded_data.get('crashed'):
        update_server_state(decoded_data, address, sock)
        print('3')

def handle_join_request(address, sock):
    """Handle a join request from a client."""
    message = json.dumps({'leader': host.leader, 'data': ''}).encode()
    sock.sendto(message, address)
    print(f'[MULTICAST RECEIVER {host.myIP}] Client {address} wants to join the Chat Room\n', file=sys.stderr)

def handle_server_join(address, sock):
    """Handle a new server joining the multicast group."""
    if address[0] not in host.server_list:
        host.server_list.append(address[0])
        sock.sendto('ack'.encode(), address)
        host.network_changed = True

def update_server_state(data, address, sock):
    """Update server state based on received data."""
    host.server_list = data.get('servers', [])
    host.leader = data.get('leader', '')
    host.client_list = data.get('clients', [])
    print(f'[MULTICAST RECEIVER {host.myIP}] All Data have been updated', file=sys.stderr)
    sock.sendto('ack'.encode(), address)
    host.network_changed = True

def update_server_list(data, address, sock):
    """Update server list every 2s."""
    host.server_list = data.get('servers', [])
    host.leader = data.get('leader', '')
    host.client_list = data.get('clients', [])
    # print(f'[MULTICAST RECEIVER {host.myIP}] All Data have been updated', file=sys.stderr)
    sock.sendto('ack'.encode(), address)
    host.network_changed = True

def start_multicast_receiver():
    """Start the multicast receiver to listen for messages."""
    sock = create_udp_socket()
    print(f'\n[MULTICAST RECEIVER {host.myIP}] Starting UDP Socket and listening on Port {port.multicast_port}',
          file=sys.stderr)
    try:
        while True:
            data, address = sock.recvfrom(host.buffer_size)
            process_received_data(data, address, sock)
    except KeyboardInterrupt:
        print(f'\n[MULTICAST RECEIVER {host.myIP}] Closing UDP Socket', file=sys.stderr)
        sock.close()

if __name__ == "__main__":
    start_multicast_receiver()
