import socket

def send(sentence):
    """
    Sends a sentence to the server listening on port 50000.
    Displays the response received from the server.
    
    Args:
        sentence (str): The sentence to send to the server.
    """
    host = '127.0.0.1'  # Server's IP address
    port = 50000        # Server's port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(sentence.encode('utf-8'))

        data = client_socket.recv(1024)  # Receive up to 1024 bytes
        response = data.decode('utf-8')
        print(f"Received from server: {response}")
