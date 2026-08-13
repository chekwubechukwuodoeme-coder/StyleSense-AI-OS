import sqlite3

from database.profiles import DB_PATH


print("Database location:")
print(DB_PATH)

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""")

tables = cursor.fetchall()

print("\nTables:")
print(tables)

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    AND name = 'fashion_profiles'
""")

result = cursor.fetchone()

if result:
    print("\n✅ fashion_profiles EXISTS")
else:
    print("\n❌ fashion_profiles DOES NOT EXIST")

conn.close()