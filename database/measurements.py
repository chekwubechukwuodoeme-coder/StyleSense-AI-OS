import sqlite3

from database.database import DB_PATH


# ============================================================
# CREATE MEASUREMENT PROFILE
# ============================================================

def create_measurement_profile(
    user_id,
    client_name,
    category,
    height,
    bust,
    waist,
    hip,
    shoulder,
    sleeve,
    neck,
    armhole,
    garment_length,
    trouser_length,
    inseam,
    thigh,
    ankle,
    notes,
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO measurement_profiles (
            user_id,
            client_name,
            category,
            height,
            bust,
            waist,
            hip,
            shoulder,
            sleeve,
            neck,
            armhole,
            garment_length,
            trouser_length,
            inseam,
            thigh,
            ankle,
            notes
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            client_name,
            category,
            height,
            bust,
            waist,
            hip,
            shoulder,
            sleeve,
            neck,
            armhole,
            garment_length,
            trouser_length,
            inseam,
            thigh,
            ankle,
            notes,
        ),
    )

    conn.commit()

    profile_id = cursor.lastrowid

    conn.close()

    return profile_id


# ============================================================
# GET MEASUREMENT PROFILES
# ============================================================

def get_measurement_profiles(user_id):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM measurement_profiles
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    profiles = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return profiles


# ============================================================
# DELETE MEASUREMENT PROFILE
# ============================================================

def delete_measurement_profile(
    profile_id,
    user_id,
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM measurement_profiles
        WHERE id = ?
        AND user_id = ?
        """,
        (
            profile_id,
            user_id,
        ),
    )

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted