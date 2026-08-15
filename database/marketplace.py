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

    try:

        cursor = conn.cursor()

        # ----------------------------------------------------
        # Check whether table exists
        # ----------------------------------------------------

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'marketplace_listings'
        """)

        table_exists = cursor.fetchone()

        # ----------------------------------------------------
        # CREATE TABLE
        # ----------------------------------------------------

        if not table_exists:

            cursor.execute("""
                CREATE TABLE marketplace_listings (

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

        else:

            # ------------------------------------------------
            # Get existing columns
            # ------------------------------------------------

            cursor.execute(
                "PRAGMA table_info(marketplace_listings)"
            )

            existing_columns = {
                row[1]
                for row in cursor.fetchall()
            }

            # ------------------------------------------------
            # Add missing columns
            # ------------------------------------------------

            for column_name, column_type in REQUIRED_COLUMNS.items():

                if column_name not in existing_columns:

                    cursor.execute(
                        f"""
                        ALTER TABLE marketplace_listings
                        ADD COLUMN {column_name} {column_type}
                        """
                    )

            # ------------------------------------------------
            # Migrate old "name" column if it exists
            # ------------------------------------------------

            if "name" in existing_columns:

                cursor.execute("""
                    UPDATE marketplace_listings

                    SET title = name

                    WHERE
                        (title IS NULL OR title = '')
                        AND name IS NOT NULL
                """)

            # ------------------------------------------------
            # Migrate old "contact" column if it exists
            # ------------------------------------------------

            if "contact" in existing_columns:

                cursor.execute("""
                    UPDATE marketplace_listings

                    SET phone = contact

                    WHERE
                        (phone IS NULL OR phone = '')
                        AND contact IS NOT NULL
                """)

            # ------------------------------------------------
            # Migrate old "seller" column if it exists
            # ------------------------------------------------

            if "seller" in existing_columns:

                cursor.execute("""
                    UPDATE marketplace_listings

                    SET seller_name = seller

                    WHERE
                        (seller_name IS NULL OR seller_name = '')
                        AND seller IS NOT NULL
                """)

        conn.commit()

    finally:

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

    title = str(title).strip()
    listing_type = str(listing_type).strip()
    category = str(category).strip()
    seller_name = str(seller_name).strip()

    if not title:
        raise ValueError("Listing title is required.")

    if not listing_type:
        raise ValueError("Listing type is required.")

    if not category:
        raise ValueError("Category is required.")

    if not seller_name:
        raise ValueError("Seller name is required.")

    conn = get_connection()

    try:

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
            title,
            listing_type,
            category,
            seller_name,
            str(location).strip(),
            str(description).strip(),
            str(price).strip(),
            str(image_url).strip(),
            str(phone).strip(),
            str(whatsapp).strip()

        ))

        conn.commit()

        return cursor.lastrowid

    finally:

        conn.close()


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