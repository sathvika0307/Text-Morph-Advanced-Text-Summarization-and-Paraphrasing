import sqlite3
import bcrypt
import os
from datetime import datetime, timedelta, timezone

# ---------- DATABASE PATH ----------
DB_NAME = os.path.join(os.path.dirname(__file__), "user.db")

# ---------- TIMEZONE (IST) ----------
IST = timezone(timedelta(hours=5, minutes=30))  # UTC+5:30

def _now_iso():
    """Return ISO timestamp string in IST timezone"""
    return datetime.now(IST).isoformat()

# ---------- DB CONNECTION ----------
def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn

# ---------- INITIALIZE TABLES ----------
def init_db():
    conn = get_db()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            name TEXT,
            age INTEGER,
            gender TEXT,
            language TEXT,
            photo BLOB
        )
    """)

    # Uploaded files table
    c.execute("""
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            file_name TEXT,
            file_content TEXT,
            uploaded_at TEXT
        )
    """)

    # Processed text table
    c.execute("""
        CREATE TABLE IF NOT EXISTS processed_text (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            task_type TEXT,      -- "summary" or "paraphrase"
            original_text TEXT,
            processed_text TEXT,
            model TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

# ---------- USER FUNCTIONS ----------
def add_user(username, email, password, name=None, age=None, gender=None, language=None, photo=None):
    conn = get_db()
    c = conn.cursor()
    try:
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c.execute("""
            INSERT INTO users (username, email, password, name, age, gender, language, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, email, hashed_pw, name, age, gender, language, photo))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(identifier, password):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? OR username=?", (identifier, identifier))
    user = c.fetchone()
    conn.close()
    if user:
        stored_pw = user[3]  # password is in 4th column
        if bcrypt.checkpw(password.encode('utf-8'), stored_pw):
            return user
    return None

def reset_password(identifier, new_password):
    """Reset password for a user (by email or username)."""
    conn = get_db()
    c = conn.cursor()

    hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    c.execute("UPDATE users SET password=? WHERE email=? OR username=?", (hashed_pw, identifier, identifier))
    conn.commit()

    updated = c.rowcount > 0
    conn.close()
    return updated

def save_uploaded_file(username, file_bytes, file_name="uploaded_file.txt"):
    conn = get_db()
    c = conn.cursor()
    try:
        content = file_bytes.decode("utf-8", errors="ignore")
    except:
        content = ""
    c.execute("""
        INSERT INTO uploaded_files (username, file_name, file_content, uploaded_at)
        VALUES (?, ?, ?, ?)
    """, (username, file_name, content, _now_iso()))
    conn.commit()
    conn.close()
    return True

def save_processed_text(username, task_type, original_text, processed_text, model="pegasus"):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO processed_text (username, task_type, original_text, processed_text, model, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, task_type, original_text, processed_text, model, _now_iso()))
    conn.commit()
    conn.close()
    return True

# ---------- INIT DB ----------
init_db()
