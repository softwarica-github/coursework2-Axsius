import socket
import struct
import pickle
import threading
import tkinter as tk
import subprocess

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.76', 8080))
server_socket.listen(4)
clients_connected = {}
clients_data = {}
count = 1
def run_admin_program():
    try:
        subprocess.Popen(['python', r"C:\Users\anish\OneDrive\Documents\sem 3\Algo2\cw2\admints2.py"])
    except FileNotFoundError:
        print("Program not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def connection_requests():
    global count
    while True:
        print("Waiting for connection...")
        client_socket, address = server_socket.accept()
        print(f"Connections from {address} has been established")
        print(len(clients_connected))
        if len(clients_connected) == 4:
            client_socket.send('not_allowed'.encode('utf-16'))
            client_socket.close()
            continue
        else:
            client_socket.send('allowed'.encode('utf-16'))
        try:
            client_name = client_socket.recv(1024).decode('utf-16')
        except:
            print(f"{address} disconnected")
            client_socket.close()
            continue
        print(f"{address} identified itself as {client_name}")
        clients_connected[client_socket] = (client_name, count)
        image_size_bytes = client_socket.recv(1024)
        image_size_int = struct.unpack('i', image_size_bytes)[0]
        client_socket.send('received'.encode('utf-16'))
        image_extension = client_socket.recv(1024).decode('utf-16')

        b = b''
        while True:
            image_bytes = client_socket.recv(1024)
            b += image_bytes
            if len(b) == image_size_int:
                break
        clients_data[count] = (client_name, b, image_extension)
        clients_data_bytes = pickle.dumps(clients_data)
        clients_data_length = struct.pack('i', len(clients_data_bytes))
        client_socket.send(clients_data_length)
        client_socket.send(clients_data_bytes)
        if client_socket.recv(1024).decode('utf-16') == 'image_received':
            client_socket.send(struct.pack('i', count))

            for client in clients_connected:
                if client != client_socket:
                    client.send('notification'.encode('utf-16'))
                    data = pickle.dumps(
                        {'message': f"{clients_connected[client_socket][0]} joined the chat", 'extension': image_extension,
                         'image_bytes': b, 'name': clients_connected[client_socket][0], 'n_type': 'joined', 'id': count})
                    data_length_bytes = struct.pack('i', len(data))
                    client.send(data_length_bytes)
                    client.send(data)
        count += 1
        t = threading.Thread(target=receive_data, args=(client_socket,))
        t.start()

def receive_data(client_socket):
    while True:
        try:
            data_bytes = client_socket.recv(1024)
        except ConnectionResetError:
            print(f"{clients_connected[client_socket][0]} disconnected")
            for client in clients_connected:
                if client != client_socket:
                    client.send('notification'.encode('utf-16'))
                    data = pickle.dumps({'message': f"{clients_connected[client_socket][0]} left the chat",
                                         'id': clients_connected[client_socket][1], 'n_type': 'left'})
                    data_length_bytes = struct.pack('i', len(data))
                    client.send(data_length_bytes)
                    client.send(data)

            del clients_data[clients_connected[client_socket][1]]
            del clients_connected[client_socket]
            client_socket.close()
            break
        except ConnectionAbortedError:
            print(f"{clients_connected[client_socket][0]} disconnected unexpectedly.")

            for client in clients_connected:
                if client != client_socket:
                    client.send('notification'.encode('utf-16'))
                    data = pickle.dumps({'message': f"{clients_connected[client_socket][0]} left the chat",
                                         'id': clients_connected[client_socket][1], 'n_type': 'left'})
                    data_length_bytes = struct.pack('i', len(data))
                    client.send(data_length_bytes)
                    client.send(data)
            del clients_data[clients_connected[client_socket][1]]
            del clients_connected[client_socket]
            client_socket.close()
            break

        for client in clients_connected:
            if client != client_socket:
                client.send('message'.encode('utf-16'))
                client.send(data_bytes)
connection_requests()

