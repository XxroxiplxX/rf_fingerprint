import socket
#import struct

def start_server(host="0.0.0.0", port=12345, buffer_size=1024):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Serwer nasłuchuje na {host}:{port}")
    conn, addr = server_socket.accept()
    print(f"Połączono z {addr}")

    # Odbieranie długości nazwy pliku (4 bajty)
    #file_name_length_data = conn.recv(4)
    #file_name_length = struct.unpack("!I", file_name_length_data)[0]

    # Odbieranie nazwy pliku
    file_name = conn.recv(11).decode()
    print(f"Przesłany plik: {file_name}")

    # Odbieranie zawartości pliku i zapisywanie do pliku lokalnego
    with open(file_name, "wb") as f:
        while True:
            data = conn.recv(buffer_size)
            if not data:
                break
            f.write(data)

    print(f"Plik {file_name} zapisany pomyślnie.")
    conn.close()
    server_socket.close()
    print("Serwer zamknięty.")

if __name__ == "__main__":
    start_server()
