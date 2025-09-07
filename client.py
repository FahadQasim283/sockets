import socket

HOST = "127.0.0.1"
PORT = 8081

try:
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        print("[client] connected to server")

        # take input from user
        msg = input("Enter message to send: ")
        L = len(msg)
        length_str = str(L).zfill(3)
        full_msg = length_str + msg
        s.sendall(full_msg.encode())

        # wait for reply
        data = s.recv(1024)
        print("[client] received:", data.decode())

    print("[client] done, closing")
except ConnectionRefusedError:
    print("[client] connection refused — is the server running?")
except Exception as e:
    print("[client] error:", e)
