import socket
import sys
import threading
import queue
from distributed import host, port, receive_multicast, send_multicast, heartbeat, signature, state_sync

class ChatServer:
    def __init__(self):
        self.host_address = (host.myIP, port.server_port)
        self.sock = self.create_server_socket()
        self.message_queue = queue.Queue()
        self.client_list = []
        self.initialize_server()
        self.private_key, self.public_key = signature.generate_key_pair()
        self.other_servers = [('127.0.0.1', 5001), ('127.0.0.1', 5002)]
        threading.Thread(target=self.listen_for_state_updates, daemon=True).start()
        # Start status synchronization monitoring

    def create_server_socket(self):
        """Create and configure the server socket."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock

    def printer(self):
        """Print server and client list information."""
        print(f'\n[SERVER] Server List: {host.server_list} ==> Leader: {host.leader}'
              f'\n[SERVER] Client List: {len(self.client_list)}'
              f'\n[SERVER] Neighbour ==> {host.neighbour}\n', file=sys.stderr)

    def send_messages_to_clients(self):
        """Send all messages from the queue to all connected clients."""
        while not self.message_queue.empty():
            # The loop continues as long as the message queue is not empty
            message = self.message_queue.get()
            signed_message = signature.sign_message(self.private_key, message)
            for client in self.client_list:
                client.send(message.encode(host.unicode))
                client.send(signed_message)     # Send original message and signature

    def client_handler(self, client, address):
        """Handle incoming messages from connected clients."""
        while True:
            try:
                data = client.recv(host.buffer_size)
                signature_data = client.recv(host.buffer_size)
                # Receive messages and signatures
                if not data:
                    self.handle_client_disconnection(client, address)
                    break

                if signature.verify_signature(self.public_key, data.decode(host.unicode), signature_data):
                    # Verify signature
                    message = data.decode(host.unicode)
                    self.message_queue.put(f'{address} said: {data.decode(host.unicode)}')
                    self.update_state(f'{address} said: {message}')  # update state
                    print(f'Message from {address} ==> {data.decode(host.unicode)}')

                else:
                    print("Invalid signature detected")
            except Exception as e:
                print(e)
                break

    def update_state(self, new_state):
        """Update server status and notify other server instances"""
        # Add new status (message) to message queue
        self.message_queue.put(new_state)

        # Create a dictionary representing status updates
        state_update = {
            'type': 'new_message',
            'content': new_state
        }
        # Send updates to other server instances
        state_sync.send_state_update(new_state, self.other_servers)

    def listen_for_state_updates(self):
        """Listen for status updates from other server instances"""
        state_sync.listen_for_state_updates(5000, self.handle_state_update)

    def handle_state_update(self, state_update):
        """Handle received status updates"""
        if state_update['type'] == 'new_message':
            # Add new received messages to the message queue
            self.message_queue.put(state_update['content'])

            # You can also perform other necessary synchronization operations here
            print(f"Received new message update: {state_update['content']}")

    def handle_client_disconnection(self, client, address):
        """Handle client disconnection."""
        print(f'{address} disconnected')
        self.client_list.remove(client)
        client.close()
        self.message_queue.put(f'\n{address} disconnected\n')

    def start_server(self):
        """Bind the TCP server socket and listen for connections."""
        self.sock.bind(self.host_address)
        self.sock.listen()
        print(f'\n[SERVER] Starting and listening on {self.host_address}', file=sys.stderr)
        while True:
            client, address = self.sock.accept()
            self.client_list.append(client)
            threading.Thread(target=self.client_handler, args=(client, address), daemon=True).start()

    def initialize_server(self):
        """Initialize the server and start the necessary threads."""
        if not send_multicast.sending_request_to_multicast():
            host.server_list.append(host.myIP)
            host.leader = host.myIP

        threading.Thread(target=receive_multicast.start_multicast_receiver, daemon=True).start()
        threading.Thread(target=heartbeat.start_heartbeat, daemon=True).start()
        threading.Thread(target=self.start_server, daemon=True).start()

        try:
            while True:
                if host.leader == host.myIP and (host.network_changed or host.replica_crashed):
                    send_multicast.sending_request_to_multicast()
                    host.leader_crashed = False
                    host.network_changed = False
                    host.replica_crashed = ''
                    self.printer()
                elif host.leader != host.myIP and host.network_changed:
                    host.network_changed = False
                    self.printer()
                self.send_messages_to_clients()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            self.sock.close()

if __name__ == '__main__':
    server = ChatServer()
