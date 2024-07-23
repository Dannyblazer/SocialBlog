import socket

HOST = "127.0.0.1" # Routes to Local Host (Standard loopback interface address) Use "" to accept connections from all IPV4 interfaces
PORT = 65432 # Listening on Non Privilleged port (ports > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

