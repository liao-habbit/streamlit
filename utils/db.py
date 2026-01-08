import sqlite3
from pathlib import Path
from datetime import datetime

# 資料庫位置
DB_PATH = Path("utils/database.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    """初始化資料庫"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 使用者表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password_hash TEXT,
        created_at DATETIME
    )
    """)

    # 上傳檔案表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        file_name TEXT,
        file_hash TEXT,
        upload_at DATETIME,
        UNIQUE(user_id, file_hash),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized!")

# 新增使用者
def add_user_safe(username, email, password_hash):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
    if cursor.fetchone():
        conn.close()
        return False, "帳號或電子郵件已存在"
    cursor.execute(
        "INSERT INTO users (username, email, password_hash, created_at) VALUES (?,?,?,?)",
        (username, email, password_hash, datetime.now())
    )
    conn.commit()
    conn.close()
    return True, "帳號建立成功"

# 根據帳號或 email 查詢使用者
def get_user_by_login(login_input):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (login_input, login_input))
    user = cursor.fetchone()  # 回傳 (id, username, email, password_hash, created_at) 或 None
    conn.close()
    return user

def change_password(username, new_password_hash):
    """更換密碼"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password_hash=? WHERE username=?",
        (new_password_hash, username)
    )
    conn.commit()
    conn.close()

def delete_account(username):
    """刪除帳號"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()

# 新增檔案紀錄
def add_file(user_id, file_name, file_hash):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO files (user_id, file_name, file_hash, upload_at) VALUES (?,?,?,?)",
        (user_id, file_name, file_hash, datetime.now())
    )
    conn.commit()
    conn.close()

def file_exists(user_id, file_hash):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM files WHERE user_id=? AND file_hash=?",
        (user_id, file_hash)
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# 取得使用者所有檔案
def get_user_files(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, upload_at FROM files WHERE user_id=?", (user_id,))
    files = cursor.fetchall()
    conn.close()
    return files

def delete_file(user_id, file_name):
    """刪除單一檔案紀錄"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM files WHERE user_id=? AND file_name=?",
        (user_id, file_name)
    )
    conn.commit()
    conn.close()


def delete_all_files(user_id):
    """刪除使用者所有檔案紀錄"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM files WHERE user_id=?",
        (user_id,)
    )
    conn.commit()
    conn.close()
if __name__ == "__main__":
    init_db()
