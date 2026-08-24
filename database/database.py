from pathlib import Path
import sqlite3
import ast


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "stylesense.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """

    connection = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# DATABASE HELPERS
# ============================================================

def table_exists(cursor, table_name):
    """
    Check whether a SQLite table exists.
    """

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = ?
        """,
        (table_name,)
    )

    return cursor.fetchone() is not None


def get_table_columns(cursor, table_name):
    """
    Return all existing columns in a SQLite table.
    """

    if not table_exists(cursor, table_name):
        return set()

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    return {
        row["name"]
        for row in cursor.fetchall()
    }


def add_missing_columns(
    cursor,
    table_name,
    columns
):
    """
    Add missing columns to an existing table.

    Existing data is preserved.
    """

    if not table_exists(
        cursor,
        table_name
    ):
        return

    existing_columns = get_table_columns(
        cursor,
        table_name
    )

    for column_name, column_definition in columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE {table_name}
                ADD COLUMN {column_name}
                {column_definition}
                """
            )


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_database():
    """
    Initialize and migrate the complete StyleSense database.

    Existing data is preserved.
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        # ====================================================
        # PROJECTS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL,

                description TEXT,

                category TEXT,

                cover_image TEXT,

                created_at
                    TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # ====================================================
        # FASHION PROFILES
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS fashion_profiles (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                profile_type TEXT NOT NULL,

                description TEXT,

                location TEXT,

                specialties TEXT,

                contact TEXT,

                image_url TEXT,

                created_at
                    TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # ====================================================
        # DESIGNS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS designs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                design TEXT,

                image_data BLOB,

                mode TEXT,

                category TEXT,

                gender TEXT,

                age TEXT,

                height TEXT,

                body_shape TEXT,

                skin_tone TEXT,

                fabric TEXT,

                colors TEXT,

                colour TEXT,

                occasion TEXT,

                budget TEXT,

                complexity TEXT,

                theme TEXT,

                country TEXT,

                climate TEXT,

                embroidery INTEGER DEFAULT 0,

                accessories INTEGER DEFAULT 0,

                style TEXT,

                market TEXT,

                culture TEXT,

                reference_image INTEGER DEFAULT 0,

                reference_source TEXT,

                preserve_silhouette INTEGER DEFAULT 0,

                change_fabric INTEGER DEFAULT 0,

                change_colour INTEGER DEFAULT 0,

                change_style INTEGER DEFAULT 0,

                preserve_details INTEGER DEFAULT 0,

                professional_presentation INTEGER DEFAULT 0,

                created_at
                    TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # ====================================================
        # DESIGN GENERATION JOBS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS design_jobs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                job_id TEXT UNIQUE NOT NULL,

                user_id TEXT,

                job_type TEXT,

                prompt TEXT,

                status TEXT DEFAULT 'pending',

                image_data BLOB,

                error TEXT,

                created_at
                    TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                completed_at
                    TIMESTAMP
            )
            """
        )

        # ====================================================
        # MEASUREMENT PROFILES
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS measurement_profiles (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id TEXT,

                client_name TEXT NOT NULL,

                category TEXT,

                unit TEXT DEFAULT 'in',

                head REAL DEFAULT 0,

                height REAL DEFAULT 0,

                bust REAL DEFAULT 0,

                shoulder REAL DEFAULT 0,

                sleeve REAL DEFAULT 0,

                neck REAL DEFAULT 0,

                armhole REAL DEFAULT 0,

                garment_length REAL DEFAULT 0,

                waist REAL DEFAULT 0,

                hip REAL DEFAULT 0,

                trouser_length REAL DEFAULT 0,

                inseam REAL DEFAULT 0,

                thigh REAL DEFAULT 0,

                knee REAL DEFAULT 0,

                calf REAL DEFAULT 0,

                ankle REAL DEFAULT 0,

                client_photos TEXT DEFAULT '[]',

                fabric_photos TEXT DEFAULT '[]',

                notes TEXT,

                created_at
                    TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                updated_at
                    TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # ====================================================
        # PRODUCTION ORDERS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS production_orders (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id TEXT,

                order_number TEXT,

                garment_name TEXT NOT NULL,

                design_name TEXT,

                client TEXT,

                client_name TEXT,

                category TEXT,

                fabric TEXT,

                quantity INTEGER DEFAULT 1,

                status TEXT DEFAULT 'Pending',

                priority TEXT DEFAULT 'Normal',

                start_date TEXT,

                due_date TEXT,

                deadline TEXT,

                assigned_to TEXT,

                measurement_profile_id INTEGER,

                tech_pack_id INTEGER,

                notes TEXT,

                progress INTEGER DEFAULT 0,

                estimated_cost REAL DEFAULT 0,

                actual_cost REAL DEFAULT 0,

                created_at
                    TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                updated_at
                    TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # ====================================================
        # PRODUCTION ORDER MIGRATION
        # ====================================================

        production_columns = {

            "user_id":
                "TEXT",

            "order_number":
                "TEXT",

            "garment_name":
                "TEXT",

            "design_name":
                "TEXT",

            "client":
                "TEXT",

            "client_name":
                "TEXT",

            "category":
                "TEXT",

            "fabric":
                "TEXT",

            "quantity":
                "INTEGER DEFAULT 1",

            "status":
                "TEXT DEFAULT 'Pending'",

            "priority":
                "TEXT DEFAULT 'Normal'",

            "start_date":
                "TEXT",

            "due_date":
                "TEXT",

            "deadline":
                "TEXT",

            "assigned_to":
                "TEXT",

            "measurement_profile_id":
                "INTEGER",

            "tech_pack_id":
                "INTEGER",

            "notes":
                "TEXT",

            "progress":
                "INTEGER DEFAULT 0",

            "estimated_cost":
                "REAL DEFAULT 0",

            "actual_cost":
                "REAL DEFAULT 0",

            "created_at":
                "TIMESTAMP",

            "updated_at":
                "TIMESTAMP"
        }

        add_missing_columns(
            cursor,
            "production_orders",
            production_columns
        )

        # ====================================================
        # DESIGN MIGRATION
        # ====================================================

        design_columns = {

            "design":
                "TEXT",

            "image_data":
                "BLOB",

            "mode":
                "TEXT",

            "category":
                "TEXT",

            "gender":
                "TEXT",

            "age":
                "TEXT",

            "height":
                "TEXT",

            "body_shape":
                "TEXT",

            "skin_tone":
                "TEXT",

            "fabric":
                "TEXT",

            "colors":
                "TEXT",

            "colour":
                "TEXT",

            "occasion":
                "TEXT",

            "budget":
                "TEXT",

            "complexity":
                "TEXT",

            "theme":
                "TEXT",

            "country":
                "TEXT",

            "climate":
                "TEXT",

            "embroidery":
                "INTEGER DEFAULT 0",

            "accessories":
                "INTEGER DEFAULT 0",

            "style":
                "TEXT",

            "market":
                "TEXT",

            "culture":
                "TEXT",

            "reference_image":
                "INTEGER DEFAULT 0",

            "reference_source":
                "TEXT",

            "preserve_silhouette":
                "INTEGER DEFAULT 0",

            "change_fabric":
                "INTEGER DEFAULT 0",

            "change_colour":
                "INTEGER DEFAULT 0",

            "change_style":
                "INTEGER DEFAULT 0",

            "preserve_details":
                "INTEGER DEFAULT 0",

            "professional_presentation":
                "INTEGER DEFAULT 0",

            "created_at":
                "TIMESTAMP"
        }

        add_missing_columns(
            cursor,
            "designs",
            design_columns
        )

        # ====================================================
        # MEASUREMENT MIGRATION
        # ====================================================

        measurement_columns = {

            "user_id":
                "TEXT",

            "client_name":
                "TEXT",

            "category":
                "TEXT",

            "unit":
                "TEXT DEFAULT 'in'",

            "head":
                "REAL DEFAULT 0",

            "height":
                "REAL DEFAULT 0",

            "bust":
                "REAL DEFAULT 0",

            "shoulder":
                "REAL DEFAULT 0",

            "sleeve":
                "REAL DEFAULT 0",

            "neck":
                "REAL DEFAULT 0",

            "armhole":
                "REAL DEFAULT 0",

            "garment_length":
                "REAL DEFAULT 0",

            "waist":
                "REAL DEFAULT 0",

            "hip":
                "REAL DEFAULT 0",

            "trouser_length":
                "REAL DEFAULT 0",

            "inseam":
                "REAL DEFAULT 0",

            "thigh":
                "REAL DEFAULT 0",

            "knee":
                "REAL DEFAULT 0",

            "calf":
                "REAL DEFAULT 0",

            "ankle":
                "REAL DEFAULT 0",

            "client_photos":
                "TEXT DEFAULT '[]'",

            "fabric_photos":
                "TEXT DEFAULT '[]'",

            "notes":
                "TEXT",

            "created_at":
                "TIMESTAMP",

            "updated_at":
                "TIMESTAMP"
        }

        add_missing_columns(
            cursor,
            "measurement_profiles",
            measurement_columns
        )

        # ====================================================
        # INDEXES
        # ====================================================

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_measurement_client_name
            ON measurement_profiles(client_name)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_measurement_user_id
            ON measurement_profiles(user_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_production_user_id
            ON production_orders(user_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_production_status
            ON production_orders(status)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_production_due_date
            ON production_orders(due_date)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_production_start_date
            ON production_orders(start_date)
            """
        )

        conn.commit()

        print(
            "StyleSense database initialized successfully."
        )

    finally:

        conn.close()


# ============================================================
# MEASUREMENT PHOTO HELPERS
# ============================================================

def _serialize_list(value):

    if value is None:
        return "[]"

    if isinstance(value, list):
        return repr(value)

    return repr([value])


def _deserialize_list(value):

    if not value:
        return []

    if isinstance(value, list):
        return value

    try:

        result = ast.literal_eval(
            str(value)
        )

        if isinstance(result, list):
            return result

    except Exception:
        pass

    return []


# ============================================================
# MEASUREMENT PROFILES
# ============================================================

def save_measurement_profile(
    profile_data
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO measurement_profiles (

                user_id,
                client_name,
                category,
                unit,

                head,
                height,
                bust,
                shoulder,
                sleeve,
                neck,
                armhole,
                garment_length,

                waist,
                hip,
                trouser_length,
                inseam,
                thigh,
                knee,
                calf,
                ankle,

                client_photos,
                fabric_photos,

                notes
            )

            VALUES (

                ?, ?, ?, ?,

                ?, ?, ?, ?, ?, ?, ?, ?,

                ?, ?, ?, ?, ?, ?, ?, ?,

                ?, ?,

                ?
            )
            """,
            (

                profile_data.get(
                    "user_id"
                ),

                profile_data.get(
                    "client_name",
                    ""
                ),

                profile_data.get(
                    "category",
                    ""
                ),

                profile_data.get(
                    "unit",
                    "in"
                ),

                profile_data.get(
                    "head",
                    0
                ),

                profile_data.get(
                    "height",
                    0
                ),

                profile_data.get(
                    "bust",
                    0
                ),

                profile_data.get(
                    "shoulder",
                    0
                ),

                profile_data.get(
                    "sleeve",
                    0
                ),

                profile_data.get(
                    "neck",
                    0
                ),

                profile_data.get(
                    "armhole",
                    0
                ),

                profile_data.get(
                    "garment_length",
                    0
                ),

                profile_data.get(
                    "waist",
                    0
                ),

                profile_data.get(
                    "hip",
                    0
                ),

                profile_data.get(
                    "trouser_length",
                    0
                ),

                profile_data.get(
                    "inseam",
                    0
                ),

                profile_data.get(
                    "thigh",
                    0
                ),

                profile_data.get(
                    "knee",
                    0
                ),

                profile_data.get(
                    "calf",
                    0
                ),

                profile_data.get(
                    "ankle",
                    0
                ),

                _serialize_list(
                    profile_data.get(
                        "client_photos",
                        []
                    )
                ),

                _serialize_list(
                    profile_data.get(
                        "fabric_photos",
                        []
                    )
                ),

                profile_data.get(
                    "notes",
                    ""
                )
            )
        )

        profile_id = cursor.lastrowid

        conn.commit()

        return profile_id

    finally:

        conn.close()


def get_measurement_profiles(
    user_id=None
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        if user_id:

            cursor.execute(
                """
                SELECT *
                FROM measurement_profiles
                WHERE user_id = ?
                ORDER BY id DESC
                """,
                (user_id,)
            )

        else:

            cursor.execute(
                """
                SELECT *
                FROM measurement_profiles
                ORDER BY id DESC
                """
            )

        profiles = []

        for row in cursor.fetchall():

            profile = dict(row)

            profile["client_photos"] = (
                _deserialize_list(
                    profile.get(
                        "client_photos"
                    )
                )
            )

            profile["fabric_photos"] = (
                _deserialize_list(
                    profile.get(
                        "fabric_photos"
                    )
                )
            )

            profiles.append(profile)

        return profiles

    finally:

        conn.close()


def get_measurement_profile(
    profile_id
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM measurement_profiles
            WHERE id = ?
            """,
            (profile_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        profile = dict(row)

        profile["client_photos"] = (
            _deserialize_list(
                profile.get(
                    "client_photos"
                )
            )
        )

        profile["fabric_photos"] = (
            _deserialize_list(
                profile.get(
                    "fabric_photos"
                )
            )
        )

        return profile

    finally:

        conn.close()


def update_measurement_profile(
    profile_id,
    profile_data
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE measurement_profiles

            SET

                client_name = ?,
                category = ?,
                unit = ?,

                head = ?,
                height = ?,
                bust = ?,
                shoulder = ?,
                sleeve = ?,
                neck = ?,
                armhole = ?,
                garment_length = ?,

                waist = ?,
                hip = ?,
                trouser_length = ?,
                inseam = ?,
                thigh = ?,
                knee = ?,
                calf = ?,
                ankle = ?,

                client_photos = ?,
                fabric_photos = ?,

                notes = ?,

                updated_at =
                    CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (

                profile_data.get(
                    "client_name",
                    ""
                ),

                profile_data.get(
                    "category",
                    ""
                ),

                profile_data.get(
                    "unit",
                    "in"
                ),

                profile_data.get(
                    "head",
                    0
                ),

                profile_data.get(
                    "height",
                    0
                ),

                profile_data.get(
                    "bust",
                    0
                ),

                profile_data.get(
                    "shoulder",
                    0
                ),

                profile_data.get(
                    "sleeve",
                    0
                ),

                profile_data.get(
                    "neck",
                    0
                ),

                profile_data.get(
                    "armhole",
                    0
                ),

                profile_data.get(
                    "garment_length",
                    0
                ),

                profile_data.get(
                    "waist",
                    0
                ),

                profile_data.get(
                    "hip",
                    0
                ),

                profile_data.get(
                    "trouser_length",
                    0
                ),

                profile_data.get(
                    "inseam",
                    0
                ),

                profile_data.get(
                    "thigh",
                    0
                ),

                profile_data.get(
                    "knee",
                    0
                ),

                profile_data.get(
                    "calf",
                    0
                ),

                profile_data.get(
                    "ankle",
                    0
                ),

                _serialize_list(
                    profile_data.get(
                        "client_photos",
                        []
                    )
                ),

                _serialize_list(
                    profile_data.get(
                        "fabric_photos",
                        []
                    )
                ),

                profile_data.get(
                    "notes",
                    ""
                ),

                profile_id
            )
        )

        updated = cursor.rowcount > 0

        conn.commit()

        return updated

    finally:

        conn.close()


def delete_measurement_profile(
    profile_id
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM measurement_profiles
            WHERE id = ?
            """,
            (profile_id,)
        )

        deleted = cursor.rowcount > 0

        conn.commit()

        return deleted

    finally:

        conn.close()


# ============================================================
# PRODUCTION ORDERS
# ============================================================

def _safe_garment_name(order_data):
    """
    Always return a non-empty garment name.

    This prevents:

        NOT NULL constraint failed:
        production_orders.garment_name
    """

    possible_names = [

        order_data.get(
            "garment_name"
        ),

        order_data.get(
            "design_name"
        ),

        order_data.get(
            "garment"
        ),

        order_data.get(
            "design"
        ),

        order_data.get(
            "title"
        ),

        order_data.get(
            "name"
        )
    ]

    for value in possible_names:

        if value is not None:

            value = str(value).strip()

            if value:
                return value

    category = str(
        order_data.get(
            "category",
            ""
        )
    ).strip()

    if category:
        return f"{category} Production"

    return "Untitled Production Order"


def _safe_client_name(order_data):
    """
    Support both client and client_name.
    """

    client = (
        order_data.get("client")
        or
        order_data.get("client_name")
    )

    if client is None:
        return ""

    return str(client).strip()


def create_production_order(
    order_data
):
    """
    Create a new production order.

    Supports:

    - garment_name
    - design_name
    - client
    - client_name
    - measurement_profile_id
    - tech_pack_id
    - fabric
    - start_date
    - due_date
    - deadline
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        garment_name = _safe_garment_name(
            order_data
        )

        client_name = _safe_client_name(
            order_data
        )

        status = str(
            order_data.get(
                "status",
                "Pending"
            )
        ).strip()

        if not status:
            status = "Pending"

        progress = order_data.get(
            "progress"
        )

        if progress is None:

            progress = _status_to_progress(
                status
            )

        quantity = order_data.get(
            "quantity",
            1
        )

        try:
            quantity = int(quantity)
        except Exception:
            quantity = 1

        if quantity < 1:
            quantity = 1

        start_date = (
            order_data.get(
                "start_date"
            )
            or
            order_data.get(
                "production_start_date"
            )
            or
            ""
        )

        due_date = (
            order_data.get(
                "due_date"
            )
            or
            order_data.get(
                "deadline"
            )
            or
            ""
        )

        deadline = (
            order_data.get(
                "deadline"
            )
            or
            order_data.get(
                "due_date"
            )
            or
            ""
        )

        cursor.execute(
            """
            INSERT INTO production_orders (

                user_id,

                order_number,

                garment_name,

                design_name,

                client,

                client_name,

                category,

                fabric,

                quantity,

                status,

                priority,

                start_date,

                due_date,

                deadline,

                assigned_to,

                measurement_profile_id,

                tech_pack_id,

                notes,

                progress,

                estimated_cost,

                actual_cost

            )

            VALUES (

                ?, ?, ?, ?, ?, ?, ?, ?,

                ?, ?, ?, ?, ?, ?, ?, ?, ?,

                ?, ?, ?, ?, ?
            )
            """,
            (

                order_data.get(
                    "user_id"
                ),

                order_data.get(
                    "order_number"
                ),

                garment_name,

                order_data.get(
                    "design_name",
                    garment_name
                ),

                client_name,

                client_name,

                order_data.get(
                    "category",
                    "Other"
                ),

                order_data.get(
                    "fabric",
                    ""
                ),

                quantity,

                status,

                order_data.get(
                    "priority",
                    "Normal"
                ),

                start_date,

                due_date,

                deadline,

                order_data.get(
                    "assigned_to",
                    "Unassigned"
                ),

                order_data.get(
                    "measurement_profile_id"
                ),

                order_data.get(
                    "tech_pack_id"
                ),

                order_data.get(
                    "notes",
                    ""
                ),

                progress,

                order_data.get(
                    "estimated_cost",
                    0
                ),

                order_data.get(
                    "actual_cost",
                    0
                )
            )
        )

        order_id = cursor.lastrowid

        conn.commit()

        return order_id

    finally:

        conn.close()


def get_production_orders(
    user_id=None
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        if user_id:

            cursor.execute(
                """
                SELECT *
                FROM production_orders
                WHERE user_id = ?
                ORDER BY id DESC
                """,
                (user_id,)
            )

        else:

            cursor.execute(
                """
                SELECT *
                FROM production_orders
                ORDER BY id DESC
                """
            )

        orders = []

        for row in cursor.fetchall():

            order = dict(row)

            # ------------------------------------------------
            # BACKWARD COMPATIBILITY
            # ------------------------------------------------

            if not order.get("client_name"):

                order["client_name"] = (
                    order.get("client")
                    or
                    ""
                )

            if not order.get("client"):

                order["client"] = (
                    order.get("client_name")
                    or
                    ""
                )

            if not order.get("design_name"):

                order["design_name"] = (
                    order.get("garment_name")
                    or
                    ""
                )

            if not order.get("due_date"):

                order["due_date"] = (
                    order.get("deadline")
                    or
                    ""
                )

            orders.append(order)

        return orders

    finally:

        conn.close()


def get_production_order(
    order_id
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM production_orders
            WHERE id = ?
            """,
            (order_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        order = dict(row)

        if not order.get("client_name"):

            order["client_name"] = (
                order.get("client")
                or
                ""
            )

        if not order.get("client"):

            order["client"] = (
                order.get("client_name")
                or
                ""
            )

        if not order.get("design_name"):

            order["design_name"] = (
                order.get("garment_name")
                or
                ""
            )

        if not order.get("due_date"):

            order["due_date"] = (
                order.get("deadline")
                or
                ""
            )

        return order

    finally:

        conn.close()


def update_production_order(
    order_id,
    order_data
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        garment_name = _safe_garment_name(
            order_data
        )

        client_name = _safe_client_name(
            order_data
        )

        status = order_data.get(
            "status",
            "Pending"
        )

        progress = order_data.get(
            "progress"
        )

        if progress is None:

            progress = _status_to_progress(
                status
            )

        start_date = (
            order_data.get(
                "start_date"
            )
            or
            ""
        )

        due_date = (
            order_data.get(
                "due_date"
            )
            or
            order_data.get(
                "deadline"
            )
            or
            ""
        )

        deadline = (
            order_data.get(
                "deadline"
            )
            or
            order_data.get(
                "due_date"
            )
            or
            ""
        )

        cursor.execute(
            """
            UPDATE production_orders

            SET

                garment_name = ?,

                design_name = ?,

                client = ?,

                client_name = ?,

                category = ?,

                fabric = ?,

                quantity = ?,

                status = ?,

                priority = ?,

                start_date = ?,

                due_date = ?,

                deadline = ?,

                assigned_to = ?,

                measurement_profile_id = ?,

                tech_pack_id = ?,

                notes = ?,

                progress = ?,

                estimated_cost = ?,

                actual_cost = ?,

                updated_at =
                    CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (

                garment_name,

                order_data.get(
                    "design_name",
                    garment_name
                ),

                client_name,

                client_name,

                order_data.get(
                    "category",
                    "Other"
                ),

                order_data.get(
                    "fabric",
                    ""
                ),

                order_data.get(
                    "quantity",
                    1
                ),

                status,

                order_data.get(
                    "priority",
                    "Normal"
                ),

                start_date,

                due_date,

                deadline,

                order_data.get(
                    "assigned_to",
                    "Unassigned"
                ),

                order_data.get(
                    "measurement_profile_id"
                ),

                order_data.get(
                    "tech_pack_id"
                ),

                order_data.get(
                    "notes",
                    ""
                ),

                progress,

                order_data.get(
                    "estimated_cost",
                    0
                ),

                order_data.get(
                    "actual_cost",
                    0
                ),

                order_id
            )
        )

        updated = cursor.rowcount > 0

        conn.commit()

        return updated

    finally:

        conn.close()


def update_production_status(
    order_id,
    status
):

    progress = _status_to_progress(
        status
    )

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE production_orders

            SET

                status = ?,

                progress = ?,

                updated_at =
                    CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                status,
                progress,
                order_id
            )
        )

        updated = cursor.rowcount > 0

        conn.commit()

        return updated

    finally:

        conn.close()


def delete_production_order(
    order_id
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM production_orders
            WHERE id = ?
            """,
            (order_id,)
        )

        deleted = cursor.rowcount > 0

        conn.commit()

        return deleted

    finally:

        conn.close()


def get_production_statistics(
    user_id=None
):

    orders = get_production_orders(
        user_id
    )

    total = len(orders)

    active = sum(
        1
        for order in orders
        if order.get("status")
        == "In Production"
    )

    pending = sum(
        1
        for order in orders
        if order.get("status")
        == "Pending"
    )

    completed = sum(
        1
        for order in orders
        if order.get("status")
        == "Completed"
    )

    quality_check = sum(
        1
        for order in orders
        if order.get("status")
        == "Quality Check"
    )

    on_hold = sum(
        1
        for order in orders
        if order.get("status")
        == "On Hold"
    )

    return {

        "total":
            total,

        "active":
            active,

        "pending":
            pending,

        "completed":
            completed,

        "quality_check":
            quality_check,

        "on_hold":
            on_hold
    }


def _status_to_progress(
    status
):

    progress_map = {

        "Pending":
            0,

        "In Production":
            50,

        "Quality Check":
            80,

        "Completed":
            100,

        "On Hold":
            25
    }

    return progress_map.get(
        status,
        0
    )


# ============================================================
# DESIGN DATABASE
# ============================================================

def save_design_to_database(
    design_data
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        colors = design_data.get(
            "colors",
            []
        )

        if isinstance(
            colors,
            list
        ):

            colors_text = ", ".join(
                str(color)
                for color in colors
                if color
            )

        elif colors:

            colors_text = str(
                colors
            )

        else:

            colors_text = ""

        cursor.execute(
            """
            INSERT INTO designs (

                design,
                image_data,
                mode,
                category,

                gender,
                age,
                height,
                body_shape,
                skin_tone,

                fabric,
                colors,
                colour,

                occasion,
                budget,
                complexity,
                theme,

                country,
                climate,

                embroidery,
                accessories,

                style,
                market,
                culture,

                reference_image,
                reference_source,

                preserve_silhouette,
                change_fabric,
                change_colour,
                change_style,
                preserve_details,
                professional_presentation,

                created_at
            )

            VALUES (

                ?, ?, ?, ?,

                ?, ?, ?, ?, ?,

                ?, ?, ?,

                ?, ?, ?, ?,

                ?, ?,

                ?, ?,

                ?, ?, ?,

                ?, ?,

                ?, ?, ?, ?, ?, ?,

                COALESCE(
                    ?,
                    CURRENT_TIMESTAMP
                )
            )
            """,
            (

                design_data.get(
                    "design",
                    ""
                ),

                design_data.get(
                    "image_data"
                ),

                design_data.get(
                    "mode",
                    "Guided Design"
                ),

                design_data.get(
                    "category",
                    "AI Design"
                ),

                design_data.get(
                    "gender",
                    ""
                ),

                str(
                    design_data.get(
                        "age",
                        ""
                    )
                ),

                str(
                    design_data.get(
                        "height",
                        ""
                    )
                ),

                design_data.get(
                    "body_shape",
                    ""
                ),

                design_data.get(
                    "skin_tone",
                    ""
                ),

                design_data.get(
                    "fabric",
                    ""
                ),

                colors_text,

                design_data.get(
                    "colour",
                    ""
                ),

                design_data.get(
                    "occasion",
                    ""
                ),

                design_data.get(
                    "budget",
                    ""
                ),

                design_data.get(
                    "complexity",
                    ""
                ),

                design_data.get(
                    "theme",
                    ""
                ),

                design_data.get(
                    "country",
                    ""
                ),

                design_data.get(
                    "climate",
                    ""
                ),

                1 if design_data.get(
                    "embroidery",
                    False
                ) else 0,

                1 if design_data.get(
                    "accessories",
                    False
                ) else 0,

                design_data.get(
                    "style",
                    ""
                ),

                design_data.get(
                    "market",
                    ""
                ),

                design_data.get(
                    "culture",
                    ""
                ),

                1 if design_data.get(
                    "reference_image",
                    False
                ) else 0,

                design_data.get(
                    "reference_source",
                    ""
                ),

                1 if design_data.get(
                    "preserve_silhouette",
                    False
                ) else 0,

                1 if design_data.get(
                    "change_fabric",
                    False
                ) else 0,

                1 if design_data.get(
                    "change_colour",
                    False
                ) else 0,

                1 if design_data.get(
                    "change_style",
                    False
                ) else 0,

                1 if design_data.get(
                    "preserve_details",
                    False
                ) else 0,

                1 if design_data.get(
                    "professional_presentation",
                    False
                ) else 0,

                design_data.get(
                    "created_at"
                )
            )
        )

        design_id = cursor.lastrowid

        conn.commit()

        return design_id

    finally:

        conn.close()


def _parse_colors(
    colors
):

    if not colors:
        return []

    if isinstance(
        colors,
        list
    ):
        return colors

    try:

        parsed = ast.literal_eval(
            str(colors)
        )

        if isinstance(
            parsed,
            list
        ):

            return [
                str(color).strip()
                for color in parsed
                if color
            ]

    except Exception:
        pass

    return [
        color.strip()
        for color in str(
            colors
        ).split(",")
        if color.strip()
    ]


def get_all_designs():

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM designs
            ORDER BY id DESC
            """
        )

        designs = []

        boolean_fields = [

            "embroidery",

            "accessories",

            "reference_image",

            "preserve_silhouette",

            "change_fabric",

            "change_colour",

            "change_style",

            "preserve_details",

            "professional_presentation"
        ]

        for row in cursor.fetchall():

            design = dict(row)

            design["colors"] = _parse_colors(
                design.get(
                    "colors"
                )
            )

            for field in boolean_fields:

                if field in design:

                    design[field] = bool(
                        design[field]
                    )

            image_data = design.get(
                "image_data"
            )

            if image_data:

                design["image"] = bytes(
                    image_data
                )

            else:

                design["image"] = None

            designs.append(
                design
            )

        return designs

    finally:

        conn.close()


def get_design_by_id(
    design_id
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM designs
            WHERE id = ?
            """,
            (design_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        design = dict(row)

        design["colors"] = _parse_colors(
            design.get(
                "colors"
            )
        )

        boolean_fields = [

            "embroidery",

            "accessories",

            "reference_image",

            "preserve_silhouette",

            "change_fabric",

            "change_colour",

            "change_style",

            "preserve_details",

            "professional_presentation"
        ]

        for field in boolean_fields:

            if field in design:

                design[field] = bool(
                    design[field]
                )

        image_data = design.get(
            "image_data"
        )

        design["image"] = (
            bytes(image_data)
            if image_data
            else None
        )

        return design

    finally:

        conn.close()


def delete_design(
    design_id
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM designs
            WHERE id = ?
            """,
            (design_id,)
        )

        deleted = (
            cursor.rowcount > 0
        )

        conn.commit()

        return deleted

    finally:

        conn.close()


def clear_all_designs():

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM designs
            """
        )

        deleted_count = (
            cursor.rowcount
        )

        conn.commit()

        return deleted_count

    finally:

        conn.close()


def update_design(
    design_id,
    design_data
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        colors = design_data.get(
            "colors",
            []
        )

        if isinstance(
            colors,
            list
        ):

            colors = ", ".join(
                str(color)
                for color in colors
                if color
            )

        elif colors:

            colors = str(
                colors
            )

        else:

            colors = ""

        cursor.execute(
            """
            UPDATE designs

            SET

                design = ?,
                mode = ?,
                category = ?,

                gender = ?,
                age = ?,
                height = ?,
                body_shape = ?,
                skin_tone = ?,

                fabric = ?,
                colors = ?,
                colour = ?,

                occasion = ?,
                budget = ?,
                complexity = ?,
                theme = ?,

                country = ?,
                climate = ?,

                embroidery = ?,
                accessories = ?,

                style = ?,
                market = ?,
                culture = ?,

                reference_image = ?,
                reference_source = ?,

                preserve_silhouette = ?,
                change_fabric = ?,
                change_colour = ?,
                change_style = ?,
                preserve_details = ?,
                professional_presentation = ?

            WHERE id = ?
            """,
            (

                design_data.get(
                    "design",
                    ""
                ),

                design_data.get(
                    "mode",
                    "Guided Design"
                ),

                design_data.get(
                    "category",
                    "AI Design"
                ),

                design_data.get(
                    "gender",
                    ""
                ),

                str(
                    design_data.get(
                        "age",
                        ""
                    )
                ),

                str(
                    design_data.get(
                        "height",
                        ""
                    )
                ),

                design_data.get(
                    "body_shape",
                    ""
                ),

                design_data.get(
                    "skin_tone",
                    ""
                ),

                design_data.get(
                    "fabric",
                    ""
                ),

                colors,

                design_data.get(
                    "colour",
                    ""
                ),

                design_data.get(
                    "occasion",
                    ""
                ),

                design_data.get(
                    "budget",
                    ""
                ),

                design_data.get(
                    "complexity",
                    ""
                ),

                design_data.get(
                    "theme",
                    ""
                ),

                design_data.get(
                    "country",
                    ""
                ),

                design_data.get(
                    "climate",
                    ""
                ),

                1 if design_data.get(
                    "embroidery",
                    False
                ) else 0,

                1 if design_data.get(
                    "accessories",
                    False
                ) else 0,

                design_data.get(
                    "style",
                    ""
                ),

                design_data.get(
                    "market",
                    ""
                ),

                design_data.get(
                    "culture",
                    ""
                ),

                1 if design_data.get(
                    "reference_image",
                    False
                ) else 0,

                design_data.get(
                    "reference_source",
                    ""
                ),

                1 if design_data.get(
                    "preserve_silhouette",
                    False
                ) else 0,

                1 if design_data.get(
                    "change_fabric",
                    False
                ) else 0,

                1 if design_data.get(
                    "change_colour",
                    False
                ) else 0,

                1 if design_data.get(
                    "change_style",
                    False
                ) else 0,

                1 if design_data.get(
                    "preserve_details",
                    False
                ) else 0,

                1 if design_data.get(
                    "professional_presentation",
                    False
                ) else 0,

                design_id
            )
        )

        updated = (
            cursor.rowcount > 0
        )

        conn.commit()

        return updated

    finally:

        conn.close()


# ============================================================
# DESIGN JOBS
# ============================================================

def create_design_job(
    job_id,
    user_id,
    job_type,
    prompt
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO design_jobs (

                job_id,
                user_id,
                job_type,
                prompt,
                status

            )

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                job_id,
                user_id,
                job_type,
                prompt,
                "pending"
            )
        )

        conn.commit()

        return job_id

    finally:

        conn.close()


def get_design_job(
    job_id
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM design_jobs
            WHERE job_id = ?
            """,
            (job_id,)
        )

        row = cursor.fetchone()

        if row:

            return dict(row)

        return None

    finally:

        conn.close()


def update_design_job(
    job_id,
    status,
    image_data=None,
    error=None
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        if status == "completed":

            cursor.execute(
                """
                UPDATE design_jobs

                SET

                    status = ?,

                    image_data = ?,

                    completed_at =
                        CURRENT_TIMESTAMP

                WHERE job_id = ?
                """,
                (
                    status,
                    image_data,
                    job_id
                )
            )

        elif status == "failed":

            cursor.execute(
                """
                UPDATE design_jobs

                SET

                    status = ?,

                    error = ?,

                    completed_at =
                        CURRENT_TIMESTAMP

                WHERE job_id = ?
                """,
                (
                    status,
                    error,
                    job_id
                )
            )

        else:

            cursor.execute(
                """
                UPDATE design_jobs

                SET

                    status = ?

                WHERE job_id = ?
                """,
                (
                    status,
                    job_id
                )
            )

        conn.commit()

    finally:

        conn.close()


# ============================================================
# AUTO INITIALIZATION
# ============================================================

if __name__ == "__main__":

    init_database()

    print(
        f"Database location: {DB_PATH}"
    )