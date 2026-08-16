import io
from pathlib import Path

import streamlit as st
from PIL import Image


# ============================================================
# IMAGE CONVERSION
# ============================================================

def image_to_bytes(image):

    if image is None:
        return None

    # Bytes
    if isinstance(image, bytes):
        return image

    # PIL
    if isinstance(image, Image.Image):

        buffer = io.BytesIO()

        image.convert("RGB").save(
            buffer,
            format="PNG"
        )

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

    st.title(
        "📚 Design Library"
    )

    st.caption(
        "Your personal collection of StyleSense AI fashion designs."
    )

    st.divider()

    # ========================================================
    # SESSION STATE
    # ========================================================

    if "saved_designs" not in st.session_state:

        st.session_state.saved_designs = []

    designs = st.session_state.saved_designs

    # ========================================================
    # EMPTY
    # ========================================================

    if not designs:

        st.info(
            """
🎨 Your Design Library is empty.

Go to **✨ AI Design Studio** and generate
your first fashion design.
"""
        )

        return

    # ========================================================
    # STATISTICS
    # ========================================================

    total_designs = len(designs)

    images_count = sum(
        1
        for item in designs
        if isinstance(item, dict)
        and item.get("image") is not None
    )

    modes = set()

    for item in designs:

        if isinstance(item, dict):

            mode = item.get(
                "mode"
            )

            if mode:
                modes.add(mode)

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

        st.metric(
            "⚙️ Design Modes",
            len(modes)
        )

    st.divider()

    # ========================================================
    # SEARCH
    # ========================================================

    search = st.text_input(
        "🔎 Search Designs",
        placeholder=(
            "Search by fabric, category, theme, "
            "occasion or design type..."
        )
    )

    # ========================================================
    # MODE FILTER
    # ========================================================

    mode_options = [
        "All"
    ]

    for item in designs:

        if isinstance(item, dict):

            mode = item.get(
                "mode"
            )

            if mode and mode not in mode_options:

                mode_options.append(
                    mode
                )

    selected_mode = st.selectbox(
        "⚙️ Filter by Design Type",
        mode_options
    )

    st.divider()

    # ========================================================
    # FILTER DESIGNS
    # ========================================================

    displayed = []

    for original_index, item in enumerate(designs):

        if isinstance(item, str):

            if search and search.lower() not in item.lower():

                continue

            displayed.append(
                (
                    original_index,
                    item
                )
            )

            continue

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        if search:

            search_text = " ".join(
                [
                    str(item.get("design", "")),
                    str(item.get("category", "")),
                    str(item.get("fabric", "")),
                    str(item.get("occasion", "")),
                    str(item.get("theme", "")),
                    str(item.get("gender", "")),
                    str(item.get("country", "")),
                    str(item.get("mode", "")),
                    str(item.get("style", "")),
                    str(item.get("culture", "")),
                    str(item.get("market", "")),
                ]
            ).lower()

            if search.lower() not in search_text:

                continue

        # ----------------------------------------------------
        # MODE
        # ----------------------------------------------------

        if selected_mode != "All":

            if item.get("mode") != selected_mode:

                continue

        displayed.append(
            (
                original_index,
                item
            )
        )

    # ========================================================
    # EMPTY FILTER
    # ========================================================

    if not displayed:

        st.warning(
            "No designs match your search."
        )

        return

    # ========================================================
    # NEWEST FIRST
    # ========================================================

    displayed.reverse()

    # ========================================================
    # DESIGN CARDS
    # ========================================================

    for display_number, (
        original_index,
        item
    ) in enumerate(
        displayed,
        start=1
    ):

        # ====================================================
        # OLD STRING
        # ====================================================

        if isinstance(item, str):

            with st.expander(
                f"🎨 Design {display_number}"
            ):

                st.markdown(item)

                st.download_button(
                    "📄 Download Concept",
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
        # DATA
        # ====================================================

        design_text = item.get(
            "design",
            ""
        )

        image = item.get(
            "image"
        )

        mode = item.get(
            "mode",
            "Fashion Design"
        )

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

        created_at = item.get(
            "created_at",
            "Unknown"
        )

        title = (
            f"🎨 {category} • {mode}"
        )

        with st.expander(
            title,
            expanded=(display_number == 1)
        ):

            # =================================================
            # IMAGE
            # =================================================

            if image:

                st.image(
                    image,
                    use_container_width=True
                )

            else:

                st.info(
                    "No generated image available."
                )

            # =================================================
            # DETAILS
            # =================================================

            st.subheader(
                "📋 Design Information"
            )

            st.write(
                f"**Design Type:** {mode}"
            )

            st.write(
                f"**Category:** {category}"
            )

            if fabric != "Not specified":

                st.write(
                    f"**Fabric:** {fabric}"
                )

            if occasion != "Not specified":

                st.write(
                    f"**Occasion:** {occasion}"
                )

            if theme != "Not specified":

                st.write(
                    f"**Theme:** {theme}"
                )

            st.write(
                f"**Created:** {created_at}"
            )

            # =================================================
            # ADVANCED DETAILS
            # =================================================

            if mode == "Advanced Prompt-to-Design":

                st.divider()

                st.subheader(
                    "⚙️ AI Design Settings"
                )

                st.write(
                    f"**Style:** "
                    f"{item.get('style', 'AI Choice')}"
                )

                st.write(
                    f"**Fabric:** "
                    f"{item.get('fabric', 'AI Choice')}"
                )

                st.write(
                    f"**Colour:** "
                    f"{item.get('colour', 'AI Choice')}"
                )

                st.write(
                    f"**Occasion:** "
                    f"{item.get('occasion', 'AI Choice')}"
                )

                st.write(
                    f"**Market:** "
                    f"{item.get('market', 'AI Choice')}"
                )

                st.write(
                    f"**Culture:** "
                    f"{item.get('culture', 'AI Choice')}"
                )

            # =================================================
            # REFERENCE DESIGN DETAILS
            # =================================================

            if mode == "Reference Image → Design":

                st.divider()

                st.subheader(
                    "🖼️ Reference Information"
                )

                st.write(
                    f"**Reference Source:** "
                    f"{item.get('reference_source', 'Image')}"
                )

                st.write(
                    f"**Silhouette Preserved:** "
                    f"{'Yes' if item.get('preserve_silhouette') else 'No'}"
                )

                st.write(
                    f"**Fabric Changed:** "
                    f"{'Yes' if item.get('change_fabric') else 'No'}"
                )

                st.write(
                    f"**Colour Changed:** "
                    f"{'Yes' if item.get('change_colour') else 'No'}"
                )

                st.write(
                    f"**Style Changed:** "
                    f"{'Yes' if item.get('change_style') else 'No'}"
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
            # IMAGE
            # -------------------------------------------------

            with download_col1:

                if image:

                    image_bytes = image_to_bytes(
                        image
                    )

                    if image_bytes:

                        st.download_button(
                            "📥 Download Design Image",
                            data=image_bytes,
                            file_name=(
                                f"StyleSense_"
                                f"Design_{display_number}.png"
                            ),
                            mime="image/png",
                            use_container_width=True,
                            key=(
                                f"library_image_"
                                f"{original_index}"
                            )
                        )

            # -------------------------------------------------
            # CONCEPT
            # -------------------------------------------------

            with download_col2:

                if design_text:

                    st.download_button(
                        "📄 Download Concept",
                        data=design_text,
                        file_name=(
                            f"StyleSense_"
                            f"Concept_{display_number}.txt"
                        ),
                        mime="text/plain",
                        use_container_width=True,
                        key=(
                            f"library_concept_"
                            f"{original_index}"
                        )
                    )

            st.divider()

            # =================================================
            # DELETE
            # =================================================

            if st.button(
                "🗑️ Delete Design",
                key=f"delete_library_{original_index}",
                use_container_width=True
            ):

                del st.session_state.saved_designs[
                    original_index
                ]

                st.success(
                    "Design deleted."
                )

                st.rerun()