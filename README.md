# Distributed File System — Client/Server Implementation
## Architecture Overview

```
CLIENT  ──────────────►  SERVER1  ──────────────►  SERVER2
  (file request)         (primary)                (replica)
        ◄──────────────           ◄──────────────
          (file/result)             (file response)
```

---

## Files

| File | Description |
|------|-------------|
| `server1.py` | Primary file server (port 6001) |
| `server2.py` | Replica file server (port 6002) |
| `client.py` | Client that sends file requests |
| `setup_test_files.py` | Creates sample test files |

---

## How to Run

### On a Single Machine (Local Testing)

**Step 1 — Setup test files:**
```bash
python3 setup_test_files.py
```

**Step 2 — Start SERVER2** (Terminal 1):
```bash
python3 server2.py
```

**Step 3 — Start SERVER1** (Terminal 2):
```bash
python3 server1.py
```

**Step 4 — Run CLIENT** (Terminal 3):
```bash
python3 client.py              # Interactive mode
python3 client.py hello.txt    # Single request mode
```

---

### On 3 Separate Cloud Nodes

**Node 1 (CLIENT):**
- Edit `client.py` → set `SERVER1_HOST = '<NODE2_IP>'`
- Run: `python3 client.py`

**Node 2 (SERVER1):**
- Edit `server1.py` → set `SERVER2_HOST = '<NODE3_IP>'`
- Run: `python3 server1.py`

**Node 3 (SERVER2):**
- Run: `python3 server2.py`

> Make sure firewall/security groups allow TCP on ports **6001** and **6002**.

---

## Logic Flow

```
CLIENT sends pathname  ──►  SERVER1
                              │
                    ┌─────────┴──────────┐
                    ▼                    ▼
             Check own files      Forward to SERVER2
                    │                    │
                    └─────────┬──────────┘
                              ▼
                  Both found?  ──► Compare contents
                  ├── Same     ──► Send one file to CLIENT
                  └── Different ─► Send BOTH files to CLIENT

                  Only S1 found ─► Send S1 file to CLIENT
                  Only S2 found ─► Send S2 file to CLIENT
                  Neither found ─► Send "not found" message
```

---

## Test Cases

| File Request | Expected Result |
|---|---|
| `hello.txt` | Files match → single file returned |
| `data.txt` | Files differ → both versions returned |
| `only_on_server1.txt` | Only on S1 → file returned from S1 |
| `only_on_server2.txt` | Only on S2 → file returned via S1 |
| `missing.txt` | Not found on either server |

---

## Configurable Parameters

In `server1.py`:
```python
SERVER2_HOST = '127.0.0.1'  # IP of SERVER2 node
SERVER2_PORT = 6002
```

In `client.py`:
```python
SERVER1_HOST = '127.0.0.1'  # IP of SERVER1 node
SERVER1_PORT = 6001
```
