import socket

HOST = "127.0.0.1" # Server Hostname or IPAddress
PORT = 65432 # Port Used on the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello World Blaze")
    data = s.recv(1024)

print(f"Received {data!r}")
