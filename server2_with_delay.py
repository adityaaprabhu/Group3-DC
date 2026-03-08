"""
SERVER 2 - Replica File Server
Listens for file requests from SERVER 1, returns file contents if found.
Note: Simulates replication delay — SERVER2 may have outdated file versions.
"""

import socket
import os
import json
import time
import random

HOST = '0.0.0.0'
PORT = 6002
FILES_DIR = './server2_files'  # Directory where SERVER2 stores its files

# Replication delay simulation (in seconds)
# Represents the delay in updating the replica server
REPLICATION_DELAY = 5  # seconds

def handle_request(conn):
    try:
        data = conn.recv(4096).decode()
        request = json.loads(data)
        pathname = request.get('pathname', '')

        # Simulate replication delay — SERVER2 may lag behind SERVER1
        delay = random.uniform(0, REPLICATION_DELAY)
        print(f"[SERVER2] Simulating replication delay of {delay:.2f}s...")
        time.sleep(delay)

        filepath = os.path.join(FILES_DIR, pathname.lstrip('/'))

        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            response = {
                'status': 'found',
                'pathname': pathname,
                'content': content
            }
            print(f"[SERVER2] File '{pathname}' found. Sending to SERVER1.")
        else:
            response = {
                'status': 'not_found',
                'pathname': pathname,
                'content': None
            }
            print(f"[SERVER2] File '{pathname}' NOT found.")

        conn.sendall(json.dumps(response).encode())
    except Exception as e:
        print(f"[SERVER2] Error: {e}")
        error_resp = {'status': 'error', 'message': str(e)}
        conn.sendall(json.dumps(error_resp).encode())
    finally:
        conn.close()

def main():
    os.makedirs(FILES_DIR, exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[SERVER2] Listening on port {PORT}...")
        while True:
            conn, addr = s.accept()
            print(f"[SERVER2] Connection from {addr}")
            handle_request(conn)

if __name__ == '__main__':
    main()
