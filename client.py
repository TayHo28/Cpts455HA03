# client.py
import socket

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get local machine name
    host = socket.gethostname()
    # Reserve a port for your service
    port = 12344
    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")
    # loop to keep receiving messages from the server
    try:
        while True:
            # Ask to send message or file, then send
            action = input("Do you want to send a (m)essage or (f)ile? ").lower()
            if action == 'm':
                client_message = input("Client: ")
                client_socket.sendall((client_message + "\n").encode('utf-8'))
                if client_message.lower() == 'bye':
                    print("Client ended the chat. Exiting...")
                    break
            elif action == 'f':
                file_path = input("Enter the path to the file: ")
                send_file(client_socket, file_path)
                # Wait for acknowledgment from the server
                print(f"Server: {client_socket.recv(1024).decode('utf-8')}")

            # Receive message or file from server
            header = client_socket.recv(1024).decode('utf-8')
            if header.startswith("FILE|"):
                receive_file(client_socket, buffer_size=1024, header=header)
            else:
                print(f"Server: {header.strip()}")
                if header.strip().lower() == 'bye':
                    print("Server ended the chat. Exiting...")
                    break

    # Close the connection with the server
    except KeyboardInterrupt:
        print("\nClient manually closed. Exiting...")
    finally:
        client_socket.close()
# The client can send a file to the server by using the following function:
def send_file(socket, file_path):
    with open(file_path, 'rb') as file: # rb = read binary
        file_data = file.read()
        header = f"FILE|{file_path.split('/')[-1]}|{len(file_data)}|" 
        socket.sendall(header.encode('utf-8') + file_data) # utf-8 is a character encoding scheme that uses 8-bit code units

# The server can receive a file from the client by using the following function:
def receive_file(socket, header, buffer_size=1024):
    file_name, file_size = header.split('|')[1:3]
    print(f"Receiving file: {file_name} of size: {file_size}")
    file_size = int(file_size)
    file_data = b""
    while len(file_data) < file_size:
        chunk = socket.recv(buffer_size)
        if not chunk:
            raise ConnectionError("Connection lost!")
        file_data += chunk
    
    with open("received_" + file_name, 'wb') as file:
        file.write(file_data)

    # Print the contents of the received file
    print(f"Received file: {file_name}")
    with open("received_" + file_name, 'r', encoding='utf-8', errors='ignore') as file:
        print("Contents of the file:")
        print(file.read())


if __name__ == "__main__":
    start_client()
