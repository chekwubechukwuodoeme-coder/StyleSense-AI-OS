import sqlite3

conn = sqlite3.connect(
    "stylesense.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS saved_feed(

id INTEGER PRIMARY KEY AUTOINCREMENT,

user_id INTEGER,

title TEXT,

image TEXT,

source TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()


def save_feed(user_id, title, image, source):

    cursor.execute("""

    INSERT INTO saved_feed(

    user_id,
    title,
    image,
    source

    )

    VALUES(?,?,?,?)

    """, (

        user_id,
        title,
        image,
        source

    ))

    conn.commit()


def get_saved_feed(user_id):

    cursor.execute("""

    SELECT *

    FROM saved_feed

    WHERE user_id=?

    ORDER BY created_at DESC

    """,(user_id,))

    return cursor.fetchall()