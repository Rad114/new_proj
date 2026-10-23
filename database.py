import sqlite3
import hashlib


DATABASE_NAME = "users.db"


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# PASSWORD HASH
# ============================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# REGISTER USER
# ============================================================

def register_user(name, email, password):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    hashed_password = hash_password(password)

    try:

        cursor.execute("""
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
        """, (
            name,
            email,
            hashed_password
        ))

        connection.commit()

        connection.close()

        return True, "Registration successful."

    except sqlite3.IntegrityError:

        connection.close()

        return False, "Email already registered."

    except Exception as error:

        connection.close()

        return False, str(error)


# ============================================================
# CHECK USER
# ============================================================

def user_exists():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count > 0
# ============================================================
# LOGIN USER
# ============================================================

def login_user(email, password):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        SELECT id, name, email
        FROM users
        WHERE email = ? AND password = ?
    """, (
        email,
        hashed_password
    ))

    user = cursor.fetchone()

    connection.close()

    if user:
        return True, user

    return False, None


# ============================================================
# CREATE DATABASE WHEN FILE RUNS
# ============================================================

create_database()