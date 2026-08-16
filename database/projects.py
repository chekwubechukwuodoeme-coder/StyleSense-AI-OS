from database.database import get_connection


# ============================================================
# INITIALIZE PROJECTS TABLE
# ============================================================

def init_projects_table():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # CREATE TABLE IF IT DOES NOT EXIST
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (

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

    # --------------------------------------------------------
    # CHECK EXISTING COLUMNS
    # --------------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(projects)"
    )

    existing_columns = {
        row[1]
        for row in cursor.fetchall()
    }

    # --------------------------------------------------------
    # ADD MISSING COLUMNS
    # --------------------------------------------------------

    if "title" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE projects
            ADD COLUMN title TEXT
            """
        )

    if "description" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE projects
            ADD COLUMN description TEXT
            """
        )

    if "category" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE projects
            ADD COLUMN category TEXT
            """
        )

    if "cover_image" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE projects
            ADD COLUMN cover_image TEXT
            """
        )

    if "created_at" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE projects
            ADD COLUMN created_at
            TIMESTAMP
            """
        )

    conn.commit()
    conn.close()


# ============================================================
# CREATE PROJECT
# ============================================================

def create_project(
    title,
    description,
    category
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO projects (
            title,
            description,
            category
        )
        VALUES (?, ?, ?)
        """,
        (
            title,
            description,
            category
        )
    )

    conn.commit()

    project_id = cursor.lastrowid

    conn.close()

    return project_id


# ============================================================
# GET PROJECTS
# ============================================================

def get_projects():

    conn = get_connection()
    cursor = conn.cursor()

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

    projects = cursor.fetchall()

    conn.close()

    return projects


# ============================================================
# DELETE PROJECT
# ============================================================

def delete_project(project_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM projects
        WHERE id = ?
        """,
        (project_id,)
    )

    conn.commit()
    conn.close()


# ============================================================
# INITIALIZE
# ============================================================

init_projects_table()