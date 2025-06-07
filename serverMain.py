import socket

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 1000))
server_socket.listen(1)
print("Waiting for connection...")

conn, addr = server_socket.accept()
print("Connected by", addr)
data = conn.recv(1024).decode()
print("Received:", data)

conn.close()
