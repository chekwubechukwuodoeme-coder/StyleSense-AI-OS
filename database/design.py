import sqlite3

conn = sqlite3.connect(
    "stylesense.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS designs(

id INTEGER PRIMARY KEY AUTOINCREMENT,

project_id INTEGER,

title TEXT,

design TEXT,

image TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()


def save_design(
    project_id,
    title,
    design,
    image
):

    cursor.execute(

        """
        INSERT INTO designs(
        project_id,
        title,
        design,
        image
        )

        VALUES(?,?,?,?)
        """,

        (
            project_id,
            title,
            design,
            image
        )

    )

    conn.commit()


def get_designs(project_id):

    cursor.execute(

        """
        SELECT *
        FROM designs
        WHERE project_id=?
        ORDER BY created_at DESC
        """,

        (project_id,)
    )

    return cursor.fetchall()