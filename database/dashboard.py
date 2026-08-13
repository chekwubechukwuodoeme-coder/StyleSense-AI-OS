import sqlite3
from pathlib import Path


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "stylesense.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Connect to the main StyleSense database.
    """

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# INITIALIZE DASHBOARD DATABASE
# ============================================================

def init_dashboard_tables():
    """
    Create tables required by the dashboard.
    """

    conn = get_connection()

    try:

        # ----------------------------------------------------
        # PROJECTS
        # ----------------------------------------------------

        conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                status TEXT DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ----------------------------------------------------
        # MISSION LOGS
        # ----------------------------------------------------

        conn.execute("""
            CREATE TABLE IF NOT EXISTS mission_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mission TEXT DEFAULT '',
                description TEXT DEFAULT '',
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ----------------------------------------------------
        # FASHION PROFILES
        #
        # This is the table used for designers.
        # We don't create a separate "designers" table.
        # ----------------------------------------------------

        conn.execute("""
            CREATE TABLE IF NOT EXISTS fashion_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,
                profile_type TEXT NOT NULL,

                location TEXT DEFAULT '',
                description TEXT DEFAULT '',
                specialties TEXT DEFAULT '',

                phone TEXT DEFAULT '',
                whatsapp TEXT DEFAULT '',
                image_url TEXT DEFAULT '',

                verified INTEGER DEFAULT 0,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(name, profile_type, location)
            )
        """)

        conn.commit()

    finally:
        conn.close()


# ============================================================
# COUNT PROJECTS
# ============================================================

def count_projects():

    init_dashboard_tables()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            SELECT COUNT(*)
            FROM projects
        """)

        return cursor.fetchone()[0]

    finally:
        conn.close()


# ============================================================
# COUNT DESIGNERS
# ============================================================

def count_designers():

    init_dashboard_tables()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            SELECT COUNT(*)
            FROM fashion_profiles
            WHERE LOWER(profile_type) = 'fashion designer'
        """)

        return cursor.fetchone()[0]

    finally:
        conn.close()


# ============================================================
# COUNT AI MISSIONS
# ============================================================

def count_missions():

    init_dashboard_tables()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            SELECT COUNT(*)
            FROM mission_logs
        """)

        return cursor.fetchone()[0]

    finally:
        conn.close()


# ============================================================
# INITIALIZE
# ============================================================

init_dashboard_tables()