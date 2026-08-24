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

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# INITIALIZE DASHBOARD TABLES
# ============================================================

def init_dashboard_tables():
    """
    Initialize only dashboard-specific tables.

    IMPORTANT:
    The main projects, fashion_profiles and designs tables
    are created and managed by database/database.py.

    This file only creates mission_logs because it is
    dashboard-specific.
    """

    conn = get_connection()

    try:

        # ----------------------------------------------------
        # MISSION LOGS
        # ----------------------------------------------------

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mission_logs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                mission TEXT DEFAULT '',

                description TEXT DEFAULT '',

                status TEXT DEFAULT 'Pending',

                created_at
                    TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()

    finally:

        conn.close()


# ============================================================
# COUNT PROJECTS
# ============================================================

def count_projects():
    """
    Return the total number of projects.

    Uses the existing projects table from database.py.
    """

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            SELECT COUNT(*)
            FROM projects
            """
        )

        return cursor.fetchone()[0]

    except sqlite3.OperationalError:

        return 0

    finally:

        conn.close()


# ============================================================
# COUNT DESIGNS
# ============================================================

def count_designs():
    """
    Return the total number of saved AI designs.

    Uses the existing designs table from database.py.
    """

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            SELECT COUNT(*)
            FROM designs
            """
        )

        return cursor.fetchone()[0]

    except sqlite3.OperationalError:

        return 0

    finally:

        conn.close()


# ============================================================
# COUNT DESIGNERS
# ============================================================

def count_designers():
    """
    Return the total number of fashion designers.

    Uses the existing fashion_profiles table from database.py.

    A profile is counted as a designer when profile_type
    contains 'designer'.
    """

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            SELECT COUNT(*)
            FROM fashion_profiles
            WHERE LOWER(profile_type) LIKE '%designer%'
            """
        )

        return cursor.fetchone()[0]

    except sqlite3.OperationalError:

        return 0

    finally:

        conn.close()


# ============================================================
# COUNT AI GENERATIONS
# ============================================================

def count_ai_generations():
    """
    Return the total number of AI design generation jobs.

    Completed jobs are counted from design_jobs.

    If design_jobs does not exist, fall back to the number
    of saved designs.
    """

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            SELECT COUNT(*)
            FROM design_jobs
            WHERE LOWER(status) = 'completed'
            """
        )

        return cursor.fetchone()[0]

    except sqlite3.OperationalError:

        try:

            cursor = conn.execute(
                """
                SELECT COUNT(*)
                FROM designs
                """
            )

            return cursor.fetchone()[0]

        except sqlite3.OperationalError:

            return 0

    finally:

        conn.close()


# ============================================================
# COUNT MISSIONS
# ============================================================

def count_missions():
    """
    Return the total number of mission logs.
    """

    init_dashboard_tables()

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            SELECT COUNT(*)
            FROM mission_logs
            """
        )

        return cursor.fetchone()[0]

    except sqlite3.OperationalError:

        return 0

    finally:

        conn.close()


# ============================================================
# GET RECENT PROJECTS
# ============================================================

def get_recent_projects(limit=5):
    """
    Return the most recently created projects.
    """

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            SELECT *
            FROM projects
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    except sqlite3.OperationalError:

        return []

    finally:

        conn.close()


# ============================================================
# GET RECENT DESIGNS
# ============================================================

def get_recent_designs(limit=5):
    """
    Return the most recently created designs.
    """

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            SELECT *
            FROM designs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    except sqlite3.OperationalError:

        return []

    finally:

        conn.close()


# ============================================================
# GET RECENT DESIGNERS
# ============================================================

def get_recent_designers(limit=5):
    """
    Return recently added fashion designers.
    """

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            SELECT *
            FROM fashion_profiles
            WHERE LOWER(profile_type) LIKE '%designer%'
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    except sqlite3.OperationalError:

        return []

    finally:

        conn.close()


# ============================================================
# GET RECENT MISSIONS
# ============================================================

def get_recent_missions(limit=5):
    """
    Return the most recent AI missions.
    """

    init_dashboard_tables()

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            SELECT *
            FROM mission_logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    except sqlite3.OperationalError:

        return []

    finally:

        conn.close()


# ============================================================
# CREATE MISSION
# ============================================================

def create_mission(
    mission,
    description="",
    status="Pending"
):
    """
    Create a new dashboard mission.
    """

    init_dashboard_tables()

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            INSERT INTO mission_logs (
                mission,
                description,
                status
            )

            VALUES (?, ?, ?)
            """,
            (
                mission,
                description,
                status
            )
        )

        conn.commit()

        return cursor.lastrowid

    finally:

        conn.close()


# ============================================================
# UPDATE MISSION
# ============================================================

def update_mission(
    mission_id,
    status
):
    """
    Update the status of a mission.
    """

    init_dashboard_tables()

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            UPDATE mission_logs

            SET status = ?

            WHERE id = ?
            """,
            (
                status,
                mission_id
            )
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:

        conn.close()


# ============================================================
# DELETE MISSION
# ============================================================

def delete_mission(mission_id):
    """
    Delete a single mission.
    """

    init_dashboard_tables()

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            DELETE FROM mission_logs
            WHERE id = ?
            """,
            (mission_id,)
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:

        conn.close()


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

def get_dashboard_stats():
    """
    Return all important dashboard statistics in one dictionary.
    """

    return {

        "projects": count_projects(),

        "designs": count_designs(),

        "ai_generations": count_ai_generations(),

        "designers": count_designers(),

        "missions": count_missions(),

    }


# ============================================================
# INITIALIZE DASHBOARD-SPECIFIC TABLES
# ============================================================

init_dashboard_tables()