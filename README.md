# Socket-Based Client-Server Communication

This project implements a client-server communication channel using raw sockets in Python. The client can send OS commands to the server, which executes them and returns the result.

## Requirements

- Python 3.x
- socket
- json
- subprocess
- threading
- unittest

## Setup

1. Clone the repository.
2. Navigate to the project directory.
3. Install the required packages using `pip install -r requirements.txt`.

## Usage

### Running the Server

```bash
python3 server.py

### Running the client.py
```bash
python3 client.py