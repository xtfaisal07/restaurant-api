import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "restaurant.db"

SCHEMA = BASE_DIR / "schema.sql"
SEED = BASE_DIR / "seed.sql"


def reset_database():
    if DB_FILE.exists():
        DB_FILE.unlink()

    conn = sqlite3.connect(DB_FILE)

    with open(SCHEMA, "r") as f:
        conn.executescript(f.read())

    with open(SEED, "r") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

    print("PASS: Fresh SQLite database created")


if __name__ == "__main__":
    reset_database()