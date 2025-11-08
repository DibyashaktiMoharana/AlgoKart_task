clients = {}


def send(sock, message):
    """Send message to client (adds newline if needed)"""
    if not message.endswith('\n'):
        message += '\n'
    try:
        sock.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Send error: {e}")


def broadcast(message):
    """Send message to all clients"""
    for sock in list(clients.values()):
        send(sock, message)


def broadcast_except(message, exclude_username):
    """Send message to all clients except one"""
    for username, sock in list(clients.items()):
        if username != exclude_username:
            send(sock, message)


def send_to_user(username, message):
    """Send message to specific user"""
    if sock := clients.get(username):
        send(sock, message)
        return True
    return False


def add_client(username, sock):
    """Register new client"""
    clients[username] = sock


def remove_client(username):
    """Remove client"""
    clients.pop(username, None)


def is_username_taken(username):
    """Check if username exists"""
    return username in clients


def get_usernames():
    """Get list of all active usernames"""
    return list(clients.keys())
