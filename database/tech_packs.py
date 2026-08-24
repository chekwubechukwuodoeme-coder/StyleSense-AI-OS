import sqlite3

from database.database import DB_PATH


# ============================================================
# CREATE TECH PACK
# ============================================================

def create_tech_pack(
    user_id,
    design_name,
    category,
    description,
    fabric,
    colour,
    secondary_colour,
    trims,
    embroidery,
    construction,
    finishing,
    size_range,
    quantity,
    production_type,
    quality_control,
    notes,
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tech_packs (

            user_id,
            design_name,
            category,
            description,
            fabric,
            colour,
            secondary_colour,
            trims,
            embroidery,
            construction,
            finishing,
            size_range,
            quantity,
            production_type,
            quality_control,
            notes

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            design_name,
            category,
            description,
            fabric,
            colour,
            secondary_colour,
            trims,
            embroidery,
            construction,
            finishing,
            size_range,
            quantity,
            production_type,
            quality_control,
            notes,
        ),
    )

    conn.commit()

    pack_id = cursor.lastrowid

    conn.close()

    return pack_id


# ============================================================
# GET TECH PACKS
# ============================================================

def get_tech_packs(user_id):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tech_packs
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    packs = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return packs


# ============================================================
# DELETE TECH PACK
# ============================================================

def delete_tech_pack(
    pack_id,
    user_id,
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tech_packs
        WHERE id = ?
        AND user_id = ?
        """,
        (
            pack_id,
            user_id,
        ),
    )

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted