import socket
import os

def start_server(host='0.0.0.0', port=12346):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")
    
    clients = []
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            clients.append(client_socket)
            client_socket.send(b"Welcome to the server!")
            handle_client(client_socket, clients)
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server_socket.close()

def handle_client(client_socket, clients):
    try:
        while True:
            file_info = client_socket.recv(1024).decode()
            if not file_info:
                break
            
            file_name, file_size = file_info.split(':')
            file_size = int(file_size)
            
            print(f"Receiving file: {file_name} of size: {file_size} bytes")
            
            with open(file_name, 'wb') as file:
                received_size = 0
                while received_size < file_size:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    received_size += len(data)
            
            print(f"Received file: {file_name}")
            broadcast(file_name, file_size, clients, client_socket)
    finally:
        client_socket.close()

def broadcast(file_name, file_size, clients, source_socket):
    for client in clients:
        if client != source_socket:
            try:
                client.send(f"{file_name}:{file_size}".encode())
                with open(file_name, 'rb') as file:
                    while (data := file.read(1024)):
                        client.send(data)
            except:
                clients.remove(client)

if __name__ == "__main__":
    start_server()
