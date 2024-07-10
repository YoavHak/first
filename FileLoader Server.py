import socket
import os
import threading

UPLOAD_FOLDER = "uploaded_files"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

def handle_client(client_socket):
    try:
        command = client_socket.recv(1024).decode()
        
        if command.startswith('UPLOAD'):
            filename = command.split()[1]
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            with open(filepath, 'wb') as f:
                while True:
                    bytes_read = client_socket.recv(4096)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
            
            print(f"File {filename} uploaded successfully.")
        
        elif command.startswith('DOWNLOAD'):
            filename = command.split()[1]
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    while True:
                        bytes_read = f.read(4096)
                        if not bytes_read:
                            break
                        client_socket.sendall(bytes_read)
                
                print(f"File {filename} downloaded successfully.")
            else:
                client_socket.sendall(b"File not found.")
        
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
