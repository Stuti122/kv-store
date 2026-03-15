import os
import sys

DB_FILE = "data.db"
store = {}

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            for line in f:
                parts = line.strip().split(" ", 2)
                if parts[0] == "SET":
                    store[parts[1]] = parts[2]

def set_value(key, value):
    store[key] = value
    with open(DB_FILE, "a") as f:
        f.write(f"SET {key} {value}\n")

def get_value(key):
    if key in store:
        print(store[key], flush=True)
def main():
    load_db()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split(" ", 2)
        cmd = parts[0]

        if cmd == "SET":
            set_value(parts[1], parts[2])

        elif cmd == "GET":
            get_value(parts[1])

        elif cmd == "EXIT":
            break

if __name__ == "__main__":
    main()