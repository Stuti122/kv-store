import sys
import os

DB_FILE = "data.db"
store = {}


def load_db():
    """Load key-value pairs from the data.db file into memory."""
    if not os.path.exists(DB_FILE):
        return

    with open(DB_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(" ", 2)
            if len(parts) == 3 and parts[0] == "SET":
                key = parts[1]
                value = parts[2]
                store[key] = value


def set_value(key, value):
    """Store a key-value pair and persist it to the database file."""
    store[key] = value
    with open(DB_FILE, "a") as f:
        f.write(f"SET {key} {value}\n")


def get_value(key):
    """Retrieve and print the value associated with a key."""
    if key in store:
        print(store[key], flush=True)


def main():
    """Main command loop for the key-value store."""
    load_db()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split(" ", 2)
        cmd = parts[0]

        if cmd == "SET":
            if len(parts) == 3:
                set_value(parts[1], parts[2])

        elif cmd == "GET":
            if len(parts) >= 2:
                get_value(parts[1])

        elif cmd == "EXIT":
            break


if __name__ == "__main__":
    main()