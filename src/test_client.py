"""Test client for chat server"""

import socket
import threading

HOST = '127.0.0.1'
PORT = 4000


def receiver(sock, stop_event):
    """Background thread to receive messages from server"""
    try:
        buffer = ""
        while not stop_event.is_set():
            sock.settimeout(0.5)
            try:
                data = sock.recv(4096)
                if not data:
                    break
                
                buffer += data.decode('utf-8', errors='ignore')
                
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        print(line)
            except socket.timeout:
                continue
    except Exception:
        pass


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stop_event = threading.Event()
    
    try:
        sock.connect((HOST, PORT))
        
        recv_thread = threading.Thread(target=receiver, args=(sock, stop_event), daemon=True)
        recv_thread.start()
        
        while True:
            try:
                line = input()
                if not line.strip():
                    continue
                
                if line.strip().upper() in ['QUIT', 'EXIT']:
                    sock.sendall((line + '\n').encode('utf-8'))
                    stop_event.set()
                    recv_thread.join(timeout=1)
                    break
                
                sock.sendall((line + '\n').encode('utf-8'))
            except EOFError:
                break
            except KeyboardInterrupt:
                break
                
    except ConnectionRefusedError:
        print(f"Error: Could not connect to {HOST}:{PORT}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()


if __name__ == '__main__':
    main()
