from database.database import get_connection


def init_projects_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            cover_image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_project(title, description, category):

    title = (title or "").strip()
    description = (description or "").strip()
    category = (category or "").strip()

    if not title:
        raise ValueError("Project title cannot be empty.")

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

    finally:
        conn.close()


def get_projects():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                title,
                description,
                category,
                created_at
            FROM projects
            ORDER BY created_at DESC
        """)

        return cursor.fetchall()

    finally:
        conn.close()


def delete_project(project_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "DELETE FROM projects WHERE id = ?",
            (project_id,)
        )

        conn.commit()

    finally:
        conn.close()


init_projects_table()