import socket
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

def upload_file(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    
    command = f"UPLOAD {filename}"
    client.sendall(command.encode())
    
    with open(filename, 'rb') as f:
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            client.sendall(bytes_read)
    
    client.close()
    print(f"File {filename} uploaded successfully.")

def download_file(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    
    command = f"DOWNLOAD {filename}"
    client.sendall(command.encode())
    
    filepath = os.path.join('downloaded_files', filename)
    if not os.path.exists('downloaded_files'):
        os.makedirs('downloaded_files')
    
    with open(filepath, 'wb') as f:
        while True:
            bytes_read = client.recv(4096)
            if not bytes_read:
                break
            f.write(bytes_read)
    
    client.close()
    print(f"File {filename} downloaded successfully.")

if __name__ == "__main__":
    while True:
        action = input("Enter 'upload' to upload a file or 'download' to download a file (or 'exit' to quit): ").lower()
        if action == 'exit':
            break
        filename = input("Enter the filename: ")
        
        if action == 'upload':
            if os.path.exists(filename):
                upload_file(filename)
            else:
                print("File not found.")
        elif action == 'download':
            download_file(filename)
        else:
            print("Invalid action.")
