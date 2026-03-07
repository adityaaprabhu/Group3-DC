"""
CLIENT - Distributed File System Client
Sends file requests to SERVER1 and displays results.
"""

import socket
import json
import sys

SERVER1_HOST = '127.0.0.1'  # Update to SERVER1's IP if on separate node
SERVER1_PORT = 6001

def request_file(pathname):
    print(f"\n[CLIENT] Requesting file: '{pathname}'")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER1_HOST, SERVER1_PORT))
            request = json.dumps({'pathname': pathname})
            s.sendall(request.encode())

            response_data = b''
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk

        response = json.loads(response_data.decode())
        status = response.get('status')
        message = response.get('message', '')

        print(f"[CLIENT] Status: {status.upper()}")
        print(f"[CLIENT] Message: {message}")

        if status == 'match':
            file_info = response.get('file', {})
            print(f"[CLIENT] === File from {file_info['server']} ===")
            print(file_info['content'])

        elif status == 'mismatch':
            f1 = response.get('file_server1', {})
            f2 = response.get('file_server2', {})
            print(f"[CLIENT] === File from {f1['server']} ===")
            print(f1['content'])
            print(f"[CLIENT] === File from {f2['server']} ===")
            print(f2['content'])

        elif status == 'partial':
            file_info = response.get('file', {})
            print(f"[CLIENT] === File from {file_info['server']} ===")
            print(file_info['content'])

        elif status == 'not_found':
            print(f"[CLIENT] File not available on any server.")

        elif status == 'error':
            print(f"[CLIENT] Server error: {message}")

    except ConnectionRefusedError:
        print(f"[CLIENT] Could not connect to SERVER1 at {SERVER1_HOST}:{SERVER1_PORT}")
    except Exception as e:
        print(f"[CLIENT] Error: {e}")

def main():
    if len(sys.argv) < 2:
        # Interactive mode
        print("=== Distributed File System Client ===")
        print(f"Connected to SERVER1 at {SERVER1_HOST}:{SERVER1_PORT}")
        while True:
            pathname = input("\nEnter file pathname (or 'quit' to exit): ").strip()
            if pathname.lower() == 'quit':
                print("[CLIENT] Exiting.")
                break
            if pathname:
                request_file(pathname)
    else:
        # Command-line argument mode
        request_file(sys.argv[1])

if __name__ == '__main__':
    main()
