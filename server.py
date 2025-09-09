import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

def handle_client(conn, addr):
    print(f"Client with port number {addr[1]} is served by “{threading.current_thread().name}”")
    with conn:
        while True:
            print("[server] waiting to receive data...")
            data = conn.recv(1024)
            if not data:      # client closed connection
                print("[server] no data received, closing connection.")
                break
            print(f"[server] received raw data: {data}")
            length_str = data[:3].decode()
            L = int(length_str)
            print(f"[server] extracted length: {L}")
            message = data[3:3+L].decode()
            print(f"[server] extracted message: '{message}'")
            print(f"[server] message length: {len(message)}")
            if message.strip().lower() == "hello":
                print("[server] received 'hello', sending greeting.")
                conn.sendall(b"Greetings from server!\n")
            else:
                print(f"[server] echoing back message: '{message}'")
                conn.sendall(message.encode())  # echo back
    print(f"[server] disconnected {addr}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[server] listening on {HOST}:{PORT}")

    while True:  # keep accepting new clients
        print("[server] waiting for a new connection...")
        conn, addr = server.accept()
        print(f"[server] connected by {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
