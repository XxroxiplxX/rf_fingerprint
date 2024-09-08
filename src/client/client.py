import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Received: {message.decode()}")
        except:
            break

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    try:
        while True:
            message = input("Enter message: ")
            client_socket.send(message.encode())
    except KeyboardInterrupt:
        print("Disconnecting from server.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    server_ip = '0.0.0.0'  # Replace with the actual server IP
    server_port = 12345
    start_client(server_ip, server_port)
