import threading
import time
import socket
from my_socket_module.socket_client import send

def test_send():
    def mock_server():
        host = '127.0.0.1'
        port = 50000
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(1)
            conn, _ = server_socket.accept()
            with conn:
                data = conn.recv(1024)
                message = data.decode('utf-8').upper()
                conn.sendall(message.encode('utf-8'))

    # Start the mock server in a separate thread
    server_thread = threading.Thread(target=mock_server)
    server_thread.daemon = True
    server_thread.start()

    # Give the server time to start
    time.sleep(1)

    # Test sending a message to the mock server
    send("hello world")
