from database.database import get_connection


# ============================================================
# PROJECT TABLE INITIALIZATION / MIGRATION
# ============================================================

def init_projects_table():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'projects'
        """)

        table_exists = cursor.fetchone()

        # ----------------------------------------------------
        # CREATE TABLE
        # ----------------------------------------------------

        if not table_exists:

            cursor.execute("""
                CREATE TABLE projects (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    user_id INTEGER,

                    title TEXT NOT NULL,

                    description TEXT DEFAULT '',

                    category TEXT DEFAULT '',

                    cover_image TEXT DEFAULT '',

                    created_at
                        TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            return

        # ----------------------------------------------------
        # CHECK EXISTING COLUMNS
        # ----------------------------------------------------

        cursor.execute(
            "PRAGMA table_info(projects)"
        )

        columns = cursor.fetchall()

        existing_columns = {
            column[1]
            for column in columns
        }

        # ----------------------------------------------------
        # ADD USER ID IF MISSING
        # ----------------------------------------------------

        if "user_id" not in existing_columns:

            cursor.execute("""
                ALTER TABLE projects
                ADD COLUMN user_id INTEGER
            """)

        # ----------------------------------------------------
        # ADD COVER IMAGE IF MISSING
        # ----------------------------------------------------

        if "cover_image" not in existing_columns:

            cursor.execute("""
                ALTER TABLE projects
                ADD COLUMN cover_image TEXT DEFAULT ''
            """)

        conn.commit()

    except Exception as e:

        conn.rollback()

        print(
            "PROJECT TABLE ERROR:",
            repr(e)
        )

        raise

    finally:

        conn.close()


# ============================================================
# CREATE PROJECT
# ============================================================

def create_project(
    title,
    description,
    category,
    user_id=None,
    cover_image=""
):

    title = (title or "").strip()
    description = (description or "").strip()
    category = (category or "").strip()
    cover_image = (cover_image or "").strip()

    if not title:

        raise ValueError(
            "Project title cannot be empty."
        )

    init_projects_table()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO projects (
                user_id,
                title,
                description,
                category,
                cover_image
            )

            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            title,
            description,
            category,
            cover_image
        ))

        conn.commit()

        return cursor.lastrowid

    except Exception as e:

        conn.rollback()

        print(
            "CREATE PROJECT ERROR:",
            repr(e)
        )

        raise

    finally:

        conn.close()


# ============================================================
# GET PROJECTS
# ============================================================

def get_projects(user_id=None):

    init_projects_table()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        if user_id is None:

            cursor.execute("""
                SELECT
                    id,
                    user_id,
                    title,
                    description,
                    category,
                    cover_image,
                    created_at

                FROM projects

                ORDER BY created_at DESC
            """)

        else:

            cursor.execute("""
                SELECT
                    id,
                    user_id,
                    title,
                    description,
                    category,
                    cover_image,
                    created_at

                FROM projects

                WHERE user_id = ?

                ORDER BY created_at DESC
            """, (
                user_id,
            ))

        return cursor.fetchall()

    finally:

        conn.close()


# ============================================================
# GET SINGLE PROJECT
# ============================================================

def get_project(
    project_id,
    user_id=None
):

    init_projects_table()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        if user_id is None:

            cursor.execute("""
                SELECT
                    id,
                    user_id,
                    title,
                    description,
                    category,
                    cover_image,
                    created_at

                FROM projects

                WHERE id = ?
            """, (
                project_id,
            ))

        else:

            cursor.execute("""
                SELECT
                    id,
                    user_id,
                    title,
                    description,
                    category,
                    cover_image,
                    created_at

                FROM projects

                WHERE id = ?
                AND user_id = ?
            """, (
                project_id,
                user_id
            ))

        return cursor.fetchone()

    finally:

        conn.close()


# ============================================================
# DELETE PROJECT
# ============================================================

def delete_project(
    project_id,
    user_id=None
):

    init_projects_table()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        if user_id is None:

            cursor.execute("""
                DELETE FROM projects
                WHERE id = ?
            """, (
                project_id,
            ))

        else:

            cursor.execute("""
                DELETE FROM projects
                WHERE id = ?
                AND user_id = ?
            """, (
                project_id,
                user_id
            ))

        conn.commit()

        return cursor.rowcount > 0

    finally:

        conn.close()


# ============================================================
# INITIALIZE
# ============================================================

init_projects_table()