import socket
import threading
import os
from rfsoc_ofdm.overlay import Overlay


def capture_and_save(ol, filename):

    with open(filename, 'w') as file:
        for point in ol.inspectors['receiver'].get_frame():
            file.write(f"{point.real};{point.imag}\n")

def receive_files(client_socket):
    while True:
        try:
            file_info = client_socket.recv(1024).decode()
            if not file_info:
                break
            
            file_name, file_size = file_info.split(':')
            file_size = int(file_size)
            
            print(f"Receiving file: {file_name} of size: {file_size} bytes")
            
            with open(f"received_{file_name}", 'wb') as file:
                received_size = 0
                while received_size < file_size:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    print(data)
                    received_size += len(data)
            
            print(f"Received file: {file_name}")
        except:
            break

def send_file(client_socket, file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    client_socket.send(f"{file_name}:{file_size}".encode())
    
    with open(file_path, 'rb') as file:
        while (data := file.read(1024)):
            client_socket.send(data)

def start_client(server_ip, server_port, ol):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    threading.Thread(target=receive_files, args=(client_socket,)).start()
    counter = 0
    MAX_COUNT = 5
    try:
        while counter < MAX_COUNT:
            file_path = 'iq_data_' + str(counter) + '.csv'
            capture_and_save(ol, file_path)
            send_file(client_socket, file_path)
            os.remove(file_path)
            counter += 1
    except KeyboardInterrupt:
        print("Disconnecting from server.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    ol = Overlay()
    print('overlay set')
        # Konfiguracja ADC (odbiór sygnałów na 2432 MHz)
    adc_sample_freq = 4844.00  # częstotliwość próbkowania w MHz
    centre_freq = -2412  # przesunięcie częstotliwości środkowej do 2432 MHz

    ol.configure_adcs(sample_freq=adc_sample_freq, centre_freq=centre_freq)

    # Inicjalizacja odbiornika OFDM na 2432 MHz
    ol.initialise_receiver(enable=1, modulation='QPSK')
    server_ip = '192.168.0.34'  # Replace with the actual server IP
    server_port = 12346
    start_client(server_ip, server_port, ol)