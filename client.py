import socket

HOST = "127.0.0.1"
PORT = 65432
print("[client] starting client...")
print(f"[client] attempting to connect to {HOST}:{PORT}")
try:
  with socket.create_connection((HOST, PORT), timeout=5) as s:
    print("[client] connected to server")
    msg = input("Enter message to send: ")
    print(f"[client] message entered: '{msg}'")
    L = len(msg)
    print(f"[client] message length: {L}")
    length_str = str(L).zfill(3)
    print(f"[client] length string (zero-padded): '{length_str}'")
    full_msg = length_str + msg
    print(f"[client] full message to send: '{full_msg}'")
    s.sendall(full_msg.encode())
    print("[client] message sent, waiting for response...")
    data = s.recv(1024)
    print("[client] received:", data.decode())
  print("[client] done, closing")
except ConnectionRefusedError:
  print("[client] connection refused — is the server running?")
except Exception as e:
  print("[client] error:", e)