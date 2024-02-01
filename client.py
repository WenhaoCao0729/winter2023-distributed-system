import socket
import threading
import sys
from time import sleep
from distributed import host, port, send_multicast

class ChatClient:
    def __init__(self):
        self.sock = None
        self.connect_to_server()

    def connect_to_server(self):
        """Connect to the chat server leader via multicast discovery."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_exists = send_multicast.sending_join_chat_request_to_multicast()
        if server_exists:
            leader_address = (host.leader, port.server_port)
            print(f'Connecting to server leader at {leader_address}')
            self.sock.connect(leader_address)
            self.sock.send('JOIN'.encode(host.unicode))
            print("You've joined the chat room. Start chatting now!")
        else:
            print("No server available. Please try joining later.")
            sys.exit(0)

    def send_messages(self):
        """Send messages to the server."""
        while True:
            message = input("")
            try:
                self.sock.send(message.encode(host.unicode))
            except Exception as e:
                print(e)
                break

    def receive_messages(self):
        """Receive messages from the server."""
        while True:
            try:
                data = self.sock.recv(host.buffer_size)
                if not data:
                    print("\nChat server unavailable. Reconnecting to new server leader in 3 seconds.")
                    self.sock.close()
                    sleep(3)
                    self.connect_to_server()
                else:
                    print(data.decode(host.unicode))
            except Exception as e:
                print(e)
                break

    def run(self):
        """Start threads for sending and receiving messages."""
        threading.Thread(target=self.send_messages, daemon=True).start()
        threading.Thread(target=self.receive_messages, daemon=True).start()
        try:
            while True: sleep(1)  # Keep the main thread alive.
        except KeyboardInterrupt:
            print("\nYou left the chat room.")
            self.sock.close()
            sys.exit(0)

if __name__ == '__main__':
    client = ChatClient()
    client.run()
