import sqlite3
import os

DB_NAME = "safe_sql_demo.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def setup_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    with get_connection() as conn:
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())
        with open("sample_data.sql", "r") as f:
            conn.executescript(f.read())
    print("Database initialized successfully.")

if __name__ == "__main__":
    setup_db()
