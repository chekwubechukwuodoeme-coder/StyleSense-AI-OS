import streamlit as st
import sqlite3
import json
import base64

from database.database import get_connection


# ============================================================
# DATABASE HELPERS
# ============================================================

def get_user_id():
    return st.session_state.get("user_id")


def table_columns(conn, table_name):
    cursor = conn.cursor()

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    return {
        row[1]
        for row in cursor.fetchall()
    }


def ensure_measurement_table():

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS measurement_profiles (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id TEXT NOT NULL,
                client_name TEXT NOT NULL,

                category TEXT,
                unit TEXT,

                height REAL DEFAULT 0,
                bust REAL DEFAULT 0,
                shoulder REAL DEFAULT 0,

                sleeve REAL DEFAULT 0,

                long_arm REAL DEFAULT 0,
                short_arm REAL DEFAULT 0,

                neck REAL DEFAULT 0,

                armhole REAL DEFAULT 0,
                armhole_type TEXT DEFAULT 'Standard',

                garment_length REAL DEFAULT 0,
                head REAL DEFAULT 0,

                waist REAL DEFAULT 0,
                hip REAL DEFAULT 0,

                trouser_length REAL DEFAULT 0,
                inseam REAL DEFAULT 0,
                thigh REAL DEFAULT 0,
                knee REAL DEFAULT 0,
                calf REAL DEFAULT 0,
                ankle REAL DEFAULT 0,

                client_photos TEXT,
                fabric_photos TEXT,

                notes TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()

        # ====================================================
        # SAFE DATABASE MIGRATION
        # ====================================================

        columns = table_columns(
            conn,
            "measurement_profiles"
        )

        required_columns = {

            "user_id":
                "TEXT",

            "client_name":
                "TEXT",

            "category":
                "TEXT",

            "unit":
                "TEXT",

            "height":
                "REAL DEFAULT 0",

            "bust":
                "REAL DEFAULT 0",

            "shoulder":
                "REAL DEFAULT 0",

            "sleeve":
                "REAL DEFAULT 0",

            "long_arm":
                "REAL DEFAULT 0",

            "short_arm":
                "REAL DEFAULT 0",

            "neck":
                "REAL DEFAULT 0",

            "armhole":
                "REAL DEFAULT 0",

            "armhole_type":
                "TEXT DEFAULT 'Standard'",

            "garment_length":
                "REAL DEFAULT 0",

            "head":
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
                "TEXT",

            "fabric_photos":
                "TEXT",

            "notes":
                "TEXT",

            "created_at":
                "TIMESTAMP",

            "updated_at":
                "TIMESTAMP",
        }

        for column, definition in required_columns.items():

            if column not in columns:

                try:

                    cursor.execute(
                        f"""
                        ALTER TABLE measurement_profiles
                        ADD COLUMN {column} {definition}
                        """
                    )

                except sqlite3.OperationalError:
                    pass

        conn.commit()

    finally:

        conn.close()


# ============================================================
# IMAGE HELPERS
# ============================================================

def image_to_base64(file_bytes):

    if not file_bytes:
        return None

    return base64.b64encode(
        file_bytes
    ).decode("utf-8")


def base64_to_bytes(value):

    if not value:
        return None

    try:

        return base64.b64decode(value)

    except Exception:

        return None


def encode_photos(photos):

    return json.dumps(
        [
            image_to_base64(photo)
            for photo in (photos or [])
            if photo
        ]
    )


def decode_photos(value):

    photos = []

    try:

        stored_photos = json.loads(
            value or "[]"
        )

        for photo in stored_photos:

            decoded = base64_to_bytes(
                photo
            )

            if decoded:
                photos.append(decoded)

    except Exception:

        pass

    return photos


# ============================================================
# LOAD MEASUREMENT PROFILES
# ============================================================

def get_measurement_profiles():

    user_id = get_user_id()

    if not user_id:
        return []

    ensure_measurement_table()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                client_name,
                category,
                unit,

                height,
                bust,
                shoulder,

                sleeve,
                long_arm,
                short_arm,

                neck,

                armhole,
                armhole_type,

                garment_length,
                head,

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

                notes,
                created_at,
                updated_at

            FROM measurement_profiles

            WHERE user_id = ?

            ORDER BY id DESC
            """,
            (
                str(user_id),
            )
        )

        rows = cursor.fetchall()

        # ====================================================
        # IMPORTANT FIX
        #
        # Instead of assuming row[0], row[1], row[2] etc.,
        # map the returned columns by their actual names.
        #
        # This prevents "tuple index out of range".
        # ====================================================

        column_names = [
            description[0]
            for description in cursor.description
        ]

        profiles = []

        for row in rows:

            data = dict(
                zip(
                    column_names,
                    row
                )
            )

            profiles.append(
                {
                    "id":
                        data.get("id"),

                    "client_name":
                        data.get(
                            "client_name",
                            ""
                        ),

                    "category":
                        data.get(
                            "category",
                            ""
                        ),

                    "unit":
                        data.get(
                            "unit",
                            "in"
                        ),

                    "height":
                        data.get(
                            "height",
                            0
                        ) or 0,

                    "bust":
                        data.get(
                            "bust",
                            0
                        ) or 0,

                    "shoulder":
                        data.get(
                            "shoulder",
                            0
                        ) or 0,

                    "sleeve":
                        data.get(
                            "sleeve",
                            0
                        ) or 0,

                    "long_arm":
                        data.get(
                            "long_arm",
                            0
                        ) or 0,

                    "short_arm":
                        data.get(
                            "short_arm",
                            0
                        ) or 0,

                    "neck":
                        data.get(
                            "neck",
                            0
                        ) or 0,

                    "armhole":
                        data.get(
                            "armhole",
                            0
                        ) or 0,

                    "armhole_type":
                        data.get(
                            "armhole_type",
                            "Standard"
                        ) or "Standard",

                    "garment_length":
                        data.get(
                            "garment_length",
                            0
                        ) or 0,

                    "head":
                        data.get(
                            "head",
                            0
                        ) or 0,

                    "waist":
                        data.get(
                            "waist",
                            0
                        ) or 0,

                    "hip":
                        data.get(
                            "hip",
                            0
                        ) or 0,

                    "trouser_length":
                        data.get(
                            "trouser_length",
                            0
                        ) or 0,

                    "inseam":
                        data.get(
                            "inseam",
                            0
                        ) or 0,

                    "thigh":
                        data.get(
                            "thigh",
                            0
                        ) or 0,

                    "knee":
                        data.get(
                            "knee",
                            0
                        ) or 0,

                    "calf":
                        data.get(
                            "calf",
                            0
                        ) or 0,

                    "ankle":
                        data.get(
                            "ankle",
                            0
                        ) or 0,

                    "client_photos":
                        decode_photos(
                            data.get(
                                "client_photos"
                            )
                        ),

                    "fabric_photos":
                        decode_photos(
                            data.get(
                                "fabric_photos"
                            )
                        ),

                    "notes":
                        data.get(
                            "notes",
                            ""
                        ) or "",

                    "created_at":
                        data.get(
                            "created_at"
                        ),

                    "updated_at":
                        data.get(
                            "updated_at"
                        ),
                }
            )

        return profiles

    except Exception as e:

        st.error(
            f"Unable to load measurement profiles: {e}"
        )

        return []

    finally:

        conn.close()


# ============================================================
# SAVE NEW MEASUREMENT PROFILE
# ============================================================

def save_measurement_profile(profile):

    user_id = get_user_id()

    if not user_id:

        return False, "No logged-in user found."

    ensure_measurement_table()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        client_photos = encode_photos(
            profile.get(
                "client_photos",
                []
            )
        )

        fabric_photos = encode_photos(
            profile.get(
                "fabric_photos",
                []
            )
        )

        cursor.execute(
            """
            INSERT INTO measurement_profiles (

                user_id,
                client_name,
                category,
                unit,

                height,
                bust,
                shoulder,

                sleeve,
                long_arm,
                short_arm,

                neck,

                armhole,
                armhole_type,

                garment_length,
                head,

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

                ?, ?, ?,

                ?, ?, ?,

                ?,

                ?, ?,

                ?, ?,

                ?, ?,

                ?, ?, ?, ?, ?, ?,

                ?, ?,

                ?
            )
            """,
            (

                str(user_id),

                profile.get(
                    "client_name",
                    ""
                ),

                profile.get(
                    "category",
                    ""
                ),

                profile.get(
                    "unit",
                    "in"
                ),

                profile.get(
                    "height",
                    0
                ),

                profile.get(
                    "bust",
                    0
                ),

                profile.get(
                    "shoulder",
                    0
                ),

                profile.get(
                    "sleeve",
                    0
                ),

                profile.get(
                    "long_arm",
                    0
                ),

                profile.get(
                    "short_arm",
                    0
                ),

                profile.get(
                    "neck",
                    0
                ),

                profile.get(
                    "armhole",
                    0
                ),

                profile.get(
                    "armhole_type",
                    "Standard"
                ),

                profile.get(
                    "garment_length",
                    0
                ),

                profile.get(
                    "head",
                    0
                ),

                profile.get(
                    "waist",
                    0
                ),

                profile.get(
                    "hip",
                    0
                ),

                profile.get(
                    "trouser_length",
                    0
                ),

                profile.get(
                    "inseam",
                    0
                ),

                profile.get(
                    "thigh",
                    0
                ),

                profile.get(
                    "knee",
                    0
                ),

                profile.get(
                    "calf",
                    0
                ),

                profile.get(
                    "ankle",
                    0
                ),

                client_photos,

                fabric_photos,

                profile.get(
                    "notes",
                    ""
                ),
            )
        )

        conn.commit()

        return True, cursor.lastrowid

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        conn.close()


# ============================================================
# UPDATE MEASUREMENT PROFILE
# ============================================================

def update_measurement_profile(
    profile_id,
    profile
):

    user_id = get_user_id()

    if not user_id:

        return False, "No logged-in user found."

    ensure_measurement_table()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        client_photos = encode_photos(
            profile.get(
                "client_photos",
                []
            )
        )

        fabric_photos = encode_photos(
            profile.get(
                "fabric_photos",
                []
            )
        )

        cursor.execute(
            """
            UPDATE measurement_profiles

            SET

                client_name = ?,
                category = ?,
                unit = ?,

                height = ?,
                bust = ?,
                shoulder = ?,

                sleeve = ?,
                long_arm = ?,
                short_arm = ?,

                neck = ?,

                armhole = ?,
                armhole_type = ?,

                garment_length = ?,
                head = ?,

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

                updated_at = CURRENT_TIMESTAMP

            WHERE id = ?
            AND user_id = ?
            """,
            (

                profile.get(
                    "client_name",
                    ""
                ),

                profile.get(
                    "category",
                    ""
                ),

                profile.get(
                    "unit",
                    "in"
                ),

                profile.get(
                    "height",
                    0
                ),

                profile.get(
                    "bust",
                    0
                ),

                profile.get(
                    "shoulder",
                    0
                ),

                profile.get(
                    "sleeve",
                    0
                ),

                profile.get(
                    "long_arm",
                    0
                ),

                profile.get(
                    "short_arm",
                    0
                ),

                profile.get(
                    "neck",
                    0
                ),

                profile.get(
                    "armhole",
                    0
                ),

                profile.get(
                    "armhole_type",
                    "Standard"
                ),

                profile.get(
                    "garment_length",
                    0
                ),

                profile.get(
                    "head",
                    0
                ),

                profile.get(
                    "waist",
                    0
                ),

                profile.get(
                    "hip",
                    0
                ),

                profile.get(
                    "trouser_length",
                    0
                ),

                profile.get(
                    "inseam",
                    0
                ),

                profile.get(
                    "thigh",
                    0
                ),

                profile.get(
                    "knee",
                    0
                ),

                profile.get(
                    "calf",
                    0
                ),

                profile.get(
                    "ankle",
                    0
                ),

                client_photos,

                fabric_photos,

                profile.get(
                    "notes",
                    ""
                ),

                profile_id,

                str(user_id),
            )
        )

        conn.commit()

        if cursor.rowcount == 0:

            return (
                False,
                "Measurement profile was not found."
            )

        return (
            True,
            "Measurement profile updated successfully."
        )

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        conn.close()


# ============================================================
# DELETE
# ============================================================

def delete_measurement_profile(
    profile_id
):

    user_id = get_user_id()

    if not user_id:

        return False, "No logged-in user."

    ensure_measurement_table()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM measurement_profiles

            WHERE id = ?

            AND user_id = ?
            """,
            (
                profile_id,
                str(user_id)
            )
        )

        conn.commit()

        return (
            True,
            "Measurement profile deleted."
        )

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        conn.close()


