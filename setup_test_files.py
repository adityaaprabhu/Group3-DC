#!/usr/bin/env python3
"""
Setup script: Creates sample files for testing the distributed file system.
Run this once before starting the servers.
"""

import os

# Create directories
os.makedirs('server1_files', exist_ok=True)
os.makedirs('server2_files', exist_ok=True)

# --- Identical file on both servers ---
with open('server1_files/hello.txt', 'w') as f:
    f.write("Hello from the distributed file system!\nThis file is the same on both servers.\n")

with open('server2_files/hello.txt', 'w') as f:
    f.write("Hello from the distributed file system!\nThis file is the same on both servers.\n")

# --- Different versions (simulating replication delay) ---
with open('server1_files/data.txt', 'w') as f:
    f.write("Version 1 of data.txt\nLine A\nLine B\n")

with open('server2_files/data.txt', 'w') as f:
    f.write("Version 2 of data.txt (updated)\nLine A\nLine B\nLine C (new)\n")

# --- File only on SERVER1 ---
with open('server1_files/only_on_server1.txt', 'w') as f:
    f.write("This file exists only on SERVER1.\n")

# --- File only on SERVER2 ---
with open('server2_files/only_on_server2.txt', 'w') as f:
    f.write("This file exists only on SERVER2.\n")

print("Setup complete! Test files created:")
print("  server1_files/hello.txt          (same on both)")
print("  server2_files/hello.txt          (same on both)")
print("  server1_files/data.txt           (different versions)")
print("  server2_files/data.txt           (different versions)")
print("  server1_files/only_on_server1.txt")
print("  server2_files/only_on_server2.txt")
print("\nTest cases:")
print("  hello.txt         -> match (single file sent)")
print("  data.txt          -> mismatch (both files sent)")
print("  only_on_server1.txt -> partial (from server1)")
print("  only_on_server2.txt -> partial (from server2)")
print("  missing.txt       -> not found")
