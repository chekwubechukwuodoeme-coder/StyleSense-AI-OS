from pathlib import Path
import sqlite3


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

def get_table_columns(cursor, table_name):
    """
    Return the existing columns in a SQLite table.
    """

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    return {
        row["name"]
        for row in cursor.fetchall()
    }


def add_missing_columns(cursor, table_name, columns):
    """
    Add missing columns to an existing table.

    This allows old StyleSense databases to migrate
    automatically without deleting existing data.
    """

    existing_columns = get_table_columns(
        cursor,
        table_name
    )

    for column_name, column_definition in columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE {table_name}
                ADD COLUMN {column_name} {column_definition}
                """
            )


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_database():
    """
    Initialize and migrate the StyleSense database.
    """

    conn = get_connection()

    cursor = conn.cursor()

    # ========================================================
    # PROJECTS
    # ========================================================

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

    # ========================================================
    # FASHION PROFILES
    # ========================================================

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

    # ========================================================
    # DESIGNS
    # ========================================================

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

    # ============================================================
    # DESIGN GENERATION JOBS
    # ============================================================

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

    # ========================================================
    # MIGRATE OLD DESIGNS TABLE
    # ========================================================

    design_columns = {

        "design": "TEXT",

        "image_data": "BLOB",

        "mode": "TEXT",

        "category": "TEXT",

        "gender": "TEXT",

        "age": "TEXT",

        "height": "TEXT",

        "body_shape": "TEXT",

        "skin_tone": "TEXT",

        "fabric": "TEXT",

        "colors": "TEXT",

        "colour": "TEXT",

        "occasion": "TEXT",

        "budget": "TEXT",

        "complexity": "TEXT",

        "theme": "TEXT",

        "country": "TEXT",

        "climate": "TEXT",

        "embroidery": "INTEGER DEFAULT 0",

        "accessories": "INTEGER DEFAULT 0",

        "style": "TEXT",

        "market": "TEXT",

        "culture": "TEXT",

        "reference_image": "INTEGER DEFAULT 0",

        "reference_source": "TEXT",

        "preserve_silhouette": "INTEGER DEFAULT 0",

        "change_fabric": "INTEGER DEFAULT 0",

        "change_colour": "INTEGER DEFAULT 0",

        "change_style": "INTEGER DEFAULT 0",

        "preserve_details": "INTEGER DEFAULT 0",

        "professional_presentation": "INTEGER DEFAULT 0",

        "created_at": "TIMESTAMP"
    }

    add_missing_columns(
        cursor,
        "designs",
        design_columns
    )

    print(
        "DESIGNS COLUMNS:",
        get_table_columns(cursor, "designs")
    )

    conn.commit()

    conn.close()


# ============================================================
# SAVE DESIGN
# ============================================================

def save_design_to_database(design_data):
    """
    Save an AI-generated fashion design.

    Returns:
        int: ID of the saved design.
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        # ----------------------------------------------------
        # COLORS
        # ----------------------------------------------------

        colors = design_data.get(
            "colors",
            []
        )

        if isinstance(colors, list):

            colors_text = ", ".join(
                str(color)
                for color in colors
                if color
            )

        elif colors:

            colors_text = str(colors)

        else:

            colors_text = ""

        # ----------------------------------------------------
        # INSERT
        # ----------------------------------------------------

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

                ?,
                ?,
                ?,
                ?,

                ?,
                ?,
                ?,
                ?,
                ?,

                ?,
                ?,
                ?,

                ?,
                ?,
                ?,
                ?,

                ?,
                ?,

                ?,
                ?,

                ?,
                ?,
                ?,

                ?,
                ?,

                ?,
                ?,
                ?,
                ?,
                ?,
                ?,

                COALESCE(?, CURRENT_TIMESTAMP)
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


# ============================================================
# GET ALL DESIGNS
# ============================================================

def get_all_designs():
    """
    Return all saved designs from newest to oldest.
    """

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

        rows = cursor.fetchall()

        designs = []

        for row in rows:

            design = dict(row)

            # ------------------------------------------------
            # COLORS
            # ------------------------------------------------

            colors = design.get(
                "colors"
            )

            if colors:

                if isinstance(colors, str):

                    # Handle both:
                    # "red, black"
                    # and
                    # "['red', 'black']"

                    try:

                        parsed = ast_literal_eval(
                            colors
                        )

                        if isinstance(
                            parsed,
                            list
                        ):

                            design["colors"] = [
                                str(color).strip()
                                for color in parsed
                                if color
                            ]

                        else:

                            design["colors"] = [
                                color.strip()
                                for color in colors.split(",")
                                if color.strip()
                            ]

                    except Exception:

                        design["colors"] = [
                            color.strip()
                            for color in colors.split(",")
                            if color.strip()
                        ]

            else:

                design["colors"] = []

            # ------------------------------------------------
            # BOOLEAN FIELDS
            # ------------------------------------------------

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

            # ------------------------------------------------
            # IMAGE
            # ------------------------------------------------

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


# ============================================================
# SAFE AST PARSER
# ============================================================

def ast_literal_eval(value):

    import ast

    return ast.literal_eval(value)


# ============================================================
# GET DESIGN BY ID
# ============================================================

def get_design_by_id(design_id):

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

        # ----------------------------------------------------
        # COLORS
        # ----------------------------------------------------

        colors = design.get(
            "colors"
        )

        if colors:

            try:

                parsed = ast_literal_eval(
                    colors
                )

                if isinstance(
                    parsed,
                    list
                ):

                    design["colors"] = [
                        str(color).strip()
                        for color in parsed
                        if color
                    ]

                else:

                    design["colors"] = [
                        color.strip()
                        for color in str(
                            colors
                        ).split(",")
                        if color.strip()
                    ]

            except Exception:

                design["colors"] = [
                    color.strip()
                    for color in str(
                        colors
                    ).split(",")
                    if color.strip()
                ]

        else:

            design["colors"] = []

        # ----------------------------------------------------
        # BOOLEAN FIELDS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------

        image_data = design.get(
            "image_data"
        )

        if image_data:

            design["image"] = bytes(
                image_data
            )

        else:

            design["image"] = None

        return design

    finally:

        conn.close()


# ============================================================
# DELETE ONE DESIGN
# ============================================================

def delete_design(design_id):

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


# ============================================================
# DELETE ALL DESIGNS
# ============================================================

def clear_all_designs():

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM designs
            """
        )

        deleted_count = cursor.rowcount

        conn.commit()

        return deleted_count

    finally:

        conn.close()


# ============================================================
# UPDATE DESIGN
# ============================================================

def update_design(
    design_id,
    design_data
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        # ----------------------------------------------------
        # COLORS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # UPDATE
        # ----------------------------------------------------

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
# GET DESIGN JOB
# ============================================================

def get_design_job(job_id):

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


# ============================================================
# UPDATE JOB STATUS
# ============================================================

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
                    completed_at = CURRENT_TIMESTAMP

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
                    completed_at = CURRENT_TIMESTAMP

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

                SET status = ?

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
# DESIGN GENERATION JOBS
# ============================================================

def create_design_job(
    job_id,
    user_id,
    job_type,
    prompt
):
    """
    Create a persistent AI design generation job.
    """

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