# ============================================================
# MEASUREMENT INPUTS
# ============================================================

def measurement_number(
    label,
    value=0.0,
    key=None
):

    return st.number_input(
        label,
        min_value=0.0,
        value=float(value or 0),
        step=0.5,
        key=key,
    )


# ============================================================
# MAIN VIEW
# ============================================================

def render_measurements():

    ensure_measurement_table()

    st.title("📏 Measurements")

    st.caption(
        "Create and manage detailed client measurement "
        "profiles for your fashion production workflow."
    )

    st.divider()

    profiles_tab, create_tab = st.tabs(
        [
            "📋 Measurement Profiles",
            "➕ Add Measurements",
        ]
    )

    # ========================================================
    # SAVED PROFILES
    # ========================================================

    with profiles_tab:

        st.subheader(
            "📋 Saved Measurement Profiles"
        )

        profiles = get_measurement_profiles()

        search = st.text_input(
            "🔍 Search Client",
            placeholder="Search by client name...",
            key="measurement_search",
        )

        search = search.strip().lower()

        filtered_profiles = [

            profile

            for profile in profiles

            if (
                not search
                or search
                in profile[
                    "client_name"
                ].lower()
            )
        ]

        if not profiles:

            st.info(
                "No measurement profiles yet. "
                "Create your first client profile."
            )

        elif not filtered_profiles:

            st.warning(
                f'No client found matching "{search}".'
            )

        else:

            st.caption(
                f"{len(filtered_profiles)} "
                "measurement profile(s)"
            )

            for profile in filtered_profiles:

                client_name = profile[
                    "client_name"
                ]

                unit = profile.get(
                    "unit",
                    "in"
                )

                with st.expander(
                    f"👤 {client_name} • "
                    f"{profile.get('category', 'Fashion Client')}"
                ):

                    # ====================================================
                    # PROFILE INFORMATION
                    # ====================================================

                    st.markdown(
                        "### 👤 Client Information"
                    )

                    c1, c2 = st.columns(2)

                    with c1:

                        st.write(
                            f"**Client:** "
                            f"{client_name}"
                        )

                        st.write(
                            f"**Category:** "
                            f"{profile.get('category', '')}"
                        )

                    with c2:

                        st.write(
                            f"**Unit:** {unit}"
                        )

                        st.write(
                            f"**Profile ID:** "
                            f"{profile['id']}"
                        )

                    st.divider()

                    # ====================================================
                    # UPPER BODY
                    # ====================================================

                    st.markdown(
                        "### 👕 Upper Body"
                    )

                    c1, c2, c3 = st.columns(3)

                    with c1:

                        st.write(
                            f"**Height:** "
                            f"{profile.get('height', 0)} {unit}"
                        )

                        st.write(
                            f"**Bust / Chest:** "
                            f"{profile.get('bust', 0)} {unit}"
                        )

                        st.write(
                            f"**Shoulder:** "
                            f"{profile.get('shoulder', 0)} {unit}"
                        )

                    with c2:

                        st.write(
                            f"**Long Arm:** "
                            f"{profile.get('long_arm', 0)} {unit}"
                        )

                        st.write(
                            f"**Short Arm:** "
                            f"{profile.get('short_arm', 0)} {unit}"
                        )

                        st.write(
                            f"**Neck:** "
                            f"{profile.get('neck', 0)} {unit}"
                        )

                    with c3:

                        st.write(
                            f"**Armhole:** "
                            f"{profile.get('armhole', 0)} {unit}"
                        )

                        st.write(
                            f"**Armhole Type:** "
                            f"{profile.get('armhole_type', 'Standard')}"
                        )

                        st.write(
                            f"**Garment Length:** "
                            f"{profile.get('garment_length', 0)} {unit}"
                        )

                    st.write(
                        f"**Head:** "
                        f"{profile.get('head', 0)} {unit}"
                    )

                    st.divider()

                    # ====================================================
                    # LOWER BODY
                    # ====================================================

                    st.markdown(
                        "### 👖 Lower Body"
                    )

                    c1, c2, c3 = st.columns(3)

                    with c1:

                        st.write(
                            f"**Waist:** "
                            f"{profile.get('waist', 0)} {unit}"
                        )

                        st.write(
                            f"**Hip:** "
                            f"{profile.get('hip', 0)} {unit}"
                        )

                        st.write(
                            f"**Trouser Length:** "
                            f"{profile.get('trouser_length', 0)} {unit}"
                        )

                    with c2:

                        st.write(
                            f"**Inseam:** "
                            f"{profile.get('inseam', 0)} {unit}"
                        )

                        st.write(
                            f"**Thigh:** "
                            f"{profile.get('thigh', 0)} {unit}"
                        )

                        st.write(
                            f"**Knee:** "
                            f"{profile.get('knee', 0)} {unit}"
                        )

                    with c3:

                        st.write(
                            f"**Calf:** "
                            f"{profile.get('calf', 0)} {unit}"
                        )

                        st.write(
                            f"**Ankle / Hem Opening:** "
                            f"{profile.get('ankle', 0)} {unit}"
                        )

                    # ====================================================
                    # CLIENT PHOTOS
                    # ====================================================

                    client_photos = profile.get(
                        "client_photos",
                        []
                    )

                    if client_photos:

                        st.divider()

                        st.markdown(
                            "### 📸 Client Photos"
                        )

                        cols = st.columns(
                            min(
                                4,
                                len(client_photos)
                            )
                        )

                        for i, photo in enumerate(
                            client_photos
                        ):

                            with cols[
                                i % len(cols)
                            ]:

                                st.image(
                                    photo,
                                    use_container_width=True
                                )

                    # ====================================================
                    # FABRIC PHOTOS
                    # ====================================================

                    fabric_photos = profile.get(
                        "fabric_photos",
                        []
                    )

                    if fabric_photos:

                        st.divider()

                        st.markdown(
                            "### 🧵 Fabric Photos"
                        )

                        cols = st.columns(
                            min(
                                4,
                                len(fabric_photos)
                            )
                        )

                        for i, photo in enumerate(
                            fabric_photos
                        ):

                            with cols[
                                i % len(cols)
                            ]:

                                st.image(
                                    photo,
                                    use_container_width=True
                                )

                    # ====================================================
                    # NOTES
                    # ====================================================

                    if profile.get(
                        "notes"
                    ):

                        st.divider()

                        st.markdown(
                            "### 📝 Production Notes"
                        )

                        st.write(
                            profile["notes"]
                        )

                    st.divider()

                    # ====================================================
                    # EDIT PROFILE
                    # ====================================================

                    with st.expander(
                        "✏️ Edit Measurement Profile"
                    ):

                        st.markdown(
                            "### ✏️ Edit Client Information"
                        )

                        edit_client_name = st.text_input(
                            "Client Name",
                            value=profile.get(
                                "client_name",
                                ""
                            ),
                            key=(
                                f"edit_client_name_"
                                f"{profile['id']}"
                            ),
                        )

                        categories = [
                            "Women's Wear",
                            "Men's Wear",
                            "Children's Wear",
                            "Bridal",
                            "Traditional Wear",
                            "Sportswear",
                            "Casual Wear",
                            "Corporate Wear",
                            "Other",
                        ]

                        current_category = profile.get(
                            "category",
                            "Women's Wear"
                        )

                        if current_category not in categories:
                            current_category = categories[0]

                        edit_category = st.selectbox(
                            "Garment Category",
                            categories,
                            index=categories.index(
                                current_category
                            ),
                            key=(
                                f"edit_category_"
                                f"{profile['id']}"
                            ),
                        )

                        units = [
                            "in",
                            "cm"
                        ]

                        current_unit = profile.get(
                            "unit",
                            "in"
                        )

                        if current_unit not in units:
                            current_unit = "in"

                        edit_unit = st.radio(
                            "Measurement Unit",
                            units,
                            index=units.index(
                                current_unit
                            ),
                            horizontal=True,
                            key=(
                                f"edit_unit_"
                                f"{profile['id']}"
                            ),
                        )

                        st.divider()

                        # ====================================================
                        # EDIT UPPER BODY
                        # ====================================================

                        st.markdown(
                            "### 👕 Upper Body"
                        )

                        e1, e2, e3 = st.columns(3)

                        with e1:

                            edit_height = measurement_number(
                                f"Height ({edit_unit})",
                                profile.get(
                                    "height",
                                    0
                                ),
                                f"edit_height_{profile['id']}",
                            )

                            edit_bust = measurement_number(
                                f"Bust / Chest ({edit_unit})",
                                profile.get(
                                    "bust",
                                    0
                                ),
                                f"edit_bust_{profile['id']}",
                            )

                            edit_shoulder = measurement_number(
                                f"Shoulder ({edit_unit})",
                                profile.get(
                                    "shoulder",
                                    0
                                ),
                                f"edit_shoulder_{profile['id']}",
                            )

                        with e2:

                            edit_long_arm = measurement_number(
                                f"Long Arm ({edit_unit})",
                                profile.get(
                                    "long_arm",
                                    0
                                ),
                                f"edit_long_arm_{profile['id']}",
                            )

                            edit_short_arm = measurement_number(
                                f"Short Arm ({edit_unit})",
                                profile.get(
                                    "short_arm",
                                    0
                                ),
                                f"edit_short_arm_{profile['id']}",
                            )

                            edit_neck = measurement_number(
                                f"Neck ({edit_unit})",
                                profile.get(
                                    "neck",
                                    0
                                ),
                                f"edit_neck_{profile['id']}",
                            )

                        with e3:

                            edit_armhole = measurement_number(
                                f"Armhole ({edit_unit})",
                                profile.get(
                                    "armhole",
                                    0
                                ),
                                f"edit_armhole_{profile['id']}",
                            )

                            armhole_types = [
                                "Standard",
                                "Long",
                                "Short",
                            ]

                            current_armhole_type = profile.get(
                                "armhole_type",
                                "Standard"
                            )

                            if current_armhole_type not in armhole_types:
                                current_armhole_type = "Standard"

                            edit_armhole_type = st.selectbox(
                                "Armhole Type",
                                armhole_types,
                                index=armhole_types.index(
                                    current_armhole_type
                                ),
                                key=(
                                    f"edit_armhole_type_"
                                    f"{profile['id']}"
                                ),
                            )

                            edit_garment_length = measurement_number(
                                f"Garment Length ({edit_unit})",
                                profile.get(
                                    "garment_length",
                                    0
                                ),
                                f"edit_garment_length_{profile['id']}",
                            )

                        edit_head = measurement_number(
                            f"Head ({edit_unit})",
                            profile.get(
                                "head",
                                0
                            ),
                            f"edit_head_{profile['id']}",
                        )

                        st.divider()

                        # ====================================================
                        # EDIT LOWER BODY
                        # ====================================================

                        st.markdown(
                            "### 👖 Lower Body"
                        )

                        e1, e2, e3 = st.columns(3)

                        with e1:

                            edit_waist = measurement_number(
                                f"Waist ({edit_unit})",
                                profile.get(
                                    "waist",
                                    0
                                ),
                                f"edit_waist_{profile['id']}",
                            )

                            edit_hip = measurement_number(
                                f"Hip ({edit_unit})",
                                profile.get(
                                    "hip",
                                    0
                                ),
                                f"edit_hip_{profile['id']}",
                            )

                            edit_trouser_length = measurement_number(
                                f"Trouser Length ({edit_unit})",
                                profile.get(
                                    "trouser_length",
                                    0
                                ),
                                f"edit_trouser_length_{profile['id']}",
                            )

                        with e2:

                            edit_inseam = measurement_number(
                                f"Inseam ({edit_unit})",
                                profile.get(
                                    "inseam",
                                    0
                                ),
                                f"edit_inseam_{profile['id']}",
                            )

                            edit_thigh = measurement_number(
                                f"Thigh ({edit_unit})",
                                profile.get(
                                    "thigh",
                                    0
                                ),
                                f"edit_thigh_{profile['id']}",
                            )

                            edit_knee = measurement_number(
                                f"Knee ({edit_unit})",
                                profile.get(
                                    "knee",
                                    0
                                ),
                                f"edit_knee_{profile['id']}",
                            )

                        with e3:

                            edit_calf = measurement_number(
                                f"Calf ({edit_unit})",
                                profile.get(
                                    "calf",
                                    0
                                ),
                                f"edit_calf_{profile['id']}",
                            )

                            edit_ankle = measurement_number(
                                f"Ankle / Hem Opening ({edit_unit})",
                                profile.get(
                                    "ankle",
                                    0
                                ),
                                f"edit_ankle_{profile['id']}",
                            )

                        st.divider()

                        # ====================================================
                        # EDIT PHOTOS
                        # ====================================================

                        st.markdown(
                            "### 📸 Replace Client Photos"
                        )

                        new_client_photos = st.file_uploader(
                            "Upload new client photos "
                            "(leave empty to keep existing photos)",
                            type=[
                                "jpg",
                                "jpeg",
                                "png",
                                "webp",
                            ],
                            accept_multiple_files=True,
                            key=(
                                f"edit_client_photos_"
                                f"{profile['id']}"
                            ),
                        )

                        st.markdown(
                            "### 🧵 Replace Fabric Photos"
                        )

                        new_fabric_photos = st.file_uploader(
                            "Upload new fabric photos "
                            "(leave empty to keep existing photos)",
                            type=[
                                "jpg",
                                "jpeg",
                                "png",
                                "webp",
                            ],
                            accept_multiple_files=True,
                            key=(
                                f"edit_fabric_photos_"
                                f"{profile['id']}"
                            ),
                        )

                        st.markdown(
                            "### 📝 Production Notes"
                        )

                        edit_notes = st.text_area(
                            "Notes",
                            value=profile.get(
                                "notes",
                                ""
                            ),
                            key=(
                                f"edit_notes_"
                                f"{profile['id']}"
                            ),
                        )

                        st.divider()

                        # ====================================================
                        # SAVE EDITS
                        # ====================================================

                        if st.button(
                            "💾 Save Changes",
                            type="primary",
                            use_container_width=True,
                            key=(
                                f"save_edit_"
                                f"{profile['id']}"
                            ),
                        ):

                            if not edit_client_name.strip():

                                st.error(
                                    "Please enter the client's name."
                                )

                            else:

                                updated_profile = {

                                    "client_name":
                                        edit_client_name.strip(),

                                    "category":
                                        edit_category,

                                    "unit":
                                        edit_unit,

                                    "height":
                                        edit_height,

                                    "bust":
                                        edit_bust,

                                    "shoulder":
                                        edit_shoulder,

                                    "sleeve":
                                        profile.get(
                                            "sleeve",
                                            0
                                        ),

                                    "long_arm":
                                        edit_long_arm,

                                    "short_arm":
                                        edit_short_arm,

                                    "neck":
                                        edit_neck,

                                    "armhole":
                                        edit_armhole,

                                    "armhole_type":
                                        edit_armhole_type,

                                    "garment_length":
                                        edit_garment_length,

                                    "head":
                                        edit_head,

                                    "waist":
                                        edit_waist,

                                    "hip":
                                        edit_hip,

                                    "trouser_length":
                                        edit_trouser_length,

                                    "inseam":
                                        edit_inseam,

                                    "thigh":
                                        edit_thigh,

                                    "knee":
                                        edit_knee,

                                    "calf":
                                        edit_calf,

                                    "ankle":
                                        edit_ankle,

                                    "client_photos":
                                        (
                                            [
                                                photo.getvalue()
                                                for photo in new_client_photos
                                            ]
                                            if new_client_photos
                                            else profile.get(
                                                "client_photos",
                                                []
                                            )
                                        ),

                                    "fabric_photos":
                                        (
                                            [
                                                photo.getvalue()
                                                for photo in new_fabric_photos
                                            ]
                                            if new_fabric_photos
                                            else profile.get(
                                                "fabric_photos",
                                                []
                                            )
                                        ),

                                    "notes":
                                        edit_notes.strip(),
                                }

                                success, message = (
                                    update_measurement_profile(
                                        profile["id"],
                                        updated_profile
                                    )
                                )

                                if success:

                                    st.success(
                                        "✅ "
                                        "Measurement profile "
                                        "updated and saved successfully."
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        f"❌ {message}"
                                    )

                    st.divider()

                    # ====================================================
                    # DELETE
                    # ====================================================

                    if st.button(
                        "🗑 Delete Measurement Profile",
                        key=(
                            f"delete_measurement_"
                            f"{profile['id']}"
                        ),
                        use_container_width=True,
                    ):

                        success, message = (
                            delete_measurement_profile(
                                profile["id"]
                            )
                        )

                        if success:

                            st.success(
                                message
                            )

                            st.rerun()

                        else:

                            st.error(
                                message
                            )

    # ========================================================
    # CREATE NEW PROFILE
    # ========================================================

    with create_tab:

        st.subheader(
            "➕ Create Measurement Profile"
        )

        client_name = st.text_input(
            "Client Name",
            placeholder="e.g. Jane Doe",
            key="measurement_client_name",
        )

        category = st.selectbox(
            "Garment Category",
            [
                "Women's Wear",
                "Men's Wear",
                "Children's Wear",
                "Bridal",
                "Traditional Wear",
                "Sportswear",
                "Casual Wear",
                "Corporate Wear",
                "Other",
            ],
            key="measurement_category",
        )

        unit = st.radio(
            "Measurement Unit",
            [
                "in",
                "cm"
            ],
            horizontal=True,
            key="measurement_unit",
        )

        st.divider()

        # ====================================================
        # UPPER BODY
        # ====================================================

        st.markdown(
            "### 👕 Upper Body"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            height = measurement_number(
                f"Height ({unit})",
                key="measurement_height",
            )

            bust = measurement_number(
                f"Bust / Chest ({unit})",
                key="measurement_bust",
            )

            shoulder = measurement_number(
                f"Shoulder ({unit})",
                key="measurement_shoulder",
            )

        with c2:

            long_arm = measurement_number(
                f"Long Arm ({unit})",
                key="measurement_long_arm",
            )

            short_arm = measurement_number(
                f"Short Arm ({unit})",
                key="measurement_short_arm",
            )

            neck = measurement_number(
                f"Neck ({unit})",
                key="measurement_neck",
            )

        with c3:

            armhole = measurement_number(
                f"Armhole ({unit})",
                key="measurement_armhole",
            )

            armhole_type = st.selectbox(
                "Armhole Type",
                [
                    "Standard",
                    "Long",
                    "Short",
                ],
                key="measurement_armhole_type",
            )

            garment_length = measurement_number(
                f"Garment Length ({unit})",
                key="measurement_garment_length",
            )

        head = measurement_number(
            f"Head ({unit})",
            key="measurement_head",
        )

        st.divider()

        # ====================================================
        # LOWER BODY
        # ====================================================

        st.markdown(
            "### 👖 Lower Body"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            waist = measurement_number(
                f"Waist ({unit})",
                key="measurement_waist",
            )

            hip = measurement_number(
                f"Hip ({unit})",
                key="measurement_hip",
            )

            trouser_length = measurement_number(
                f"Trouser Length ({unit})",
                key="measurement_trouser_length",
            )

        with c2:

            inseam = measurement_number(
                f"Inseam ({unit})",
                key="measurement_inseam",
            )

            thigh = measurement_number(
                f"Thigh ({unit})",
                key="measurement_thigh",
            )

            knee = measurement_number(
                f"Knee ({unit})",
                key="measurement_knee",
            )

        with c3:

            calf = measurement_number(
                f"Calf ({unit})",
                key="measurement_calf",
            )

            ankle = measurement_number(
                f"Ankle / Hem Opening ({unit})",
                key="measurement_ankle",
            )

        st.divider()

        # ====================================================
        # CLIENT PHOTOS
        # ====================================================

        st.markdown(
            "### 📸 Client Photos"
        )

        client_photos = st.file_uploader(
            "Upload Client Photos",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp",
            ],
            accept_multiple_files=True,
            key="measurement_client_photos",
        )

        # ====================================================
        # FABRIC PHOTOS
        # ====================================================

        st.markdown(
            "### 🧵 Fabric Photos"
        )

        fabric_photos = st.file_uploader(
            "Upload Fabric Photos",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp",
            ],
            accept_multiple_files=True,
            key="measurement_fabric_photos",
        )

        # ====================================================
        # NOTES
        # ====================================================

        st.markdown(
            "### 📝 Production Notes"
        )

        notes = st.text_area(
            "Notes",
            placeholder=(
                "Fitting notes, body adjustments, "
                "special requirements..."
            ),
            key="measurement_notes",
        )

        st.divider()

        # ====================================================
        # SAVE NEW PROFILE
        # ====================================================

        if st.button(
            "💾 Save Measurement Profile",
            type="primary",
            use_container_width=True,
        ):

            if not client_name.strip():

                st.error(
                    "Please enter the client's name."
                )

            else:

                profile = {

                    "client_name":
                        client_name.strip(),

                    "category":
                        category,

                    "unit":
                        unit,

                    "height":
                        height,

                    "bust":
                        bust,

                    "shoulder":
                        shoulder,

                    "sleeve":
                        0,

                    "long_arm":
                        long_arm,

                    "short_arm":
                        short_arm,

                    "neck":
                        neck,

                    "armhole":
                        armhole,

                    "armhole_type":
                        armhole_type,

                    "garment_length":
                        garment_length,

                    "head":
                        head,

                    "waist":
                        waist,

                    "hip":
                        hip,

                    "trouser_length":
                        trouser_length,

                    "inseam":
                        inseam,

                    "thigh":
                        thigh,

                    "knee":
                        knee,

                    "calf":
                        calf,

                    "ankle":
                        ankle,

                    "client_photos":
                        [
                            photo.getvalue()
                            for photo in (
                                client_photos or []
                            )
                        ],

                    "fabric_photos":
                        [
                            photo.getvalue()
                            for photo in (
                                fabric_photos or []
                            )
                        ],

                    "notes":
                        notes.strip(),
                }

                success, result = (
                    save_measurement_profile(
                        profile
                    )
                )

                if success:

                    st.success(
                        "✅ Measurement profile "
                        "saved successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        f"❌ {result}"
                    )