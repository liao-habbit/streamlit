import sqlite3
from pathlib import Path
DB_PATH = Path("utils/database.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 檢查 users table
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()