import sqlite3

from database.marketplace import DB_PATH

conn = sqlite3.connect(DB_PATH)

columns = conn.execute(
    "PRAGMA table_info(marketplace_listings)"
).fetchall()

print("\nDATABASE:", DB_PATH)
print("\nMARKETPLACE TABLE COLUMNS:")

for column in columns:
    print(column)

conn.close()