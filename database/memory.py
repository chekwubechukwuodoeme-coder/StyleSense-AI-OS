import sqlite3

conn = sqlite3.connect(
    "stylesense.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory(

id INTEGER PRIMARY KEY AUTOINCREMENT,

user_id INTEGER,

key TEXT,

value TEXT

)
""")

conn.commit()


def save_memory(user_id, key, value):

    cursor.execute("""

    INSERT INTO memory(
    user_id,
    key,
    value
    )

    VALUES(?,?,?)

    """, (user_id, key, value))

    conn.commit()


def get_memory(user_id):

    cursor.execute("""

    SELECT key,value

    FROM memory

    WHERE user_id=?

    """, (user_id,))

    rows = cursor.fetchall()

    return {
        row[0]: row[1]
        for row in rows
    }