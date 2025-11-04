import sqlite3
import os

def create_tables():
    if not os.path.exists("data"):
        os.mkdir("data")

    conn = sqlite3.connect("data/financeflow.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS investments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT,
        county TEXT,
        project_name TEXT,
        industry TEXT,
        funding REAL,
        jobs_created INTEGER,
        start_year INTEGER,
        end_year INTEGER
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        state TEXT,
        county TEXT,
        start_date TEXT,
        end_date TEXT,
        completed INTEGER DEFAULT 0
    )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database initialized.")

