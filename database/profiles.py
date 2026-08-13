import sqlite3
from pathlib import Path
from typing import Optional


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "stylesense.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    # Allows rows to be accessed like dictionaries:
    # row["name"], row["location"], etc.
    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_profiles_table() -> None:
    """
    Create the fashion_profiles table if it does not exist.
    """

    conn = get_connection()

    try:
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
# CREATE PROFILE
# ============================================================

def create_profile(
    name: str,
    profile_type: str,
    location: str = "",
    description: str = "",
    specialties: str = "",
    phone: str = "",
    whatsapp: str = "",
    image_url: str = ""
) -> Optional[int]:
    """
    Create a new fashion profile.

    Returns:
        Profile ID if successful.
        None if the profile already exists.
    """

    init_profiles_table()

    # Basic validation
    name = name.strip()
    profile_type = profile_type.strip()

    if not name:
        raise ValueError("Profile name is required.")

    if not profile_type:
        raise ValueError("Profile type is required.")

    conn = get_connection()

    try:
        cursor = conn.execute("""
            INSERT INTO fashion_profiles (
                name,
                profile_type,
                location,
                description,
                specialties,
                phone,
                whatsapp,
                image_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            profile_type,
            location.strip(),
            description.strip(),
            specialties.strip(),
            phone.strip(),
            whatsapp.strip(),
            image_url.strip()
        ))

        conn.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:
        # Duplicate profile
        return None

    finally:
        conn.close()


# ============================================================
# GET ALL PROFILES
# ============================================================

def get_profiles(
    profile_type: str = "All",
    location: str = ""
):
    """
    Get fashion profiles.

    Optional filters:
        profile_type
        location

    Returns:
        List of sqlite3.Row objects.
    """

    init_profiles_table()

    conn = get_connection()

    try:
        query = """
            SELECT
                id,
                name,
                profile_type,
                location,
                description,
                specialties,
                phone,
                whatsapp,
                image_url,
                verified,
                created_at

            FROM fashion_profiles

            WHERE 1 = 1
        """

        values = []

        # --------------------------------------------
        # FILTER BY PROFILE TYPE
        # --------------------------------------------

        if profile_type and profile_type.strip() != "All":
            query += """
                AND profile_type = ?
            """

            values.append(profile_type.strip())

        # --------------------------------------------
        # FILTER BY LOCATION
        # --------------------------------------------

        if location and location.strip():
            query += """
                AND location LIKE ?
            """

            values.append(f"%{location.strip()}%")

        # --------------------------------------------
        # SORT
        # --------------------------------------------

        query += """
            ORDER BY created_at DESC
        """

        cursor = conn.execute(query, values)

        return cursor.fetchall()

    finally:
        conn.close()


# ============================================================
# GET SINGLE PROFILE
# ============================================================

def get_profile(profile_id: int):
    """
    Get one fashion profile by ID.

    Returns:
        sqlite3.Row if found.
        None if not found.
    """

    init_profiles_table()

    conn = get_connection()

    try:
        cursor = conn.execute("""
            SELECT
                id,
                name,
                profile_type,
                location,
                description,
                specialties,
                phone,
                whatsapp,
                image_url,
                verified,
                created_at

            FROM fashion_profiles

            WHERE id = ?
        """, (profile_id,))

        return cursor.fetchone()

    finally:
        conn.close()


# ============================================================
# UPDATE PROFILE
# ============================================================

def update_profile(
    profile_id: int,
    name: str,
    profile_type: str,
    location: str = "",
    description: str = "",
    specialties: str = "",
    phone: str = "",
    whatsapp: str = "",
    image_url: str = ""
) -> bool:
    """
    Update an existing fashion profile.

    Returns:
        True if updated.
        False if profile was not found.
    """

    init_profiles_table()

    name = name.strip()
    profile_type = profile_type.strip()

    if not name:
        raise ValueError("Profile name is required.")

    if not profile_type:
        raise ValueError("Profile type is required.")

    conn = get_connection()

    try:
        cursor = conn.execute("""
            UPDATE fashion_profiles

            SET
                name = ?,
                profile_type = ?,
                location = ?,
                description = ?,
                specialties = ?,
                phone = ?,
                whatsapp = ?,
                image_url = ?

            WHERE id = ?
        """, (
            name,
            profile_type,
            location.strip(),
            description.strip(),
            specialties.strip(),
            phone.strip(),
            whatsapp.strip(),
            image_url.strip(),
            profile_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# ============================================================
# VERIFY / UNVERIFY PROFILE
# ============================================================

def set_profile_verified(
    profile_id: int,
    verified: bool = True
) -> bool:
    """
    Mark a profile as verified or unverified.

    Returns:
        True if updated.
        False if profile was not found.
    """

    init_profiles_table()

    conn = get_connection()

    try:
        cursor = conn.execute("""
            UPDATE fashion_profiles

            SET verified = ?

            WHERE id = ?
        """, (
            1 if verified else 0,
            profile_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    finally:
        conn.close()


# ============================================================
# DELETE PROFILE
# ============================================================

def delete_profile(profile_id: int) -> bool:
    """
    Delete a fashion profile.

    Returns:
        True if deleted.
        False if profile did not exist.
    """

    init_profiles_table()

    conn = get_connection()

    try:
        cursor = conn.execute("""
            DELETE FROM fashion_profiles
            WHERE id = ?
        """, (profile_id,))

        conn.commit()

        return cursor.rowcount > 0

    finally:
        conn.close()


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

# Automatically create the table when this module is imported.
init_profiles_table()