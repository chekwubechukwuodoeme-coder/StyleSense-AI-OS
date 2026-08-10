import sqlite3


DB_NAME = "stylesense.db"


def get_connection():
    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )


def init_projects_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects(
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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO projects(
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


def get_projects():

    conn = get_connection()
    cursor = conn.cursor()

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

    projects = cursor.fetchall()

    conn.close()

    return projects


def delete_project(project_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )

    conn.commit()
    conn.close()


init_projects_table()