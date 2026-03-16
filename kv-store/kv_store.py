import sys
import os

DB_FILE = "data.db"

# In-memory index implemented as a list of (key, value) tuples
store = []


def load_db():
    """Load the append-only log and rebuild the in-memory index."""
    if not os.path.exists(DB_FILE):
        return

    with open(DB_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(" ", 2)
            if len(parts) == 3 and parts[0] == "SET":
                key = parts[1]
                value = parts[2]
                set_in_memory(key, value)


def set_in_memory(key, value):
    """Update the in-memory list index (last write wins)."""
    for i in range(len(store)):
        if store[i][0] == key:
            store[i] = (key, value)
            return

    store.append((key, value))


def set_value(key, value):
    """Persist SET operation and update index."""
    set_in_memory(key, value)

    with open(DB_FILE, "a") as f:
        f.write(f"SET {key} {value}\n")


def get_value(key):
    """Retrieve a value by scanning the in-memory list."""
    for k, v in store:
        if k == key:
            print(v, flush=True)
            return


def main():
    """Main CLI loop reading commands from stdin."""
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