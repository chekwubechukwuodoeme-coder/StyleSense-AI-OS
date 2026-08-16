import io
from pathlib import Path

import streamlit as st
from PIL import Image


# ============================================================
# IMAGE CONVERSION
# ============================================================

def image_to_bytes(image):
    """
    Convert a generated image into PNG bytes.
    """

    if image is None:
        return None

    # Already bytes
    if isinstance(image, bytes):

        return image

    # PIL Image
    if isinstance(image, Image.Image):

        buffer = io.BytesIO()

        image.convert("RGB").save(
            buffer,
            format="PNG"
        )

        buffer.seek(0)

        return buffer.getvalue()

    # File path
    if isinstance(image, (str, Path)):

        path = Path(image)

        if path.exists():

            return path.read_bytes()

    return None


# ============================================================
# DESIGN LIBRARY
# ============================================================

def render_design_library():

    st.title("📚 Design Library")

    st.caption(
        "Your personal collection of AI-generated fashion designs."
    )

    st.divider()

    # ========================================================
    # SESSION STATE
    # ========================================================

    if "saved_designs" not in st.session_state:

        st.session_state.saved_designs = []

    # ========================================================
    # EMPTY LIBRARY
    # ========================================================

    if not st.session_state.saved_designs:

        st.info(
            """
            🎨 Your Design Library is empty.

            Go to **AI Design Studio** and generate your
            first fashion design.
            """
        )

        return

    # ========================================================
    # LIBRARY STATISTICS
    # ========================================================

    total_designs = len(
        st.session_state.saved_designs
    )

    images_count = sum(
        1
        for item in st.session_state.saved_designs
        if isinstance(item, dict)
        and item.get("image")
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🎨 Total Designs",
            total_designs
        )

    with col2:

        st.metric(
            "🖼️ Generated Images",
            images_count
        )

    with col3:

        categories = set()

        for item in st.session_state.saved_designs:

            if isinstance(item, dict):

                category = item.get("category")

                if category:

                    categories.add(category)

        st.metric(
            "👗 Categories",
            len(categories)
        )

    st.divider()

    # ========================================================
    # SEARCH
    # ========================================================

    search = st.text_input(
        "🔎 Search Designs",
        placeholder="Search by category, fabric, theme..."
    )

    # ========================================================
    # FILTER
    # ========================================================

    all_categories = ["All"]

    for item in st.session_state.saved_designs:

        if isinstance(item, dict):

            category = item.get("category")

            if category and category not in all_categories:

                all_categories.append(category)

    selected_category = st.selectbox(
        "👗 Filter by Category",
        all_categories
    )

    st.divider()

    # ========================================================
    # DISPLAY DESIGNS
    # ========================================================

    displayed_designs = []

    for original_index, item in enumerate(
        st.session_state.saved_designs
    ):

        # ----------------------------------------------------
        # OLD STRING FORMAT
        # ----------------------------------------------------

        if isinstance(item, str):

            displayed_designs.append(
                (
                    original_index,
                    item
                )
            )

            continue

        # ----------------------------------------------------
        # SEARCH FILTER
        # ----------------------------------------------------

        if search:

            search_text = " ".join([
                str(item.get("design", "")),
                str(item.get("category", "")),
                str(item.get("fabric", "")),
                str(item.get("occasion", "")),
                str(item.get("theme", "")),
                str(item.get("gender", "")),
                str(item.get("country", ""))
            ]).lower()

            if search.lower() not in search_text:

                continue

        # ----------------------------------------------------
        # CATEGORY FILTER
        # ----------------------------------------------------

        if selected_category != "All":

            if item.get("category") != selected_category:

                continue

        displayed_designs.append(
            (
                original_index,
                item
            )
        )

    # ========================================================
    # NO SEARCH RESULTS
    # ========================================================

    if not displayed_designs:

        st.warning(
            "No designs match your search."
        )

        return

    # ========================================================
    # NEWEST FIRST
    # ========================================================

    displayed_designs.reverse()

    # ========================================================
    # DESIGN CARDS
    # ========================================================

    for display_number, (
        original_index,
        item
    ) in enumerate(
        displayed_designs,
        start=1
    ):

        # ====================================================
        # OLD FORMAT
        # ====================================================

        if isinstance(item, str):

            with st.expander(
                f"🎨 Design {display_number}"
            ):

                st.markdown(item)

                st.download_button(
                    "📄 Download Design Concept",
                    data=item,
                    file_name=(
                        f"StyleSense_Design_"
                        f"{display_number}.txt"
                    ),
                    mime="text/plain",
                    use_container_width=True,
                    key=f"old_download_{original_index}"
                )

            continue

        # ====================================================
        # DESIGN INFORMATION
        # ====================================================

        category = item.get(
            "category",
            "Fashion Design"
        )

        fabric = item.get(
            "fabric",
            "Not specified"
        )

        occasion = item.get(
            "occasion",
            "Not specified"
        )

        theme = item.get(
            "theme",
            "Not specified"
        )

        gender = item.get(
            "gender",
            "Not specified"
        )

        country = item.get(
            "country",
            "Not specified"
        )

        created_at = item.get(
            "created_at",
            "Unknown"
        )

        image = item.get(
            "image"
        )

        design_text = item.get(
            "design",
            ""
        )

        # ====================================================
        # TITLE
        # ====================================================

        title = (
            f"🎨 {category} "
            f"— {theme}"
        )

        with st.expander(
            title,
            expanded=(display_number == 1)
        ):

            # =================================================
            # IMAGE + DETAILS
            # =================================================

            left, right = st.columns(
                [1.3, 1]
            )

            # -------------------------------------------------
            # IMAGE
            # -------------------------------------------------

            with left:

                if image:

                    st.image(
                        image,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No image available."
                    )

            # -------------------------------------------------
            # DETAILS
            # -------------------------------------------------

            with right:

                st.subheader(
                    "📋 Design Details"
                )

                st.write(
                    f"**Category:** {category}"
                )

                st.write(
                    f"**Fabric:** {fabric}"
                )

                st.write(
                    f"**Occasion:** {occasion}"
                )

                st.write(
                    f"**Theme:** {theme}"
                )

                st.write(
                    f"**Gender:** {gender}"
                )

                st.write(
                    f"**Country:** {country}"
                )

                st.write(
                    f"**Created:** {created_at}"
                )

                # ---------------------------------------------
                # COLORS
                # ---------------------------------------------

                colors = item.get(
                    "colors",
                    []
                )

                if colors:

                    st.write(
                        "**Colors:** "
                        + ", ".join(colors)
                    )

                # ---------------------------------------------
                # BUDGET
                # ---------------------------------------------

                budget = item.get(
                    "budget"
                )

                if budget:

                    st.write(
                        f"**Budget:** {budget}"
                    )

            st.divider()

            # =================================================
            # AI CONCEPT
            # =================================================

            st.subheader(
                "📝 AI Fashion Concept"
            )

            if design_text:

                st.markdown(
                    design_text
                )

            else:

                st.info(
                    "No design description available."
                )

            st.divider()

            # =================================================
            # DOWNLOADS
            # =================================================

            st.subheader(
                "📥 Downloads"
            )

            download_col1, download_col2 = st.columns(2)

            # -------------------------------------------------
            # IMAGE DOWNLOAD
            # -------------------------------------------------

            with download_col1:

                if image:

                    image_bytes = image_to_bytes(
                        image
                    )

                    if image_bytes:

                        st.download_button(
                            "📥 Download Image",
                            data=image_bytes,
                            file_name=(
                                f"StyleSense_"
                                f"{category.replace(' ', '_')}_"
                                f"{display_number}.png"
                            ),
                            mime="image/png",
                            use_container_width=True,
                            key=(
                                f"image_download_"
                                f"{original_index}"
                            )
                        )

            # -------------------------------------------------
            # TEXT DOWNLOAD
            # -------------------------------------------------

            with download_col2:

                if design_text:

                    st.download_button(
                        "📄 Download Concept",
                        data=design_text,
                        file_name=(
                            f"StyleSense_"
                            f"{category.replace(' ', '_')}_"
                            f"{display_number}.txt"
                        ),
                        mime="text/plain",
                        use_container_width=True,
                        key=(
                            f"concept_download_"
                            f"{original_index}"
                        )
                    )

            st.divider()

            # =================================================
            # DELETE
            # =================================================

            if st.button(
                "🗑️ Delete Design",
                key=f"delete_{original_index}",
                use_container_width=True
            ):

                del st.session_state.saved_designs[
                    original_index
                ]

                st.success(
                    "Design deleted."
                )

                st.rerun()