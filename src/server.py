"""Simple Socket Chat Server - Main entry point"""

import socket
import threading
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from handlers.client_handler import handle_client
from utils.config import get_port


def start_server():
    """Initialize and start the TCP chat server"""
    port = get_port()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.settimeout(1.0)
    
    try:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(10)
        
        print(f"Chat server started on port {port}")
        print("Waiting for connections... (Press Ctrl+C to stop)")
        
        while True:
            try:
                client_socket, address = server_socket.accept()
                threading.Thread(
                    target=handle_client,
                    args=(client_socket, address),
                    daemon=True
                ).start()
            except socket.timeout:
                continue
    
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()
        print("Server stopped")


if __name__ == "__main__":
    start_server()
