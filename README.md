# Simple Socket Chat Server

A lightweight multi-user TCP chat server (no HTTP, no database) that supports real-time communication using sockets and only the language standard library.


## Project Structure

```
algokart/
├── src/
│   ├── server.py              # Main server entry point
│   ├── test_client.py         # Test client application
│   ├── handlers/
│   │   ├── client_handler.py  # Client connection logic
│   │   └── broadcast.py       # Message broadcasting
│   └── utils/
│       └── config.py          # Configuration management
├── README.md
└── .gitignore
```

## Setup

No external dependencies required. This project uses only the Python standard library.

### Requirements

- Python 3.10 or higher
- Windows, macOS, or Linux


### Available Commands

- `LOGIN <username>` - Log in with a unique username
- `MSG <text>` - Broadcast message to all other users
- `WHO` - List all active users
- `DM <username> <text>` - Send private message to specific user
- `PING` - Test connection (server responds with PONG)
- `QUIT` or `EXIT` - Disconnect from server



## How to Run

### Start the Server

Open a terminal and run:

```cmd
python src\server.py
```

The server starts on port 4000 by default.

To use a custom port:

```cmd
python src\server.py --port 5000
```

Or via environment variable:

```cmd
set PORT=5000
python src\server.py
```

### Connect Clients

Open additional terminals (one per client) and run:

```cmd
python src\test_client.py
```

Each client can connect to the server and interact using the protocol commands.


## Testing with Multiple Terminals

To test the chat server functionality:

1. **Terminal 1 (Server):**

   ```cmd
   python src\server.py
   ```

2. **Terminal 2 (Client 1):**

   ```cmd
   python src\test_client.py
   ```

   Type: `LOGIN alice`

3. **Terminal 3 (Client 2):**

   ```cmd
   python src\test_client.py
   ```

   Type: `LOGIN bob`

4. **Test Commands:**
   - In alice's terminal: `MSG Hello everyone!`
   - In bob's terminal: `MSG Hi alice!`
   - In either terminal: `WHO` to see active users
   - In alice's terminal: `DM bob Private message`
   - In either terminal: `PING` to test connection
   - Type `QUIT` or `EXIT` to disconnect cleanly




## Example Session

### Terminal 1 - Server

```cmd
D:\webDev\algokart> python src\server.py
Chat server started on port 4000
Waiting for connections... (Press Ctrl+C to stop)
New connection from ('127.0.0.1', 52341)
New connection from ('127.0.0.1', 52342)
Connection closed: ('127.0.0.1', 52342)
```

### Terminal 2 - Client 1 (Naman)

```
LOGIN Naman
OK
MSG hi everyone!
MSG how are you?
WHO
USER Naman
USER Yudi
QUIT
Goodbye!
```

### Terminal 3 - Client 2 (Yudi)

```
LOGIN Yudi
OK
MSG Naman hi everyone!
MSG Naman how are you?
MSG hello Naman!
INFO Naman disconnected
```


This implementation follows the wire protocol strictly, defaults to port 4000, and supports configuration via `PORT` environment variable or `--port` CLI flag.
