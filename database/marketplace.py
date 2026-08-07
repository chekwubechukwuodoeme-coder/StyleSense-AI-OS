import sqlite3

conn = sqlite3.connect(
    "stylesense.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS designers(

id INTEGER PRIMARY KEY AUTOINCREMENT,

user_id INTEGER,

business_name TEXT,

owner_name TEXT,

city TEXT,

country TEXT,

specialty TEXT,

bio TEXT,

phone TEXT,

email TEXT,

price_range TEXT

)
""")

conn.commit()


def add_designer(
    user_id,
    business_name,
    owner_name,
    city,
    country,
    specialty,
    bio,
    phone,
    email,
    price_range
):

    cursor.execute("""

    INSERT INTO designers(

    user_id,

    business_name,

    owner_name,

    city,

    country,

    specialty,

    bio,

    phone,

    email,

    price_range

    )

    VALUES(?,?,?,?,?,?,?,?,?,?)

    """,(

        user_id,

        business_name,

        owner_name,

        city,

        country,

        specialty,

        bio,

        phone,

        email,

        price_range

    ))

    conn.commit()


def get_designers():

    cursor.execute("""

    SELECT *

    FROM designers

    ORDER BY business_name

    """)

    return cursor.fetchall()