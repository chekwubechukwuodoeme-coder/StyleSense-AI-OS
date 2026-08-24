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
# INITIALIZE DATABASE
# ============================================================

def init_profiles_table() -> None:

    conn = get_connection()

    try:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS fashion_profiles (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                name TEXT NOT NULL,

                profile_type TEXT NOT NULL,

                location TEXT DEFAULT '',

                description TEXT DEFAULT '',

                specialties TEXT DEFAULT '',

                phone TEXT DEFAULT '',

                whatsapp TEXT DEFAULT '',

                image_url TEXT DEFAULT '',

                image_data BLOB,

                image_mime_type TEXT DEFAULT '',

                verified INTEGER DEFAULT 0,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(
                    name,
                    profile_type,
                    location
                )
            )
        """)

        # ====================================================
        # DATABASE MIGRATION
        # ====================================================

        cursor = conn.execute(
            "PRAGMA table_info(fashion_profiles)"
        )

        columns = {
            row["name"]
            for row in cursor.fetchall()
        }

        # ----------------------------------------------------
        # USER ID
        # ----------------------------------------------------

        if "user_id" not in columns:

            conn.execute("""
                ALTER TABLE fashion_profiles
                ADD COLUMN user_id INTEGER
            """)

        # ----------------------------------------------------
        # IMAGE DATA
        # ----------------------------------------------------

        if "image_data" not in columns:

            conn.execute("""
                ALTER TABLE fashion_profiles
                ADD COLUMN image_data BLOB
            """)

        # ----------------------------------------------------
        # IMAGE MIME TYPE
        # ----------------------------------------------------

        if "image_mime_type" not in columns:

            conn.execute("""
                ALTER TABLE fashion_profiles
                ADD COLUMN image_mime_type TEXT DEFAULT ''
            """)

        conn.commit()

    finally:

        conn.close()


# ============================================================
# CREATE PROFILE
# ============================================================

def create_profile(
    user_id: Optional[int],
    name: str,
    profile_type: str,
    location: str = "",
    description: str = "",
    specialties: str = "",
    phone: str = "",
    whatsapp: str = "",
    image_data: Optional[bytes] = None,
    image_mime_type: str = ""
) -> Optional[int]:

    init_profiles_table()

    name = str(name).strip()

    profile_type = str(
        profile_type
    ).strip()

    if not name:

        raise ValueError(
            "Profile name is required."
        )

    if not profile_type:

        raise ValueError(
            "Profile type is required."
        )

    conn = get_connection()

    try:

        cursor = conn.execute("""
            INSERT INTO fashion_profiles (

                user_id,

                name,

                profile_type,

                location,

                description,

                specialties,

                phone,

                whatsapp,

                image_url,

                image_data,

                image_mime_type

            )

            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (

            user_id,

            name,

            profile_type,

            str(location).strip(),

            str(description).strip(),

            str(specialties).strip(),

            str(phone).strip(),

            str(whatsapp).strip(),

            "",

            image_data,

            str(image_mime_type or "").strip()

        ))

        conn.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:

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

    init_profiles_table()

    conn = get_connection()

    try:

        query = """
            SELECT

                id,

                user_id,

                name,

                profile_type,

                location,

                description,

                specialties,

                phone,

                whatsapp,

                image_url,

                image_data,

                image_mime_type,

                verified,

                created_at

            FROM fashion_profiles

            WHERE 1 = 1
        """

        values = []

        # ----------------------------------------------------
        # PROFILE TYPE
        # ----------------------------------------------------

        if (
            profile_type
            and profile_type.strip() != "All"
        ):

            query += """
                AND profile_type = ?
            """

            values.append(
                profile_type.strip()
            )

        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------

        if location and location.strip():

            query += """
                AND location LIKE ?
            """

            values.append(
                f"%{location.strip()}%"
            )

        # ----------------------------------------------------
        # SORT
        # ----------------------------------------------------

        query += """
            ORDER BY created_at DESC
        """

        cursor = conn.execute(
            query,
            values
        )

        return cursor.fetchall()

    finally:

        conn.close()


# ============================================================
# GET SINGLE PROFILE
# ============================================================

def get_profile(profile_id: int):

    init_profiles_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            SELECT

                id,

                user_id,

                name,

                profile_type,

                location,

                description,

                specialties,

                phone,

                whatsapp,

                image_url,

                image_data,

                image_mime_type,

                verified,

                created_at

            FROM fashion_profiles

            WHERE id = ?

        """, (
            profile_id,
        ))

        return cursor.fetchone()

    finally:

        conn.close()


# ============================================================
# GET USER PROFILES
# ============================================================

def get_user_profiles(
    user_id: int
):

    init_profiles_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            SELECT

                id,

                user_id,

                name,

                profile_type,

                location,

                description,

                specialties,

                phone,

                whatsapp,

                image_url,

                image_data,

                image_mime_type,

                verified,

                created_at

            FROM fashion_profiles

            WHERE user_id = ?

            ORDER BY created_at DESC

        """, (
            user_id,
        ))

        return cursor.fetchall()

    finally:

        conn.close()


# ============================================================
# UPDATE PROFILE
# ============================================================

def update_profile(
    profile_id: int,
    user_id: int,
    name: str,
    profile_type: str,
    location: str = "",
    description: str = "",
    specialties: str = "",
    phone: str = "",
    whatsapp: str = "",
    image_data: Optional[bytes] = None,
    image_mime_type: str = "",
    remove_image: bool = False
) -> bool:

    init_profiles_table()

    name = str(name).strip()

    profile_type = str(
        profile_type
    ).strip()

    if not name:

        raise ValueError(
            "Profile name is required."
        )

    if not profile_type:

        raise ValueError(
            "Profile type is required."
        )

    conn = get_connection()

    try:

        # ====================================================
        # IMAGE HANDLING
        # ====================================================

        if remove_image:

            image_query = """
                image_data = NULL,
                image_mime_type = '',
                image_url = ''
            """

            image_values = []

        elif image_data is not None:

            image_query = """
                image_data = ?,
                image_mime_type = ?,
                image_url = ''
            """

            image_values = [
                image_data,
                str(
                    image_mime_type or ""
                ).strip()
            ]

        else:

            image_query = """
                image_data = image_data,
                image_mime_type = image_mime_type
            """

            image_values = []

        # ====================================================
        # UPDATE
        # ====================================================

        query = f"""
            UPDATE fashion_profiles

            SET

                name = ?,

                profile_type = ?,

                location = ?,

                description = ?,

                specialties = ?,

                phone = ?,

                whatsapp = ?,

                {image_query}

            WHERE

                id = ?

                AND user_id = ?
        """

        values = [

            name,

            profile_type,

            str(location).strip(),

            str(description).strip(),

            str(specialties).strip(),

            str(phone).strip(),

            str(whatsapp).strip(),

        ]

        values.extend(
            image_values
        )

        values.extend([
            profile_id,
            user_id
        ])

        cursor = conn.execute(
            query,
            values
        )

        conn.commit()

        return cursor.rowcount > 0

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ============================================================
# DELETE PROFILE
# ============================================================

def delete_profile(
    profile_id: int,
    user_id: int
) -> bool:

    init_profiles_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            DELETE FROM fashion_profiles

            WHERE

                id = ?

                AND user_id = ?

        """, (
            profile_id,
            user_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    finally:

        conn.close()


# ============================================================
# VERIFY / UNVERIFY PROFILE
# ============================================================

def set_profile_verified(
    profile_id: int,
    verified: bool = True
) -> bool:

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
# DATABASE INITIALIZATION
# ============================================================

init_profiles_table()