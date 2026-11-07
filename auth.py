import sqlite3
import bcrypt

DB_PATH = "learniq.db"


def init_auth_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def register_user(name, email, password):
    conn = sqlite3.connect(DB_PATH)

    try:
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email.lower().strip(), password_hash)
        )
        conn.commit()
        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "This email is already registered."

    finally:
        conn.close()


def authenticate_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, email, password_hash FROM users WHERE email = ?",
        (email.lower().strip(),)
    )

    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode("utf-8"), user[2]):
        return user[0], user[1]

    return None