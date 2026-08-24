import sqlite3
from pathlib import Path


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "stylesense.db"
)


def get_connection():

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

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
    # CREATE MAIN MARKETPLACE TABLE
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

        WHERE
            title IS NULL
            OR title = ''
    """)

    cursor.execute("""
        UPDATE marketplace_listings

        SET seller_name = 'Unknown Seller'

        WHERE
            seller_name IS NULL
            OR seller_name = ''
    """)

    cursor.execute("""
        UPDATE marketplace_listings

        SET listing_type = 'Product'

        WHERE
            listing_type IS NULL
            OR listing_type = ''
    """)

    cursor.execute("""
        UPDATE marketplace_listings

        SET category = 'Other'

        WHERE
            category IS NULL
            OR category = ''
    """)

    # ========================================================
    # MULTIPLE MARKETPLACE IMAGES TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_listing_images (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            listing_id INTEGER NOT NULL,

            image_data BLOB NOT NULL,

            filename TEXT DEFAULT '',

            mime_type TEXT DEFAULT 'image/jpeg',

            sort_order INTEGER DEFAULT 0,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (listing_id)
                REFERENCES marketplace_listings(id)
                ON DELETE CASCADE
        )
    """)

    # ========================================================
    # INDEX FOR FASTER IMAGE LOOKUPS
    # ========================================================

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_marketplace_listing_images_listing_id

        ON marketplace_listing_images(listing_id)
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
        str(title).strip(),
        listing_type,
        category,
        str(seller_name).strip(),
        str(location).strip(),
        str(description).strip(),
        str(price).strip(),
        str(image_url).strip(),
        str(phone).strip(),
        str(whatsapp).strip()

    ))

    conn.commit()

    listing_id = cursor.lastrowid

    conn.close()

    return listing_id


# ============================================================
# ADD IMAGE TO LISTING
# ============================================================

def add_listing_image(
    listing_id,
    image_data,
    filename="",
    mime_type="image/jpeg",
    sort_order=0
):

    init_marketplace_table()

    conn = get_connection()

    try:

        conn.execute("""
            INSERT INTO marketplace_listing_images (

                listing_id,
                image_data,
                filename,
                mime_type,
                sort_order

            )

            VALUES (?, ?, ?, ?, ?)

        """, (

            listing_id,
            sqlite3.Binary(image_data),
            str(filename or ""),
            str(mime_type or "image/jpeg"),
            int(sort_order)

        ))

        conn.commit()

    finally:

        conn.close()


# ============================================================
# ADD MULTIPLE IMAGES
# ============================================================

def add_listing_images(
    listing_id,
    uploaded_images
):

    if not uploaded_images:
        return

    init_marketplace_table()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        # ----------------------------------------------------
        # Find current highest sort order
        # ----------------------------------------------------

        cursor.execute("""
            SELECT COALESCE(
                MAX(sort_order),
                -1
            )

            FROM marketplace_listing_images

            WHERE listing_id = ?
        """, (listing_id,))

        result = cursor.fetchone()

        current_order = (
            result[0]
            if result and result[0] is not None
            else -1
        )

        # ----------------------------------------------------
        # Insert images
        # ----------------------------------------------------

        for index, uploaded_file in enumerate(
            uploaded_images
        ):

            image_data = uploaded_file.getvalue()

            if not image_data:
                continue

            filename = (
                getattr(
                    uploaded_file,
                    "name",
                    ""
                )
                or ""
            )

            mime_type = (
                getattr(
                    uploaded_file,
                    "type",
                    None
                )
                or "image/jpeg"
            )

            cursor.execute("""
                INSERT INTO marketplace_listing_images (

                    listing_id,
                    image_data,
                    filename,
                    mime_type,
                    sort_order

                )

                VALUES (?, ?, ?, ?, ?)

            """, (

                listing_id,
                sqlite3.Binary(image_data),
                filename,
                mime_type,
                current_order + index + 1

            ))

        conn.commit()

    finally:

        conn.close()


# ============================================================
# GET LISTING IMAGES
# ============================================================

def get_listing_images(listing_id):

    init_marketplace_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            SELECT

                id,
                listing_id,
                image_data,
                filename,
                mime_type,
                sort_order,
                created_at

            FROM marketplace_listing_images

            WHERE listing_id = ?

            ORDER BY
                sort_order ASC,
                id ASC

        """, (listing_id,))

        return cursor.fetchall()

    finally:

        conn.close()


# ============================================================
# GET IMAGE COUNT
# ============================================================

def get_listing_image_count(listing_id):

    init_marketplace_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            SELECT COUNT(*)

            FROM marketplace_listing_images

            WHERE listing_id = ?

        """, (listing_id,))

        result = cursor.fetchone()

        return (
            result[0]
            if result
            else 0
        )

    finally:

        conn.close()


# ============================================================
# DELETE SINGLE LISTING IMAGE
# ============================================================

def delete_listing_image(
    image_id,
    listing_id
):

    init_marketplace_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            DELETE FROM marketplace_listing_images

            WHERE
                id = ?
                AND listing_id = ?

        """, (
            image_id,
            listing_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    finally:

        conn.close()


# ============================================================
# DELETE ALL LISTING IMAGES
# ============================================================

def delete_all_listing_images(
    listing_id
):

    init_marketplace_table()

    conn = get_connection()

    try:

        cursor = conn.execute("""
            DELETE FROM marketplace_listing_images

            WHERE listing_id = ?

        """, (listing_id,))

        conn.commit()

        return cursor.rowcount > 0

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

            search_value = (
                f"%{search.strip()}%"
            )

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

        if (
            category
            and category != "All"
        ):

            query += """
                AND category = ?
            """

            values.append(category)

        # ----------------------------------------------------
        # LISTING TYPE
        # ----------------------------------------------------

        if (
            listing_type
            and listing_type != "All"
        ):

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

        # ----------------------------------------------------
        # Delete images first
        # ----------------------------------------------------

        conn.execute("""
            DELETE FROM marketplace_listing_images

            WHERE listing_id = ?

        """, (listing_id,))

        # ----------------------------------------------------
        # Delete listing
        # ----------------------------------------------------

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