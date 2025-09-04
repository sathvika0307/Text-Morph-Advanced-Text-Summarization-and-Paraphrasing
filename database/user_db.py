import sqlite3
import bcrypt
import os

# ---------- DATABASE PATH ----------
DB_NAME = os.path.join(os.path.dirname(__file__), "user.db")

# ---------- DB CONNECTION ----------
def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn

# ---------- INITIALIZE USERS TABLE ----------
def init_db():
    conn = get_db()
    c = conn.cursor()
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
            photo BLOB,
            uploaded_file BLOB
        )
    """)
    conn.commit()
    conn.close()

# ---------- ADD NEW USER ----------
def add_user(username, email, password, name, age, gender, language, photo):
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

# ---------- CHECK USER ----------
def check_user(identifier, password):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? OR username=?", (identifier, identifier))
    user = c.fetchone()
    conn.close()
    if user:
        stored_pw = user[3]
        if bcrypt.checkpw(password.encode('utf-8'), stored_pw):
            return user
    return None

# ---------- RESET PASSWORD ----------
def reset_password(identifier, new_password):
    conn = get_db()
    c = conn.cursor()
    hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    c.execute("UPDATE users SET password=? WHERE email=? OR username=?", 
              (hashed_pw, identifier, identifier))
    conn.commit()
    conn.close()
    return True

# ---------- UPDATE PROFILE ----------
def update_profile(username, name=None, age=None, gender=None, language=None, photo=None):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        UPDATE users SET 
            name = COALESCE(?, name),
            age = COALESCE(?, age),
            gender = COALESCE(?, gender),
            language = COALESCE(?, language),
            photo = COALESCE(?, photo)
        WHERE username = ?
    """, (name, age, gender, language, photo, username))
    conn.commit()
    conn.close()
    return True

# ---------- SAVE UPLOADED FILE ----------
def save_uploaded_file(username, file_bytes):
    """
    Save an uploaded document (txt, pdf, docx) in the database for the user.
    """
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET uploaded_file=? WHERE username=?", (file_bytes, username))
    conn.commit()
    conn.close()
    return True
