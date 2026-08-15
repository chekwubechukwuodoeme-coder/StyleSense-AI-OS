import sqlite3
from pathlib import Path


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_PATH = Path(__file__).resolve().parent.parent / "stylesense.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    return conn


# ============================================================
# MARKETPLACE OPTIONS
# ============================================================

MARKETPLACE_CATEGORIES = [
    # Products
    "Clothing",
    "Fabrics & Textiles",
    "Shoes",
    "Bags",
    "Jewelry",
    "Accessories",
    "Makeup & Beauty",
    "Fashion Tools & Equipment",

    # Services
    "Fashion Services",
    "Tailoring Services",
    "Fashion Design Services",
    "Styling Services",
    "Photography Services",
    "Videography Services",
    "Makeup Services",
    "Hair Services",
    "Fashion Illustration Services",
    "Pattern Making Services",
    "Embroidery Services",
    "Fashion Production Services",
    "Fashion Consulting Services",

    "Other",
]


LISTING_TYPES = [
    "Product",
    "Service",
]


# ============================================================
# REQUIRED COLUMNS
# ============================================================

REQUIRED_COLUMNS = {
    "user_id": "INTEGER",
    "title": "TEXT",
    "listing_type": "TEXT",
    "category": "TEXT",
    "seller_name": "TEXT",
    "location": "TEXT",
    "description": "TEXT",
    "price": "TEXT",
    "image_url": "TEXT",
    "phone": "TEXT",
    "whatsapp": "TEXT",
    "created_at": "TIMESTAMP",
}


# ============================================================
# INITIALIZE / MIGRATE MARKETPLACE
# ============================================================

def init_marketplace_table():

    conn = get_connection()
    cursor = conn.cursor()

    # ========================================================
    # CREATE TABLE IF IT DOES NOT EXIST
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_listings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            title TEXT NOT NULL,

            listing_type TEXT NOT NULL,

            category TEXT NOT NULL,

            seller_name TEXT NOT NULL,

            location TEXT DEFAULT '',

            description TEXT DEFAULT '',

            price TEXT DEFAULT '',

            image_url TEXT DEFAULT '',

            phone TEXT DEFAULT '',

            whatsapp TEXT DEFAULT '',

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ========================================================
    # CHECK EXISTING COLUMNS
    # ========================================================

    cursor.execute(
        "PRAGMA table_info(marketplace_listings)"
    )

    columns = {
        row[1]
        for row in cursor.fetchall()
    }

    # ========================================================
    # MIGRATE OLD DATABASE
    # ========================================================

    if "user_id" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN user_id INTEGER
        """)

    if "title" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN title TEXT
        """)

        if "name" in columns:

            cursor.execute("""
                UPDATE marketplace_listings

                SET title = name

                WHERE
                    title IS NULL
                    OR title = ''
            """)

    if "listing_type" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN listing_type TEXT
        """)

    if "category" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN category TEXT
        """)

    if "seller_name" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN seller_name TEXT
        """)

        if "name" in columns:

            cursor.execute("""
                UPDATE marketplace_listings

                SET seller_name = name

                WHERE
                    seller_name IS NULL
                    OR seller_name = ''
            """)

    if "location" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN location TEXT
        """)

    if "description" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN description TEXT
        """)

    if "price" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN price TEXT
        """)

    if "image_url" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN image_url TEXT
        """)

    if "phone" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN phone TEXT
        """)

        if "contact" in columns:

            cursor.execute("""
                UPDATE marketplace_listings

                SET phone = contact

                WHERE
                    (phone IS NULL OR phone = '')
                    AND contact IS NOT NULL
            """)

    if "whatsapp" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN whatsapp TEXT
        """)

    if "created_at" not in columns:

        cursor.execute("""
            ALTER TABLE marketplace_listings
            ADD COLUMN created_at TIMESTAMP
        """)

    # ========================================================
    # FIX OLD NULL VALUES
    # ========================================================

    cursor.execute("""
        UPDATE marketplace_listings

        SET title = 'Untitled Listing'

        WHERE title IS NULL
        OR title = ''
    """)

    cursor.execute("""
        UPDATE marketplace_listings

        SET seller_name = 'Unknown Seller'

        WHERE seller_name IS NULL
        OR seller_name = ''
    """)

    cursor.execute("""
        UPDATE marketplace_listings

        SET listing_type = 'Product'

        WHERE listing_type IS NULL
        OR listing_type = ''
    """)

    cursor.execute("""
        UPDATE marketplace_listings

        SET category = 'Other'

        WHERE category IS NULL
        OR category = ''
    """)

    # ========================================================
    # SAVE
    # ========================================================

    conn.commit()
    conn.close()


# ============================================================
# CREATE LISTING
# ============================================================

def create_listing(
    user_id,
    title,
    listing_type,
    category,
    seller_name,
    location="",
    description="",
    price="",
    image_url="",
    phone="",
    whatsapp=""
):

    init_marketplace_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO marketplace_listings (

            user_id,
            title,
            listing_type,
            category,
            seller_name,
            location,
            description,
            price,
            image_url,
            phone,
            whatsapp

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        user_id,
        title.strip(),
        listing_type,
        category,
        seller_name.strip(),
        location.strip(),
        description.strip(),
        price.strip(),
        image_url.strip(),
        phone.strip(),
        whatsapp.strip()

    ))

    conn.commit()

    listing_id = cursor.lastrowid

    conn.close()

    return listing_id


# ============================================================
# GET ALL LISTINGS
# ============================================================

def get_listings(
    search="",
    category="All",
    listing_type="All",
    location=""
):

    init_marketplace_table()

    conn = get_connection()

    try:

        query = """
            SELECT

                id,
                user_id,
                title,
                listing_type,
                category,
                seller_name,
                location,
                description,
                price,
                image_url,
                phone,
                whatsapp,
                created_at

            FROM marketplace_listings

            WHERE 1 = 1
        """

        values = []

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        if search and search.strip():

            search_value = f"%{search.strip()}%"

            query += """
                AND (
                    title LIKE ?
                    OR description LIKE ?
                    OR seller_name LIKE ?
                    OR category LIKE ?
                    OR location LIKE ?
                )
            """

            values.extend([
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            ])

        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        if category and category != "All":

            query += """
                AND category = ?
            """

            values.append(category)

        # ----------------------------------------------------
        # LISTING TYPE
        # ----------------------------------------------------

        if listing_type and listing_type != "All":

            query += """
                AND listing_type = ?
            """

            values.append(listing_type)

        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------

        if location and location.strip():

            query += """
                AND location LIKE ?
            """

            values.append(
                f"%{location.strip()}%"
            )

        # ----------------------------------------------------
        # SORT
        # ----------------------------------------------------

        query += """
            ORDER BY created_at DESC
        """

        cursor = conn.execute(
            query,
            values
        )

        return cursor.fetchall()

    finally:

        conn.close()


# ============================================================
# GET SINGLE LISTING
# ============================================================

def get_listing(listing_id):

    init_marketplace_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            SELECT

                id,
                user_id,
                title,
                listing_type,
                category,
                seller_name,
                location,
                description,
                price,
                image_url,
                phone,
                whatsapp,
                created_at

            FROM marketplace_listings

            WHERE id = ?

        """, (listing_id,))

        return cursor.fetchone()

    finally:

        conn.close()


