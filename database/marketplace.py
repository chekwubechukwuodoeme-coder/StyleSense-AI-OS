import sqlite3
from pathlib import Path


# ============================================================
# DATABASE
# ============================================================

DB_PATH = Path(__file__).resolve().parent.parent / "stylesense.db"


def get_connection():
    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


# ============================================================
# CATEGORIES
# ============================================================

MARKETPLACE_CATEGORIES = [
    "Clothing",
    "Fabrics & Textiles",
    "Shoes",
    "Bags",
    "Jewelry",
    "Accessories",
    "Makeup & Beauty",
    "Fashion Tools & Equipment",

    "Fashion Designer",
    "Tailor",
    "Stylist",
    "Fashion Photographer",
    "Makeup Artist",
    "Hair Stylist",
    "Shoemaker",
    "Bag Maker",
    "Jewelry Maker",
    "Fashion Illustrator",
    "Pattern Maker",
    "Fashion Consultant",

    "Fashion Manufacturer",
    "Fabric Seller",
    "Clothing Seller",

    "Fashion Service",
    "Other",
]


LISTING_TYPES = [
    "Product",
    "Professional",
    "Service",
]


# ============================================================
# INITIALIZE / MIGRATE MARKETPLACE
# ============================================================

def init_marketplace_table():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Check table
    # --------------------------------------------------------

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'marketplace_listings'
    """)

    exists = cursor.fetchone()

    # --------------------------------------------------------
    # Create new table
    # --------------------------------------------------------

    if not exists:

        cursor.execute("""
            CREATE TABLE marketplace_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                title TEXT NOT NULL,
                listing_type TEXT NOT NULL,
                category TEXT NOT NULL,

                seller_name TEXT NOT NULL,
                location TEXT,

                description TEXT,
                price TEXT,
                image_url TEXT,

                phone TEXT,
                whatsapp TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    else:

        # ----------------------------------------------------
        # Read existing columns
        # ----------------------------------------------------

        cursor.execute(
            "PRAGMA table_info(marketplace_listings)"
        )

        columns = {
            row[1]
            for row in cursor.fetchall()
        }

        # ----------------------------------------------------
        # Add user_id
        # ----------------------------------------------------

        if "user_id" not in columns:

            cursor.execute("""
                ALTER TABLE marketplace_listings
                ADD COLUMN user_id INTEGER
            """)

        # ----------------------------------------------------
        # Add title
        # ----------------------------------------------------

        if "title" not in columns:

            cursor.execute("""
                ALTER TABLE marketplace_listings
                ADD COLUMN title TEXT
            """)

            if "name" in columns:

                cursor.execute("""
                    UPDATE marketplace_listings
                    SET title = name
                    WHERE title IS NULL
                    OR title = ''
                """)

        # ----------------------------------------------------
        # Add phone
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Add WhatsApp
        # ----------------------------------------------------

        if "whatsapp" not in columns:

            cursor.execute("""
                ALTER TABLE marketplace_listings
                ADD COLUMN whatsapp TEXT
            """)

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
            name,
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

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        user_id,
        title.strip(),
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
    cursor = conn.cursor()

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

        WHERE 1=1
    """

    values = []

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    if search.strip():

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

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------

    if category != "All":

        query += """
            AND category = ?
        """

        values.append(category)

    # --------------------------------------------------------
    # Listing type
    # --------------------------------------------------------

    if listing_type != "All":

        query += """
            AND listing_type = ?
        """

        values.append(listing_type)

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    if location.strip():

        query += """
            AND location LIKE ?
        """

        values.append(
            f"%{location.strip()}%"
        )

    # --------------------------------------------------------
    # Newest first
    # --------------------------------------------------------

    query += """
        ORDER BY created_at DESC
    """

    cursor.execute(
        query,
        values
    )

    listings = cursor.fetchall()

    conn.close()

    return listings


# ============================================================
# GET SINGLE LISTING
# ============================================================

def get_listing(listing_id):

    init_marketplace_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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

    listing = cursor.fetchone()

    conn.close()

    return listing


# ============================================================
# GET USER'S LISTINGS
# ============================================================

def get_user_listings(user_id):

    init_marketplace_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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

    listings = cursor.fetchall()

    conn.close()

    return listings


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
    cursor = conn.cursor()

    cursor.execute("""
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

        title.strip(),
        listing_type,
        category,
        seller_name.strip(),
        location.strip(),
        description.strip(),
        price.strip(),
        image_url.strip(),
        phone.strip(),
        whatsapp.strip(),

        listing_id,
        user_id

    ))

    updated = cursor.rowcount

    conn.commit()
    conn.close()

    return updated > 0


# ============================================================
# DELETE LISTING
# ============================================================

def delete_listing(
    listing_id,
    user_id
):

    init_marketplace_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM marketplace_listings

        WHERE
            id = ?
            AND user_id = ?
    """, (
        listing_id,
        user_id
    ))

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted > 0