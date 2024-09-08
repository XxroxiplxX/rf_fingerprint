import socket

def start_server(host='0.0.0.0', port=12345):
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
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Received: {message.decode()}")
            broadcast(message, clients, client_socket)
    finally:
        client_socket.close()

def broadcast(message, clients, source_socket):
    for client in clients:
        if client != source_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

if __name__ == "__main__":
    start_server()
