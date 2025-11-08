import socket
from . import broadcast

IDLE_TIMEOUT = 60  # seconds


def sanitize(text):
    """Clean user input"""
    return ' '.join(text.replace('\r\n', '\n').replace('\r', '\n').split())


def parse_command(line):
    """Parse command line into (command, args)"""
    parts = line.strip().split(maxsplit=1)
    if not parts:
        return "", ""
    return parts[0].upper(), parts[1] if len(parts) > 1 else ""


def handle_client(sock, address):
    """Handle single client connection lifecycle"""
    print(f"New connection from {address}")
    username = None
    buffer = ""
    cleanup_done = False
    sock.settimeout(IDLE_TIMEOUT)
    
    try:
        while True:
            try:
                data = sock.recv(1024)
            except socket.timeout:
                if username:
                    broadcast.remove_client(username)
                    broadcast.broadcast(f"INFO {username} disconnected")
                    cleanup_done = True
                sock.close()
                print(f"Connection closed (idle timeout): {address}")
                return
            
            if not data:
                break
            
            buffer += data.decode('utf-8', errors='ignore')
            
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                line = line.strip()
                if not line:
                    continue
                
                command, args = parse_command(line)
                
                # LOGIN command
                if command == "LOGIN":
                    if username:
                        broadcast.send(sock, "ERR already-logged-in")
                    elif not args:
                        broadcast.send(sock, "ERR missing-username")
                    else:
                        clean_username = sanitize(args)
                        if not clean_username:
                            broadcast.send(sock, "ERR invalid-username")
                        elif broadcast.is_username_taken(clean_username):
                            broadcast.send(sock, "ERR username-taken")
                        else:
                            broadcast.add_client(clean_username, sock)
                            broadcast.send(sock, "OK")
                            username = clean_username
                
                # All other commands require login
                elif not username:
                    broadcast.send(sock, "ERR not-logged-in")
                
                elif command == "MSG":
                    if args:
                        clean_text = sanitize(args)
                        if clean_text:
                            broadcast.broadcast_except(f"MSG {username} {clean_text}", username)
                
                elif command == "WHO":
                    for user in broadcast.get_usernames():
                        broadcast.send(sock, f"USER {user}")
                
                elif command == "DM":
                    if args:
                        parts = args.split(maxsplit=1)
                        if len(parts) == 2:
                            recipient = sanitize(parts[0])
                            text = sanitize(parts[1])
                            if recipient and text:
                                broadcast.send_to_user(recipient, f"DM {username} {text}")
                
                elif command == "PING":
                    broadcast.send(sock, "PONG")
                
                elif command in ("QUIT", "EXIT"):
                    broadcast.send(sock, "Goodbye!")
                    break
                
                else:
                    broadcast.send(sock, f"ERR unknown-command {command}")
    
    except Exception as e:
        print(f"Error handling {address}: {e}")
    
    finally:
        if username and not cleanup_done:
            broadcast.remove_client(username)
            broadcast.broadcast(f"INFO {username} disconnected")
        sock.close()
        print(f"Connection closed: {address}")
