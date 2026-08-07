import sqlite3

conn = sqlite3.connect(
    "stylesense.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS planner(

id INTEGER PRIMARY KEY AUTOINCREMENT,

user_id INTEGER,

title TEXT,

status TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()


def create_task(user_id, title):

    cursor.execute(
        """
        INSERT INTO planner(
        user_id,
        title,
        status
        )

        VALUES(?,?,?)
        """,

        (
            user_id,
            title,
            "Pending"
        )
    )

    conn.commit()


def get_tasks(user_id):

    cursor.execute(

        """
        SELECT *
        FROM planner
        WHERE user_id=?
        """,

        (user_id,)
    )

    return cursor.fetchall()