# ============================================================
# GET USER LISTINGS
# ============================================================

def get_user_listings(user_id):

    init_marketplace_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            SELECT

                id,
                user_id,
                title,
                listing_type,
                category,
                seller_name,
                location,
                description,
                price,
                image_url,
                phone,
                whatsapp,
                created_at

            FROM marketplace_listings

            WHERE user_id = ?

            ORDER BY created_at DESC

        """, (user_id,))

        return cursor.fetchall()

    finally:

        conn.close()


# ============================================================
# UPDATE LISTING
# ============================================================

def update_listing(
    listing_id,
    user_id,
    title,
    listing_type,
    category,
    seller_name,
    location="",
    description="",
    price="",
    image_url="",
    phone="",
    whatsapp=""
):

    init_marketplace_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            UPDATE marketplace_listings

            SET

                title = ?,
                listing_type = ?,
                category = ?,
                seller_name = ?,
                location = ?,
                description = ?,
                price = ?,
                image_url = ?,
                phone = ?,
                whatsapp = ?

            WHERE
                id = ?
                AND user_id = ?

        """, (

            str(title).strip(),
            listing_type,
            category,
            str(seller_name).strip(),
            str(location).strip(),
            str(description).strip(),
            str(price).strip(),
            str(image_url).strip(),
            str(phone).strip(),
            str(whatsapp).strip(),

            listing_id,
            user_id

        ))

        conn.commit()

        return cursor.rowcount > 0

    finally:

        conn.close()


# ============================================================
# DELETE LISTING
# ============================================================

def delete_listing(
    listing_id,
    user_id
):

    init_marketplace_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            DELETE FROM marketplace_listings

            WHERE
                id = ?
                AND user_id = ?

        """, (
            listing_id,
            user_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    finally:

        conn.close()


# ============================================================
# INITIALIZE ON IMPORT
# ============================================================

init_marketplace_table()