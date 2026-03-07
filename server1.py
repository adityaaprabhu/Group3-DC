"""
SERVER 1 - Primary File Server
- Receives file requests from CLIENT
- Checks its own filesystem
- Forwards request to SERVER 2
- Compares files and sends result to CLIENT
"""

import socket
import os
import json

# SERVER 1 configuration
HOST = '0.0.0.0'
PORT = 6001
FILES_DIR = './server1_files'

# SERVER 2 configuration (update IP if on separate nodes)
SERVER2_HOST = '127.0.0.1'
SERVER2_PORT = 6002

def query_server2(pathname):
    """Send file request to SERVER2 and return its response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER2_HOST, SERVER2_PORT))
            request = json.dumps({'pathname': pathname})
            s.sendall(request.encode())
            response_data = b''
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            return json.loads(response_data.decode())
    except ConnectionRefusedError:
        print("[SERVER1] Could not connect to SERVER2.")
        return {'status': 'error', 'message': 'SERVER2 unavailable'}
    except Exception as e:
        print(f"[SERVER1] Error querying SERVER2: {e}")
        return {'status': 'error', 'message': str(e)}

def handle_client(conn):
    try:
        data = conn.recv(4096).decode()
        request = json.loads(data)
        pathname = request.get('pathname', '')
        print(f"\n[SERVER1] Received request for: '{pathname}'")

        # --- Check SERVER1's own filesystem ---
        filepath = os.path.join(FILES_DIR, pathname.lstrip('/'))
        s1_found = os.path.isfile(filepath)
        s1_content = None
        if s1_found:
            with open(filepath, 'r') as f:
                s1_content = f.read()
            print(f"[SERVER1] File found locally.")
        else:
            print(f"[SERVER1] File NOT found locally.")

        # --- Query SERVER2 ---
        print(f"[SERVER1] Querying SERVER2 for '{pathname}'...")
        s2_response = query_server2(pathname)
        s2_found = s2_response.get('status') == 'found'
        s2_content = s2_response.get('content') if s2_found else None

        # --- Decision Logic ---
        if s1_found and s2_found:
            if s1_content == s2_content:
                print("[SERVER1] Files MATCH. Sending single file to CLIENT.")
                response = {
                    'status': 'match',
                    'message': 'Files are identical on both servers.',
                    'file': {'server': 'SERVER1', 'content': s1_content}
                }
            else:
                print("[SERVER1] Files DIFFER. Sending both files to CLIENT.")
                response = {
                    'status': 'mismatch',
                    'message': 'Files differ between servers! Sending both.',
                    'file_server1': {'server': 'SERVER1', 'content': s1_content},
                    'file_server2': {'server': 'SERVER2', 'content': s2_content}
                }

        elif s1_found and not s2_found:
            print("[SERVER1] File only on SERVER1. Sending to CLIENT.")
            response = {
                'status': 'partial',
                'message': 'File found only on SERVER1.',
                'file': {'server': 'SERVER1', 'content': s1_content}
            }

        elif not s1_found and s2_found:
            print("[SERVER1] File only on SERVER2. Sending to CLIENT.")
            response = {
                'status': 'partial',
                'message': 'File found only on SERVER2.',
                'file': {'server': 'SERVER2', 'content': s2_content}
            }

        else:
            print("[SERVER1] File NOT found on either server.")
            response = {
                'status': 'not_found',
                'message': f"File '{pathname}' not found on any server."
            }

        conn.sendall(json.dumps(response).encode())

    except Exception as e:
        print(f"[SERVER1] Error handling client: {e}")
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
        print(f"[SERVER1] Listening on port {PORT}...")
        while True:
            conn, addr = s.accept()
            print(f"[SERVER1] Connection from {addr}")
            handle_client(conn)

if __name__ == '__main__':
    main()
