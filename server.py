import socket

# Define the server address and port
server_address = ('localhost', 12345)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Server is listening on", server_address)

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print("Accepted connection from", client_address)

    # Receive data from the client
    received_data = client_socket.recv(1024).decode()
    print("Received data:", received_data)

    # Send data back to the client
    response = "Hello, client!"
    client_socket.sendall(response.encode())

    # Close the client connection
    client_socket.close()
