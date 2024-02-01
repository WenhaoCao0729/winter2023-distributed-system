import socket

class DistributedSystemClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
            print("Connected to the server.")
        except ConnectionRefusedError:
            print("Failed to connect to the server.")

    def send_message(self, message):
        try:
            self.socket.sendall(message.encode())
            response = self.socket.recv(1024).decode()
            print("Response from server:", response)
        except ConnectionResetError:
            print("Connection with the server was reset.")

    def disconnect(self):
        self.socket.close()
        print("Disconnected from the server.")

# Usage example
client = DistributedSystemClient("127.0.0.1", 5000)
client.connect()
client.send_message("Hello, server!")
client.disconnect()
