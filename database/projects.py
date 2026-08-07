import sqlite3

conn = sqlite3.connect(
    "stylesense.db",
    check_same_thread=False
)

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


def create_project(title, description, category):

    cursor.execute(
        """
        INSERT INTO projects(
            title,
            description,
            category
        )
        VALUES(?,?,?)
        """,
        (
            title,
            description,
            category
        )
    )

    conn.commit()


def get_projects():

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


def delete_project(project_id):

    cursor.execute(
        "DELETE FROM projects WHERE id=?",
        (project_id,)
    )

    conn.commit()