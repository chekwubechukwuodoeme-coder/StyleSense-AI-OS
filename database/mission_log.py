import sqlite3

conn = sqlite3.connect(
    "stylesense.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS mission_logs(

id INTEGER PRIMARY KEY AUTOINCREMENT,

command TEXT,

response TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()


def save_mission(command, response):

    cursor.execute(
        """
        INSERT INTO mission_logs(
            command,
            response
        )
        VALUES(?,?)
        """,
        (command, response)
    )

    conn.commit()