import socket
HOST = "127.0.0.1"
PORT = 65432
try:
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        print("[client] connected to server")
        msg = input("Enter message to send: ")
        s.sendall(msg.encode())
        data = s.recv(1024)
        print("[client] received:", data.decode())
    print("[client] done, closing")
except ConnectionRefusedError:
    print("[client] connection refused — is the server running?")
except Exception as e:
    print("[client] error:", e)
