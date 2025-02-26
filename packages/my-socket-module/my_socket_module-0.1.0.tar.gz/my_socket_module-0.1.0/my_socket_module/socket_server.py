import socket

def receive():
    """
    Starts a socket server that listens on port 50000.
    Receives a message from a client, converts it to uppercase,
    and sends it back to the client.
    """
    host = '127.0.0.1'  # Localhost
    port = 50000        # Port to listen on

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)  # Receive up to 1024 bytes
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received: {message}")
                response = message.upper()
                conn.sendall(response.encode('utf-8'))
