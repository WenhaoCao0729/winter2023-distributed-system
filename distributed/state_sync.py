import socket
import json

def send_state_update(state, server_addresses):
    """Send status updates to other server instances"""
    message = json.dumps(state).encode('utf-8')
    for address in server_addresses:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(message, address)
        except Exception as e:
            print(f"Error sending state update to {address}: {e}")

def listen_for_state_updates(port, handle_update):
    """Listen for status updates from other server instances"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('', port))
        while True:
            data, _ = sock.recvfrom(1024)
            state_update = json.loads(data.decode('utf-8'))
            handle_update(state_update)
