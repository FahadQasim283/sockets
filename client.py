import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

def client_thread(msg):
    print(f"[client] starting client thread for message '{msg}'...")
    print(f"[client] attempting to connect to {HOST}:{PORT}")
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            print(f"[client] connected to server for '{msg}'")
            print(f"[client] message: '{msg}'")
            L = len(msg)
            print(f"[client] message length: {L}")
            length_str = str(L).zfill(3)
            print(f"[client] length string (zero-padded): '{length_str}'")
            full_msg = length_str + msg
            print(f"[client] full message to send: '{full_msg}'")
            s.sendall(full_msg.encode())
            print(f"[client] message sent for '{msg}', waiting for response...")
            data = s.recv(1024)
            print(f"[client] received for '{msg}':", data.decode())
        print(f"[client] done for '{msg}', closing")
    except ConnectionRefusedError:
        print(f"[client] connection refused for '{msg}' — is the server running?")
    except Exception as e:
        print(f"[client] error for '{msg}':", e)

# List of messages to send
messages = ["hello", "world", "test message"]

threads = []
for msg in messages:
    thread = threading.Thread(target=client_thread, args=(msg,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("[client] all client threads done")