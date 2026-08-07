import sqlite3

conn = sqlite3.connect(
    "stylesense.db",
    check_same_thread=False
)

cursor = conn.cursor()


def count_projects():

    cursor.execute("SELECT COUNT(*) FROM projects")

    return cursor.fetchone()[0]


def count_designers():

    cursor.execute("SELECT COUNT(*) FROM designers")

    return cursor.fetchone()[0]


def count_missions():

    cursor.execute("SELECT COUNT(*) FROM mission_logs")

    return cursor.fetchone()[0]