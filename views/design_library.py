import streamlit as st

from database.database import (
    get_all_designs,
    delete_design,
    clear_all_designs,
)


# ============================================================
# PAGE STYLE
# ============================================================

def inject_design_library_css():

    st.markdown(
        """
        <style>

        /* ==================================================
           STYLESENSE AI OS — DESIGN LIBRARY
           PREMIUM DARK FASHION / AI THEME
        ================================================== */

        /* ==================================================
           GLOBAL PAGE
        ================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 75% 8%,
                    rgba(139, 92, 246, 0.10),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 15% 40%,
                    rgba(34, 211, 238, 0.035),
                    transparent 25%
                ),
                #050914;
        }

        .main .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }


        /* ==================================================
           HERO
        ================================================== */

        .library-hero {
            position: relative;
            padding: 24px 0 30px 0;
        }

        .library-eyebrow {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            color: #A855F7;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .library-title {
            font-size: clamp(2.2rem, 4vw, 3.4rem);
            font-weight: 800;
            letter-spacing: -0.045em;
            line-height: 1.05;

            background:
                linear-gradient(
                    90deg,
                    #F8FAFC 0%,
                    #E9D5FF 45%,
                    #C084FC 100%
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .library-subtitle {
            color: #94A3B8;
            font-size: 0.98rem;
            line-height: 1.6;
            margin-top: 12px;
            max-width: 700px;
        }


        /* ==================================================
           STATISTICS
        ================================================== */

        div[data-testid="stMetric"] {
            background:
                linear-gradient(
                    145deg,
                    rgba(16, 24, 39, 0.92),
                    rgba(11, 18, 32, 0.86)
                );

            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 16px;

            padding: 18px 20px;

            min-height: 110px;

            transition:
                transform 180ms ease,
                border-color 180ms ease,
                box-shadow 180ms ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);

            border-color:
                rgba(139, 92, 246, 0.38);

            box-shadow:
                0 10px 35px
                rgba(0, 0, 0, 0.22),

                0 0 25px
                rgba(139, 92, 246, 0.08);
        }

        div[data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
            font-size: 0.78rem !important;
        }

        div[data-testid="stMetricValue"] {
            color: #F8FAFC !important;
            font-size: 1.8rem !important;
            font-weight: 800 !important;
        }


        /* ==================================================
           SECTION HEADERS
        ================================================== */

        .section-title {
            font-size: 1.3rem;
            font-weight: 750;
            letter-spacing: -0.02em;
            color: #F8FAFC;
            margin-bottom: 3px;
        }

        .section-subtitle {
            color: #64748B;
            font-size: 0.82rem;
            margin-bottom: 14px;
        }


        /* ==================================================
           FEATURED CREATION
        ================================================== */

        .featured-label {
            font-size: 0.68rem;
            font-weight: 750;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: #A855F7;
        }

        .featured-title {
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -0.035em;
            color: #F8FAFC;
            margin-top: 5px;
            margin-bottom: 8px;
        }

        .featured-description {
            color: #94A3B8;
            font-size: 0.9rem;
            line-height: 1.65;
        }


        /* ==================================================
           SEARCH
        ================================================== */

        div[data-testid="stTextInput"] input {
            background: #0B1220 !important;

            color: #F8FAFC !important;

            border:
                1px solid
                rgba(148, 163, 184, 0.14) !important;

            border-radius: 12px !important;

            min-height: 44px !important;

            transition:
                border-color 180ms ease,
                box-shadow 180ms ease;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color:
                rgba(139, 92, 246, 0.65) !important;

            box-shadow:
                0 0 0 1px
                rgba(139, 92, 246, 0.18),

                0 0 24px
                rgba(139, 92, 246, 0.08);
        }


        /* ==================================================
           SELECTBOX
        ================================================== */

        div[data-baseweb="select"] > div {
            background: #0B1220 !important;

            border:
                1px solid
                rgba(148, 163, 184, 0.14) !important;

            border-radius: 12px !important;

            color: #F8FAFC !important;
        }


        /* ==================================================
           DESIGN CARDS
        ================================================== */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background:
                linear-gradient(
                    145deg,
                    rgba(16, 24, 39, 0.96),
                    rgba(11, 18, 32, 0.94)
                );

            border:
                1px solid
                rgba(148, 163, 184, 0.12);

            border-radius: 16px;

            transition:
                transform 180ms ease,
                border-color 180ms ease,
                box-shadow 180ms ease;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-4px);

            border-color:
                rgba(139, 92, 246, 0.32);

            box-shadow:
                0 15px 45px
                rgba(0, 0, 0, 0.28),

                0 0 30px
                rgba(139, 92, 246, 0.06);
        }


        /* ==================================================
           DESIGN CARD IMAGE
        ================================================== */

        div[data-testid="stVerticalBlockBorderWrapper"]
        img {
            border-radius: 12px;

            transition:
                transform 250ms ease,
                filter 250ms ease;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:hover
        img {
            filter: brightness(1.04);
        }


        /* ==================================================
           DESIGN CARD TEXT
        ================================================== */

        .design-card-title {
            color: #F8FAFC;
            font-size: 1rem;
            font-weight: 750;
            letter-spacing: -0.015em;
            margin-top: 7px;
            margin-bottom: 3px;
        }

        .design-card-mode {
            color: #A855F7;
            font-size: 0.72rem;
            font-weight: 650;
        }

        .design-card-description {
            color: #94A3B8;
            font-size: 0.78rem;
            line-height: 1.5;
            margin-top: 7px;
        }


        /* ==================================================
           METADATA PILLS
        ================================================== */

        .metadata-pill {
            display: inline-block;

            border:
                1px solid
                rgba(139, 92, 246, 0.14);

            border-radius: 999px;

            padding: 4px 9px;

            margin:
                4px 4px 0 0;

            background:
                rgba(139, 92, 246, 0.07);

            color: #C4B5FD;

            font-size: 0.68rem;
        }


        /* ==================================================
           BUTTONS
        ================================================== */

        .stButton > button {
            border-radius: 10px !important;

            border:
                1px solid
                rgba(148, 163, 184, 0.14) !important;

            background:
                rgba(11, 18, 32, 0.9) !important;

            color: #E2E8F0 !important;

            transition:
                transform 160ms ease,
                border-color 160ms ease,
                box-shadow 160ms ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);

            border-color:
                rgba(139, 92, 246, 0.45) !important;

            box-shadow:
                0 0 20px
                rgba(139, 92, 246, 0.10);
        }

        .stButton > button[kind="primary"] {
            background:
                linear-gradient(
                    135deg,
                    #7C3AED,
                    #A855F7
                ) !important;

            border:
                1px solid
                rgba(192, 132, 252, 0.35) !important;

            color: white !important;

            box-shadow:
                0 6px 24px
                rgba(139, 92, 246, 0.20);
        }

        .stButton > button[kind="primary"]:hover {
            box-shadow:
                0 8px 30px
                rgba(139, 92, 246, 0.32);
        }


        /* ==================================================
           DOWNLOAD BUTTON
        ================================================== */

        .stDownloadButton > button {
            border-radius: 10px !important;

            background:
                rgba(139, 92, 246, 0.10) !important;

            border:
                1px solid
                rgba(139, 92, 246, 0.20) !important;

            color: #DDD6FE !important;
        }

        .stDownloadButton > button:hover {
            background:
                rgba(139, 92, 246, 0.17) !important;

            border-color:
                rgba(139, 92, 246, 0.40) !important;
        }


        /* ==================================================
           DIVIDERS
        ================================================== */

        hr {
            border-color:
                rgba(148, 163, 184, 0.09) !important;
        }


        /* ==================================================
           EMPTY STATE
        ================================================== */

        .empty-state {
            text-align: center;

            padding: 70px 25px;

            border:
                1px dashed
                rgba(148, 163, 184, 0.18);

            border-radius: 18px;

            background:
                rgba(11, 18, 32, 0.45);

            margin-top: 20px;
        }

        .empty-icon {
            font-size: 2.8rem;
            margin-bottom: 12px;
        }

        .empty-title {
            color: #F8FAFC;
            font-size: 1.35rem;
            font-weight: 750;
        }

        .empty-text {
            color: #64748B;
            max-width: 520px;
            margin: 8px auto 20px auto;
            line-height: 1.6;
        }


        /* ==================================================
           CAPTIONS
        ================================================== */

        .stCaption,
        [data-testid="stCaptionContainer"] {
            color: #64748B !important;
        }


        /* ==================================================
           EXPANDER
        ================================================== */

        div[data-testid="stExpander"] {
            background:
                rgba(11, 18, 32, 0.72);

            border:
                1px solid
                rgba(148, 163, 184, 0.10);

            border-radius: 12px;
        }


        /* ==================================================
           SCROLLBAR
        ================================================== */

        ::-webkit-scrollbar {
            width: 7px;
            height: 7px;
        }

        ::-webkit-scrollbar-track {
            background: #050914;
        }

        ::-webkit-scrollbar-thumb {
            background: #1E293B;
            border-radius: 999px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #7C3AED;
        }


        /* ==================================================
           MOBILE
        ================================================== */

        @media (max-width: 768px) {

            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .library-title {
                font-size: 2.1rem;
            }

            div[data-testid="stMetric"] {
                min-height: 95px;
                padding: 14px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# IMAGE HELPER
# ============================================================

def get_image_bytes(image_data):

    if not image_data:
        return None

    try:

        if isinstance(image_data, bytes):
            return image_data

        if isinstance(image_data, bytearray):
            return bytes(image_data)

        return bytes(image_data)

    except Exception:
        return None


# ============================================================
# NAVIGATION
# ============================================================

def go_to_design_studio():

    st.session_state.main_navigation = "AI Design Studio"

    st.rerun()


# ============================================================
# DESIGN HELPERS
# ============================================================

def get_design_title(design):

    return (
        design.get("category")
        or design.get("theme")
        or design.get("style")
        or design.get("mode")
        or "AI Fashion Design"
    )


def get_design_mode(design):

    return (
        design.get("mode")
        or "AI Design"
    )


def get_design_description(design):

    description = (
        design.get("design")
        or "AI-generated fashion concept."
    )

    return str(description)


def get_design_metadata(design):

    metadata = []

    if design.get("fabric"):
        metadata.append(
            f"🧵 {design['fabric']}"
        )

    if design.get("occasion"):
        metadata.append(
            f"🎯 {design['occasion']}"
        )

    if design.get("market"):
        metadata.append(
            f"🛍️ {design['market']}"
        )

    if design.get("theme"):
        metadata.append(
            f"✨ {design['theme']}"
        )

    if design.get("culture"):
        metadata.append(
            f"🌍 {design['culture']}"
        )

    if design.get("style"):
        metadata.append(
            f"🎨 {design['style']}"
        )

    return metadata


# ============================================================
# DESIGN DETAILS
# ============================================================

def render_design_details(design):

    design_id = design.get("id")

    title = get_design_title(design)

    mode = get_design_mode(design)

    description = get_design_description(design)

    image_bytes = get_image_bytes(
        design.get("image_data")
    )

    st.caption(
        "STYLESENSE AI OS • AI CREATIVE WORKSPACE"
    )

    st.title(title)

    st.caption(
        f"🤖 {mode}"
    )

    if image_bytes:

        st.image(
            image_bytes,
            use_container_width=True
        )

    st.subheader(
        "AI Concept"
    )

    st.write(
        description
    )

    st.subheader(
        "Design Information"
    )

    info1, info2 = st.columns(2)

    with info1:

        if design.get("category"):
            st.write(
                f"**Category:** {design['category']}"
            )

        if design.get("fabric"):
            st.write(
                f"**Fabric:** {design['fabric']}"
            )

        if design.get("colour"):
            st.write(
                f"**Colour:** {design['colour']}"
            )

        if design.get("occasion"):
            st.write(
                f"**Occasion:** {design['occasion']}"
            )

        if design.get("market"):
            st.write(
                f"**Market:** {design['market']}"
            )

    with info2:

        if design.get("style"):
            st.write(
                f"**Style:** {design['style']}"
            )

        if design.get("theme"):
            st.write(
                f"**Theme:** {design['theme']}"
            )

        if design.get("culture"):
            st.write(
                f"**Culture:** {design['culture']}"
            )

        if design.get("gender"):
            st.write(
                f"**Gender:** {design['gender']}"
            )

        if design.get("complexity"):
            st.write(
                f"**Complexity:** {design['complexity']}"
            )

    st.divider()

    action1, action2, action3 = st.columns(3)

    with action1:

        if image_bytes:

            st.download_button(
                "⬇ Download",
                data=image_bytes,
                file_name=(
                    f"StyleSense_Design_"
                    f"{design_id}.png"
                ),
                mime="image/png",
                use_container_width=True,
                key=f"detail_download_{design_id}"
            )

    with action2:

        if st.button(
            "✨ Reuse Design",
            use_container_width=True,
            key=f"reuse_design_{design_id}"
        ):

            st.session_state[
                "selected_design"
            ] = design

            go_to_design_studio()

    with action3:

        if st.button(
            "🗑 Delete",
            use_container_width=True,
            key=f"detail_delete_{design_id}"
        ):

            if delete_design(design_id):

                st.toast(
                    "Design deleted."
                )

                st.session_state.pop(
                    "design_library_selected",
                    None
                )

                st.rerun()


# ============================================================
# DESIGN CARD
# ============================================================

def render_design_card(
    design,
    index
):

    design_id = design.get("id")

    title = get_design_title(design)

    mode = get_design_mode(design)

    description = get_design_description(design)

    image_bytes = get_image_bytes(
        design.get("image_data")
    )

    metadata = get_design_metadata(
        design
    )

    created_at = (
        design.get("created_at")
        or "Recently created"
    )

    with st.container(
        border=True
    ):

        # IMAGE
        if image_bytes:

            st.image(
                image_bytes,
                use_container_width=True
            )

        else:

            st.info(
                "No preview image available."
            )

        # TITLE
        st.markdown(
            f'<div class="design-card-title">{title}</div>',
            unsafe_allow_html=True
        )

        # MODE
        st.markdown(
            f'<div class="design-card-mode">🤖 {mode}</div>',
            unsafe_allow_html=True
        )

        # DESCRIPTION
        short_description = description

        if len(short_description) > 120:

            short_description = (
                short_description[:120]
                + "..."
            )

        st.markdown(
            f'<div class="design-card-description">{short_description}</div>',
            unsafe_allow_html=True
        )

        # METADATA
        if metadata:

            pills = ""

            for item in metadata[:3]:

                pills += (
                    f'<span class="metadata-pill">'
                    f'{item}'
                    f'</span>'
                )

            st.markdown(
                pills,
                unsafe_allow_html=True
            )

        st.caption(
            f"📅 {created_at}"
        )

        # VIEW
        if st.button(
            "👁 View Design",
            use_container_width=True,
            key=(
                f"view_design_"
                f"{design_id}_"
                f"{index}"
            )
        ):

            st.session_state[
                "design_library_selected"
            ] = design

            st.rerun()


# ============================================================
# FEATURED DESIGN
# ============================================================

def render_featured_design(design):

    image_bytes = get_image_bytes(
        design.get("image_data")
    )

    if not image_bytes:
        return

    title = get_design_title(design)

    mode = get_design_mode(design)

    description = get_design_description(design)

    left, right = st.columns(
        [1.25, 1],
        gap="large"
    )

    with left:

        st.image(
            image_bytes,
            use_container_width=True
        )

    with right:

        st.caption(
            "LATEST AI CREATION"
        )

        st.subheader(
            title
        )

        st.caption(
            f"🤖 {mode}"
        )

        st.write(
            description
        )

        metadata = get_design_metadata(
            design
        )

        if metadata:

            for item in metadata[:5]:

                st.caption(item)

        action1, action2 = st.columns(2)

        with action1:

            st.download_button(
                "⬇ Download",
                data=image_bytes,
                file_name=(
                    f"StyleSense_Featured_"
                    f"{design.get('id', 'design')}.png"
                ),
                mime="image/png",
                use_container_width=True,
                key=(
                    f"featured_download_"
                    f"{design.get('id', 'design')}"
                )
            )

        with action2:

            if st.button(
                "👁 Open",
                use_container_width=True,
                key=(
                    f"featured_open_"
                    f"{design.get('id', 'design')}"
                )
            ):

                st.session_state[
                    "design_library_selected"
                ] = design

                st.rerun()


# ============================================================
# EMPTY STATE
# ============================================================

def render_empty_library():

    st.info(
        "🎨 Your creative library is empty."
    )

    st.write(
        "Your AI-generated fashion designs will "
        "appear here. Start creating your first "
        "concept with StyleSense AI."
    )

    if st.button(
        "✨ Create Your First AI Design",
        type="primary",
        use_container_width=True,
        key="empty_library_create"
    ):

        go_to_design_studio()


# ============================================================
# MAIN DESIGN LIBRARY
# ============================================================

def render_design_library():

    inject_design_library_css()

    # ========================================================
    # SELECTED DESIGN
    # ========================================================

    selected_design = st.session_state.get(
        "design_library_selected"
    )

    if selected_design:

        if st.button(
            "← Back to Design Library",
            key="back_to_design_library"
        ):

            st.session_state.pop(
                "design_library_selected",
                None
            )

            st.rerun()

        st.divider()

        render_design_details(
            selected_design
        )

        return

    # ========================================================
    # HERO
    # ========================================================

    st.caption(
        "STYLESENSE AI OS • CREATIVE WORKSPACE"
    )

    st.title(
        "📚 Design Library"
    )

    st.write(
        "Your intelligent archive for AI-generated "
        "fashion concepts, references and creative "
        "experiments."
    )

    # ========================================================
    # LOAD DESIGNS
    # ========================================================

    try:

        designs = get_all_designs()

    except Exception as e:

        st.error(
            "Unable to load your Design Library."
        )

        st.exception(e)

        return

    # ========================================================
    # EMPTY
    # ========================================================

    if not designs:

        render_empty_library()

        return

    # ========================================================
    # TOP ACTION
    # ========================================================

    action1, action2 = st.columns(
        [1, 4]
    )

    with action1:

        if st.button(
            "＋ Create Design",
            type="primary",
            use_container_width=True,
            key="library_create_design"
        ):

            go_to_design_studio()

    with action2:

        st.caption(
            "Build, explore and manage your AI fashion archive."
        )

    st.write("")

        # ========================================================
    # STATISTICS
    # ========================================================

    total_designs = len(designs)

    guided_count = sum(
        1
        for design in designs
        if design.get("mode") == "Guided Design"
    )

    reference_count = sum(
        1
        for design in designs
        if design.get("reference_image")
    )

    advanced_count = sum(
        1
        for design in designs
        if design.get("mode")
        == "Advanced Prompt-to-Design"
    )

    st.markdown(
        "### 📊 Creative Activity"
    )

    st.caption(
        "A quick overview of your StyleSense AI design archive."
    )

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        st.metric(
            label="🎨 Saved Designs",
            value=total_designs
        )

    with stat2:
        st.metric(
            label="✨ Guided Designs",
            value=guided_count
        )

    with stat3:
        st.metric(
            label="🖼️ Reference Designs",
            value=reference_count
        )

    with stat4:
        st.metric(
            label="🤖 Advanced AI",
            value=advanced_count
        )

    st.write("")

    # ========================================================
    # FEATURED
    # ========================================================

    st.subheader(
        "✨ Featured Creation"
    )

    st.caption(
        "Your latest addition to the StyleSense creative archive."
    )

    latest_design = designs[0]

    render_featured_design(
        latest_design
    )

    st.divider()

    # ========================================================
    # SEARCH
    # ========================================================

    st.subheader(
        "Explore Your Designs"
    )

    st.caption(
        "Search and organize your AI fashion creations."
    )

    search_col, sort_col = st.columns(
        [4, 1]
    )

    with search_col:

        search = st.text_input(
            "Search",
            placeholder=(
                "Search designs, fabrics, occasions, "
                "themes, styles or markets..."
            ),
            label_visibility="collapsed",
            key="design_library_search"
        )

    with sort_col:

        sort_order = st.selectbox(
            "Sort",
            [
                "Newest",
                "Oldest"
            ],
            label_visibility="collapsed",
            key="design_library_sort"
        )

    # ========================================================
    # FILTERS
    # ========================================================

    filter1, filter2, filter3 = st.columns(3)

    with filter1:

        mode_filter = st.selectbox(
            "Design Type",
            [
                "All",
                "Guided Design",
                "Advanced Prompt-to-Design",
                "Reference Image → Design"
            ],
            key="design_library_mode"
        )

    with filter2:

        categories = sorted(
            list(
                set(
                    design.get("category")
                    for design in designs
                    if design.get("category")
                )
            )
        )

        category_filter = st.selectbox(
            "Category",
            ["All"] + categories,
            key="design_library_category"
        )

    with filter3:

        quick_filter = st.selectbox(
            "View",
            [
                "All Designs",
                "AI Generated",
                "Reference Designs"
            ],
            key="design_library_quick_filter"
        )

    # ========================================================
    # FILTER
    # ========================================================

    filtered_designs = []

    search_term = (
        search.strip().lower()
        if search
        else ""
    )

    for design in designs:

        # SEARCH
        if search_term:

            searchable_fields = [
                "design",
                "mode",
                "category",
                "fabric",
                "occasion",
                "theme",
                "market",
                "culture",
                "style",
                "colour",
                "gender",
                "country"
            ]

            searchable = " ".join(
                str(
                    design.get(
                        field,
                        ""
                    )
                )
                for field in searchable_fields
            ).lower()

            if search_term not in searchable:
                continue

        # MODE
        if (
            mode_filter != "All"
            and design.get("mode")
            != mode_filter
        ):

            continue

        # CATEGORY
        if (
            category_filter != "All"
            and design.get("category")
            != category_filter
        ):

            continue

        # QUICK FILTER
        if quick_filter == "Reference Designs":

            if not design.get(
                "reference_image"
            ):

                continue

        elif quick_filter == "AI Generated":

            if design.get(
                "reference_image"
            ):

                continue

        filtered_designs.append(
            design
        )

    # ========================================================
    # SORT
    # ========================================================

    if sort_order == "Newest":

        filtered_designs.sort(
            key=lambda x: x.get("id", 0),
            reverse=True
        )

    else:

        filtered_designs.sort(
            key=lambda x: x.get("id", 0)
        )

    # ========================================================
    # RESULTS
    # ========================================================

    st.caption(
        f"Showing {len(filtered_designs)} "
        f"of {total_designs} designs"
    )

    # ========================================================
    # NO RESULTS
    # ========================================================

    if not filtered_designs:

        st.info(
            "🔍 No designs found. "
            "Try a different search term or adjust your filters."
        )

        return

    # ========================================================
    # DESIGN GALLERY
    # ========================================================

    st.subheader(
        "Your Designs"
    )

    st.caption(
        "Browse your AI fashion creations."
    )

    columns = st.columns(
        3,
        gap="medium"
    )

    for index, design in enumerate(
        filtered_designs
    ):

        with columns[
            index % 3
        ]:

            render_design_card(
                design,
                index
            )

    # ========================================================
    # LIBRARY MANAGEMENT
    # ========================================================

    st.divider()

    with st.expander(
        "⚙️ Library Management"
    ):

        st.warning(
            "Deleting the entire library permanently "
            "removes all saved designs."
        )

        confirm_clear = st.checkbox(
            "I understand that this cannot be undone.",
            key="confirm_clear_designs"
        )

        if st.button(
            "🗑 Clear Entire Design Library",
            disabled=not confirm_clear,
            use_container_width=True,
            key="clear_all_designs"
        ):

            try:

                count = clear_all_designs()

                st.success(
                    f"{count} design(s) deleted."
                )

                st.session_state.pop(
                    "design_library_selected",
                    None
                )

                st.rerun()

            except Exception as e:

                st.error(
                    "Unable to clear Design Library."
                )

                st.exception(e)