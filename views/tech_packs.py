import streamlit as st

from database.database import get_connection


# ============================================================
# TECH PACKS
# ============================================================


def get_user_id():

    return st.session_state.get("user_id")


# ============================================================
# DATABASE
# ============================================================

def ensure_tech_packs_table():

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tech_packs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id TEXT NOT NULL,

                design_name TEXT NOT NULL,

                category TEXT,

                description TEXT,

                fabric TEXT,

                colour TEXT,

                secondary_colour TEXT,

                trims TEXT,

                embroidery TEXT,

                construction TEXT,

                finishing TEXT,

                size_range TEXT,

                quantity INTEGER DEFAULT 1,

                production_type TEXT,

                quality_control TEXT,

                notes TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        conn.commit()

    except Exception:

        conn.rollback()

    finally:

        conn.close()


# ============================================================
# LOAD TECH PACKS
# ============================================================

def get_tech_packs():

    user_id = get_user_id()

    if not user_id:
        return []

    ensure_tech_packs_table()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                design_name,
                category,
                description,
                fabric,
                colour,
                secondary_colour,
                trims,
                embroidery,
                construction,
                finishing,
                size_range,
                quantity,
                production_type,
                quality_control,
                notes,
                created_at
            FROM tech_packs
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (str(user_id),)
        )

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    except Exception as e:

        st.error(
            f"Unable to load tech packs: {e}"
        )

        return []

    finally:

        conn.close()


# ============================================================
# CREATE TECH PACK
# ============================================================

def create_tech_pack(pack):

    user_id = get_user_id()

    if not user_id:
        return False, "No logged-in user found."

    ensure_tech_packs_table()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tech_packs (

                user_id,

                design_name,
                category,
                description,

                fabric,
                colour,
                secondary_colour,

                trims,
                embroidery,

                construction,
                finishing,

                size_range,
                quantity,
                production_type,

                quality_control,

                notes

            )
            VALUES (
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?,
                ?, ?,
                ?, ?, ?,
                ?,
                ?
            )
            """,
            (
                str(user_id),

                pack.get("design_name", ""),
                pack.get("category", ""),
                pack.get("description", ""),

                pack.get("fabric", ""),
                pack.get("colour", ""),
                pack.get("secondary_colour", ""),

                pack.get("trims", ""),
                pack.get("embroidery", ""),

                pack.get("construction", ""),
                pack.get("finishing", ""),

                pack.get("size_range", ""),
                pack.get("quantity", 1),
                pack.get("production_type", "Custom"),

                pack.get("quality_control", ""),

                pack.get("notes", "")
            )
        )

        conn.commit()

        return True, "Tech pack saved successfully."

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        conn.close()


# ============================================================
# DELETE TECH PACK
# ============================================================

def delete_tech_pack(pack_id):

    user_id = get_user_id()

    if not user_id:
        return False, "No logged-in user found."

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM tech_packs
            WHERE id = ?
            AND user_id = ?
            """,
            (
                pack_id,
                str(user_id)
            )
        )

        conn.commit()

        return True, "Tech pack deleted."

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        conn.close()


# ============================================================
# RENDER TECH PACKS
# ============================================================

