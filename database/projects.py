from database.database import get_connection


# ============================================================
# PROJECT TABLE INITIALIZATION / MIGRATION
# ============================================================

def init_projects_table():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ----------------------------------------------------
        # Check whether projects table exists
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'projects'
            """
        )

        table_exists = cursor.fetchone()

        # ----------------------------------------------------
        # Create table if it does not exist
        # ----------------------------------------------------

        if not table_exists:

            cursor.execute(
                """
                CREATE TABLE projects (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    title TEXT NOT NULL,

                    description TEXT,

                    category TEXT,

                    cover_image TEXT,

                    created_at
                        TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.commit()

            return

        # ----------------------------------------------------
        # Inspect existing schema
        # ----------------------------------------------------

        cursor.execute(
            "PRAGMA table_info(projects)"
        )

        columns = cursor.fetchall()

        existing_columns = {
            column[1]
            for column in columns
        }

        required_columns = {
            "id",
            "title",
            "description",
            "category",
            "cover_image",
            "created_at",
        }

        # ----------------------------------------------------
        # If schema is already correct, do nothing
        # ----------------------------------------------------

        if existing_columns == required_columns:

            return

        # ----------------------------------------------------
        # MIGRATE OLD PROJECT TABLE
        #
        # This handles an older projects table on
        # Streamlit Cloud.
        # ----------------------------------------------------

        cursor.execute(
            """
            ALTER TABLE projects
            RENAME TO projects_old
            """
        )

        # ----------------------------------------------------
        # Create correct table
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE projects (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL,

                description TEXT,

                category TEXT,

                cover_image TEXT,

                created_at
                    TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # ----------------------------------------------------
        # Determine which old columns are available
        # ----------------------------------------------------

        old_columns = {
            column[1]
            for column in columns
        }

        columns_to_copy = []

        for column in [
            "id",
            "title",
            "description",
            "category",
            "cover_image",
            "created_at",
        ]:

            if column in old_columns:

                columns_to_copy.append(column)

        # ----------------------------------------------------
        # Copy existing data
        # ----------------------------------------------------

        if columns_to_copy:

            column_sql = ", ".join(
                columns_to_copy
            )

            cursor.execute(
                f"""
                INSERT INTO projects (
                    {column_sql}
                )
                SELECT
                    {column_sql}
                FROM projects_old
                """
            )

        # ----------------------------------------------------
        # Remove old table
        # ----------------------------------------------------

        cursor.execute(
            "DROP TABLE projects_old"
        )

        conn.commit()

        print(
            "PROJECTS TABLE MIGRATED SUCCESSFULLY"
        )

    except Exception as e:

        conn.rollback()

        print(
            "PROJECT TABLE MIGRATION ERROR:",
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
    category
):

    title = (title or "").strip()
    description = (description or "").strip()
    category = (category or "").strip()

    if not title:

        raise ValueError(
            "Project title cannot be empty."
        )

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO projects (
                title,
                description,
                category,
                cover_image
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                title,
                description,
                category,
                None
            )
        )

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

def get_projects():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                title,
                description,
                category,
                created_at
            FROM projects
            ORDER BY created_at DESC
            """
        )

        return cursor.fetchall()

    finally:

        conn.close()


# ============================================================
# DELETE PROJECT
# ============================================================

def delete_project(project_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM projects
            WHERE id = ?
            """,
            (project_id,)
        )

        conn.commit()

    finally:

        conn.close()


# ============================================================
# INITIALIZE
# ============================================================

init_projects_table()