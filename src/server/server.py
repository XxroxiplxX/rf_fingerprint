import socket
import numpy as np
import struct
import csv

def start_server(host='0.0.0.0', port=12345):
    # Tworzenie socketu serwera
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Serwer nasłuchuje...")

    # Akceptowanie połączenia od klienta
    client_socket, address = server_socket.accept()
    print(f"Połączono z {address}")

    # Odbieranie nazwy pliku
    file_name = client_socket.recv(11).decode()
    print(f"Odebrano nazwę pliku: {file_name}")
    
    # Tworzenie pliku CSV do zapisu
    with open(file_name, 'w', newline='') as file:
        #rec_bytes = b""
        while True:
            data_chunk = client_socket.recv(1024)
            if not data_chunk:
                print('connection empty')
                break
            file.write(data_chunk)





        '''
        csv_writer = csv.writer(file, delimiter=';')
        
        # Odbieranie 1 000 000 tablic complex od klienta
        for _ in range(1_000_000):
            # Odbieranie rozmiaru danych (8 bajtów)
            data_size = struct.unpack(">Q", client_socket.recv(8))[0]
            print(data_size)
            # Odbieranie rzeczywistych danych
            data_bytes = b""
            while len(data_bytes) < data_size:
                packet = client_socket.recv(1024)
                if not packet:
                    break
                data_bytes += packet
            
            # Odtworzenie numpy array complex128 z bajtów
            array = np.frombuffer(data_bytes, dtype=np.complex128)
            
            # Zapis do pliku CSV
            for number in array:
                csv_writer.writerow([f"{number.real}", f"{number.imag}"])'''

    print("Zakończono zapis danych.")
    client_socket.close()
    server_socket.close()

# Uruchamianie serwera
if __name__ == "__main__":
    start_server()
