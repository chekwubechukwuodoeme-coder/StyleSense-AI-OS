import sqlite3
import hashlib
from pathlib import Path


# ============================================================
# DATABASE
# ============================================================

DB_PATH = Path(__file__).resolve().parent.parent / "stylesense.db"


def get_connection():
    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


# ============================================================
# INITIALIZE / MIGRATE USERS TABLE
# ============================================================

def init_users_table():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Check whether users table exists
    # --------------------------------------------------------

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'users'
    """)

    exists = cursor.fetchone()

    # --------------------------------------------------------
    # Create table if it doesn't exist
    # --------------------------------------------------------

    if not exists:

        cursor.execute("""
            CREATE TABLE users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                full_name TEXT NOT NULL,

                email TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

    else:

        # ----------------------------------------------------
        # Get existing columns
        # ----------------------------------------------------

        cursor.execute(
            "PRAGMA table_info(users)"
        )

        columns = {
            row[1]
            for row in cursor.fetchall()
        }

        # ----------------------------------------------------
        # Add missing columns
        # ----------------------------------------------------

        if "full_name" not in columns:

            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN full_name TEXT
            """)

        if "email" not in columns:

            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN email TEXT
            """)

        if "password_hash" not in columns:

            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN password_hash TEXT
            """)

        if "created_at" not in columns:

            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN created_at TIMESTAMP
            """)

        # ----------------------------------------------------
        # Migrate possible old name column
        # ----------------------------------------------------

        if "name" in columns:

            cursor.execute("""
                UPDATE users
                SET full_name = name
                WHERE
                    (full_name IS NULL OR full_name = '')
                    AND name IS NOT NULL
            """)

    conn.commit()
    conn.close()


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# REGISTER USER
# ============================================================

def create_user(
    full_name,
    email,
    password
):

    init_users_table()

    full_name = full_name.strip()
    email = email.strip().lower()

    if not full_name:

        return False, "Please enter your full name."

    if not email:

        return False, "Please enter your email."

    if not password:

        return False, "Please enter a password."

    if len(password) < 6:

        return False, (
            "Password must be at least 6 characters."
        )

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Check existing email
    # --------------------------------------------------------

    cursor.execute("""
        SELECT id
        FROM users
        WHERE email = ?
    """, (email,))

    existing_user = cursor.fetchone()

    if existing_user:

        conn.close()

        return False, (
            "An account with this email already exists."
        )

    password_hash = hash_password(password)

    cursor.execute("""
        INSERT INTO users (
            full_name,
            email,
            password_hash
        )
        VALUES (?, ?, ?)
    """, (
        full_name,
        email,
        password_hash
    ))

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return True, user_id


# ============================================================
# LOGIN
# ============================================================

def authenticate_user(
    email,
    password
):

    init_users_table()

    email = email.strip().lower()

    password_hash = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            full_name,
            email
        FROM users
        WHERE
            email = ?
            AND password_hash = ?
    """, (
        email,
        password_hash
    ))

    user = cursor.fetchone()

    conn.close()

    return user


# ============================================================
# GET USER
# ============================================================

def get_user(user_id):

    init_users_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            full_name,
            email
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return user