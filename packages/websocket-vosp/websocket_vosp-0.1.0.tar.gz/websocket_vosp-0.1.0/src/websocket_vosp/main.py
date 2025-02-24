import socket
import json
import time

class SocketClient:
    def __init__(self, host, port, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
    
    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
        except socket.timeout:
            print(f"Connection to {self.host}:{self.port} timed out!")
            raise
        except socket.error as e:
            print(f"Socket error occurred: {e}")
            raise
    
    def send_request(self, request):
        try:
            self.sock.sendall(request.encode('utf-8'))
            print("Request sent.")
        except socket.error as e:
            print(f"Failed to send request: {e}")
            raise
    
    def receive_response(self):
        try:
            response = self.sock.recv(4096)  # Buffer size
            return response.decode('utf-8')
        except socket.error as e:
            print(f"Failed to receive response: {e}")
            raise
    
    def close(self):
        try:
            self.sock.close()
            print("Connection closed.")
        except socket.error as e:
            print(f"Failed to close socket: {e}")
            raise