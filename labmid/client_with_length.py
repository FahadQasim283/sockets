import socket

def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message = input("Enter message to send: ")

    # Compute length of message
    length = len(message.encode('utf-8'))  # Length in bytes
    length_str = str(length).zfill(3)  # Pad to 3 digits with leading zeros

    # Prepend length to message
    full_message = length_str + message

    print(f"Original message: '{message}'")
    print(f"Message length: {length} bytes")
    print(f"Padded length: '{length_str}'")
    print(f"Full message to send: '{full_message}'")

    # Send the message
    client_socket.sendall(full_message.encode('utf-8'))

    # Receive response from server
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
