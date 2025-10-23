import socket

def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            # First, receive the length prefix (exactly 3 bytes)
            length_bytes = client_socket.recv(3)
            if not length_bytes:
                break
            length_str = length_bytes.decode('utf-8')
            message_length = int(length_str)

            print(f"Received length prefix: '{length_str}' -> {message_length} bytes")

            # Now receive the message content (exactly message_length bytes)
            message_bytes = client_socket.recv(message_length)
            message = message_bytes.decode('utf-8')

            print(f"Received message: '{message}'")

            # Send acknowledgment
            response = f"Message received: '{message}' (length: {message_length})"
            client_socket.sendall(response.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_server()

# Explanation:
# This server program demonstrates receiving messages with length prefixing.
# - Accept connection: Waits for client connections.
# - Extract length: Reads the first 3 bytes and converts to integer (message length).
# - Read message: Receives exactly the number of bytes specified by the length.
# - Process message: Decodes and prints the received message.
# - Send response: Acknowledges receipt back to the client.
# This approach ensures proper handling of variable-length messages by using a fixed-size header for length information.