import threading
import time
from my_socket_module.socket_server import receive
from my_socket_module.socket_client import send

def test_receive():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=receive)
    server_thread.daemon = True
    server_thread.start()

    # Give the server time to start
    time.sleep(1)

    # Test sending a message to the server
    send("hello world")
