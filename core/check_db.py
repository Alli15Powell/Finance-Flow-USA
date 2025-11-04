import sqlite3
import pandas as pd

conn = sqlite3.connect("data/financeflow.db")

print("=== Tables ===")
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)

print("\n=== Investments Table ===")
try:
    df = pd.read_sql_query("SELECT * FROM investments", conn)
    print(df)
except Exception as e:
    print("Error reading investments:", e)

conn.close()
