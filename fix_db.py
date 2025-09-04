import sqlite3

DB_NAME = "user.db"

def add_uploaded_file_column():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("ALTER TABLE users ADD COLUMN uploaded_file BLOB")
            print("Column 'uploaded_file' added successfully!")
    except sqlite3.OperationalError:
        print("Column already exists, no changes made.")

if __name__ == "__main__":
    add_uploaded_file_column()
