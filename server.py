import socket

HOST = "127.0.0.1"
PORT = 8081

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[server] listening on {HOST}:{PORT}")

    while True:  # keep accepting new clients
        conn, addr = server.accept()
        print(f"[server] connected by {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:      # client closed connection
                    break
                print(f"[server] received raw data: {data}")
                length_str = data[:3].decode()
                L = int(length_str)
                print(f"[server] length of data: {L}")
                message = data[3:3+L].decode()
                if message.strip().lower() == "hello":
                    conn.sendall(b"Greetings from server!\n")
                else:
                    conn.sendall(message.encode())  # echo back
        print(f"[server] disconnected {addr}")
