from pathlib import Path
import sqlite3

from harness.reset_db import reset_database

BASE_DIR = Path(__file__).resolve().parent.parent
DB = BASE_DIR / "restaurant.db"


def test_fresh_database_repeatability():
    # First reset
    reset_database()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    first = cur.fetchone()[0]
    conn.close()

    # Second reset
    reset_database()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    second = cur.fetchone()[0]
    conn.close()

    assert first == second == 1