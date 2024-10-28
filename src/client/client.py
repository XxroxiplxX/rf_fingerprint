import socket
import numpy as np
import struct

def start_client(host='192.168.0.34', port=12345):
    # Tworzenie socketu klienta
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # Wysyłanie nazwy pliku
    file_name = 'iq_data.bin'
    client_socket.sendall(file_name.encode())
    
    # Generowanie i wysyłanie 1 000 000 tablic complex128
    for _ in range(10):
        # Tworzenie numpy array z liczbami zespolonymi
        array = np.array([complex(np.random.random(), np.random.random()) for _ in range(1024)], dtype=np.complex128)
        for cn in array:
            client_socket.sendall(cn.tobytes())
        # Konwersja array do bajtów
        #data_bytes = array.tobytes()
        
        # Wysyłanie rozmiaru danych
        #client_socket.sendall(struct.pack(">Q", len(data_bytes)))
        
        # Wysyłanie rzeczywistych danych
        #client_socket.sendall(data_bytes)
    
    print("Zakończono wysyłanie danych.")
    client_socket.close()

# Uruchamianie klienta
if __name__ == "__main__":
    start_client()