def render_tech_packs():

    ensure_tech_packs_table()

    st.title("📋 Tech Packs")

    st.caption(
        "Create professional production documents from your "
        "fashion designs."
    )

    st.divider()

    packs_tab, create_tab = st.tabs(
        [
            "📋 My Tech Packs",
            "➕ Create Tech Pack",
        ]
    )

    # ========================================================
    # SAVED TECH PACKS
    # ========================================================

    with packs_tab:

        st.subheader(
            "📋 Saved Tech Packs"
        )

        tech_packs = get_tech_packs()

        if not tech_packs:

            st.info(
                "No tech packs created yet. "
                "Create your first production tech pack."
            )

        else:

            for pack in tech_packs:

                pack_id = pack["id"]

                with st.expander(
                    f"📋 {pack['design_name']}"
                ):

                    st.write(
                        f"**Category:** "
                        f"{pack.get('category', '')}"
                    )

                    st.write(
                        f"**Fabric:** "
                        f"{pack.get('fabric', '')}"
                    )

                    st.write(
                        f"**Primary Colour:** "
                        f"{pack.get('colour', '')}"
                    )

                    st.write(
                        f"**Secondary Colour:** "
                        f"{pack.get('secondary_colour', '') or 'None'}"
                    )

                    st.write(
                        f"**Size Range:** "
                        f"{pack.get('size_range', '') or 'Not specified'}"
                    )

                    st.write(
                        f"**Production Quantity:** "
                        f"{pack.get('quantity', 1)}"
                    )

                    st.write(
                        f"**Production Type:** "
                        f"{pack.get('production_type', '')}"
                    )

                    st.write(
                        f"**Trims:** "
                        f"{pack.get('trims', '') or 'None'}"
                    )

                    st.write(
                        f"**Embroidery:** "
                        f"{pack.get('embroidery', '') or 'None'}"
                    )

                    st.write(
                        f"**Construction:** "
                        f"{pack.get('construction', '') or 'Not specified'}"
                    )

                    st.write(
                        f"**Finishing:** "
                        f"{pack.get('finishing', '') or 'Not specified'}"
                    )

                    st.write(
                        f"**Quality Control:** "
                        f"{pack.get('quality_control', '') or 'Not specified'}"
                    )

                    st.write(
                        f"**Production Notes:** "
                        f"{pack.get('notes', '') or 'None'}"
                    )

                    if st.button(
                        "🗑 Delete Tech Pack",
                        key=f"delete_tech_pack_{pack_id}",
                        use_container_width=True,
                    ):

                        success, message = (
                            delete_tech_pack(
                                pack_id
                            )
                        )

                        if success:

                            st.success(message)

                            st.rerun()

                        else:

                            st.error(message)

    # ========================================================
    # CREATE TECH PACK
    # ========================================================

    with create_tab:

        st.subheader(
            "➕ Create Production Tech Pack"
        )

        st.caption(
            "Document the technical specifications of your garment."
        )

        # ====================================================
        # DESIGN
        # ====================================================

        st.markdown(
            "### 🎨 Design Information"
        )

        design_name = st.text_input(
            "Design Name",
            placeholder="e.g. Emerald Royal Evening Gown",
            key="tech_design_name",
        )

        category = st.selectbox(
            "Garment Category",
            [
                "Dress",
                "Gown",
                "Top",
                "Shirt",
                "Jacket",
                "Blazer",
                "Trousers",
                "Skirt",
                "Jumpsuit",
                "Traditional Wear",
                "Bridal Wear",
                "Other",
            ],
            key="tech_category",
        )

        design_description = st.text_area(
            "Design Description",
            placeholder=(
                "Describe the garment silhouette, style, "
                "structure and overall appearance..."
            ),
            key="tech_design_description",
        )

        # ====================================================
        # FABRIC
        # ====================================================

        st.markdown(
            "### 🧵 Fabric & Colour"
        )

        col1, col2 = st.columns(2)

        with col1:

            fabric = st.text_input(
                "Fabric",
                placeholder="e.g. Silk, Satin, Velvet",
                key="tech_fabric",
            )

        with col2:

            colour = st.text_input(
                "Primary Colour",
                placeholder="e.g. Emerald Green",
                key="tech_colour",
            )

        secondary_colour = st.text_input(
            "Secondary Colour",
            placeholder="Optional",
            key="tech_secondary_colour",
        )

        # ====================================================
        # TRIMS
        # ====================================================

        st.markdown(
            "### ✨ Trims & Details"
        )

        trims = st.text_area(
            "Trims / Embellishments",
            placeholder=(
                "Beads, embroidery, zippers, buttons, "
                "sequins, lace, crystals, etc."
            ),
            key="tech_trims",
        )

        embroidery = st.text_area(
            "Embroidery Details",
            placeholder=(
                "Describe embroidery placement, pattern, "
                "thread colour and technique..."
            ),
            key="tech_embroidery",
        )

        # ====================================================
        # CONSTRUCTION
        # ====================================================

        st.markdown(
            "### 🪡 Construction"
        )

        construction = st.text_area(
            "Construction Instructions",
            placeholder=(
                "Describe seams, lining, closures, "
                "panels, structure and sewing requirements..."
            ),
            key="tech_construction",
        )

        finishing = st.text_area(
            "Finishing Instructions",
            placeholder=(
                "Pressing, hemming, edge finishing, "
                "quality control and final finishing..."
            ),
            key="tech_finishing",
        )

        # ====================================================
        # PRODUCTION
        # ====================================================

        st.markdown(
            "### 📐 Sizing & Production"
        )

        col3, col4, col5 = st.columns(3)

        with col3:

            size_range = st.text_input(
                "Size Range",
                placeholder="e.g. S - XL",
                key="tech_size_range",
            )

        with col4:

            quantity = st.number_input(
                "Production Quantity",
                min_value=1,
                value=1,
                step=1,
                key="tech_quantity",
            )

        with col5:

            production_type = st.selectbox(
                "Production Type",
                [
                    "Custom",
                    "Small Batch",
                    "Made to Order",
                    "Ready to Wear",
                    "Mass Production",
                ],
                key="tech_production_type",
            )

        # ====================================================
        # QUALITY
        # ====================================================

        st.markdown(
            "### 🔍 Quality Control"
        )

        quality_control = st.text_area(
            "Quality Control Requirements",
            placeholder=(
                "Specify measurements, stitching quality, "
                "fabric inspection, finishing and fitting checks..."
            ),
            key="tech_quality_control",
        )

        # ====================================================
        # NOTES
        # ====================================================

        st.markdown(
            "### 📝 Production Notes"
        )

        notes = st.text_area(
            "Additional Notes",
            placeholder=(
                "Any additional information for the pattern "
                "maker, cutter or sewing team..."
            ),
            key="tech_notes",
        )

        st.divider()

        # ====================================================
        # SAVE
        # ====================================================

        if st.button(
            "💾 Save Tech Pack",
            type="primary",
            use_container_width=True,
        ):

            if not design_name.strip():

                st.error(
                    "Please enter a design name."
                )

            elif not fabric.strip():

                st.error(
                    "Please enter the fabric."
                )

            else:

                tech_pack = {

                    "design_name":
                        design_name.strip(),

                    "category":
                        category,

                    "description":
                        design_description.strip(),

                    "fabric":
                        fabric.strip(),

                    "colour":
                        colour.strip(),

                    "secondary_colour":
                        secondary_colour.strip(),

                    "trims":
                        trims.strip(),

                    "embroidery":
                        embroidery.strip(),

                    "construction":
                        construction.strip(),

                    "finishing":
                        finishing.strip(),

                    "size_range":
                        size_range.strip(),

                    "quantity":
                        quantity,

                    "production_type":
                        production_type,

                    "quality_control":
                        quality_control.strip(),

                    "notes":
                        notes.strip(),
                }

                success, message = (
                    create_tech_pack(
                        tech_pack
                    )
                )

                if success:

                    st.success(
                        f"✅ {message}"
                    )

                    st.rerun()

                else:

                    st.error(
                        f"❌ {message}"
                    )