import streamlit as st

# -----------------------------
# Session State Initialization
# -----------------------------

if "saved_inspirations" not in st.session_state:
    st.session_state.saved_inspirations = []

if "selected_images" not in st.session_state:
    st.session_state.selected_images = []

if "collections" not in st.session_state:
    st.session_state.collections = []

if "current_design" not in st.session_state:
    st.session_state.current_design = ""

if "saved_designs" not in st.session_state:
    st.session_state.saved_designs = []

from services.pexels_service import search_fashion_images

from ai import (
    fashion_chat,
    analyze_outfit,
)

# ----------------------------------------
# Session State
# ----------------------------------------

if "saved_inspirations" not in st.session_state:
    st.session_state.saved_inspirations = []

if "selected_images" not in st.session_state:
    st.session_state.selected_images = []

if "collections" not in st.session_state:
    st.session_state.collections = []

if "current_design" not in st.session_state:
    st.session_state.current_design = ""

# ----------------------------------------
# Trending Searches
# ----------------------------------------

TRENDING = [

    "Luxury Ankara",

    "Old Money",

    "Royal Wedding",

    "Celebrity Fashion",

    "Italian Suit",

    "Streetwear",

    "Corporate Fashion",

    "African Royalty",

    "Luxury Agbada",

    "Paris Fashion Week",

    "Luxury Lace",

    "Modern Native Wear"

]

# ----------------------------------------
# Hero Section
# ----------------------------------------

def hero():

    st.title("💡 Fashion Inspiration")

    st.caption(
        """
Discover premium fashion inspiration from
around the world and transform ideas into
AI-powered fashion concepts.
"""
    )

# ----------------------------------------
# Dashboard
# ----------------------------------------

def dashboard():

    st.divider()

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(

            "Saved",

            len(
                st.session_state.saved_inspirations
            )

        )

    with m2:

        st.metric(

            "Collections",

            len(
                st.session_state.collections
            )

        )

    with m3:

        st.metric(

            "AI Designs",

            len(
                st.session_state.get(
                    "saved_designs",
                    []
                )
            )

        )

    with m4:

        st.metric(

            "AI Status",

            "🟢 Online"

        )

    st.divider()

# ----------------------------------------
# Trending Buttons
# ----------------------------------------

def trending():

    st.subheader("🔥 Trending Fashion")

    cols = st.columns(4)

    selected = None

    for i, trend in enumerate(TRENDING):

        if cols[i % 4].button(

            trend,

            use_container_width=True

        ):

            selected = trend

    return selected

# ----------------------------------------
# Search
# ----------------------------------------

def search_box(default_value=""):

    return st.text_input(

        "Search Inspiration",

        value=default_value,

        placeholder="Luxury Ankara, Streetwear, Wedding Suit..."

    )

# ----------------------------------------
# Filters
# ----------------------------------------

def filters():

    with st.expander(

        "🎯 Advanced Filters",

        expanded=False

    ):

        col1, col2 = st.columns(2)

        with col1:

            gender = st.selectbox(

                "Gender",

                [

                    "All",

                    "Male",

                    "Female",

                    "Unisex"

                ]

            )

            occasion = st.selectbox(

                "Occasion",

                [

                    "All",

                    "Wedding",

                    "Corporate",

                    "Luxury",

                    "Casual",

                    "Traditional"

                ]

            )

            fabric = st.selectbox(

                "Fabric",

                [

                    "All",

                    "Ankara",

                    "Silk",

                    "Lace",

                    "Cotton",

                    "Velvet",

                    "Leather"

                ]

            )

        with col2:

            color = st.selectbox(

                "Primary Color",

                [

                    "All",

                    "Black",

                    "White",

                    "Gold",

                    "Royal Blue",

                    "Wine",

                    "Brown"

                ]

            )

            luxury = st.selectbox(

                "Luxury Level",

                [

                    "Standard",

                    "Premium",

                    "Luxury",

                    "Elite"

                ]

            )

            country = st.selectbox(

                "Country",

                [

                    "Nigeria",

                    "Ghana",

                    "South Africa",

                    "United Kingdom",

                    "France",

                    "Italy"

                ]

            )

    return {

        "gender": gender,

        "occasion": occasion,

        "fabric": fabric,

        "color": color,

        "luxury": luxury,

        "country": country

    }

# ----------------------------------------
# Search Images
# ----------------------------------------

def get_images(search):

    if not search:
        return []

    try:

        with st.spinner("🔍 Searching fashion inspiration..."):

            return search_fashion_images(search)

    except Exception as e:

        st.error(e)

        return []


# ----------------------------------------
# Save Inspiration
# ----------------------------------------

def save_inspiration(image):

    exists = any(
        item["id"] == image["id"]
        for item in st.session_state.saved_inspirations
    )

    if not exists:

        st.session_state.saved_inspirations.append(image)

        st.toast(
            "❤️ Inspiration Saved",
            icon="❤️"
        )

    else:

        st.info("Already saved.")


# ----------------------------------------
# AI Analysis
# ----------------------------------------

def ai_analysis(image):

    st.markdown("### 🤖 AI Fashion Analysis")

    prompt = f"""
Analyze this fashion inspiration.

Title:

{image['title']}

Create a professional fashion analysis.

Include:

# Luxury Score

# Dominant Colors

# Suggested Fabrics

# Target Audience

# Occasion

# Fashion Style

# Accessories

# Shoes

# Styling Tips

# Photoshoot Idea
"""

    result = fashion_chat(prompt)

    st.markdown(result)


# ----------------------------------------
# Generate Similar
# ----------------------------------------

def generate_similar(search):

    prompt = f"""
Create a completely original luxury fashion design.

Inspired by:

{search}

Include

# Design Concept

# Luxury Features

# Color Palette

# Fabrics

# Tailoring

# Accessories

# Shoes

# Hairstyle

# Styling Tips

Do not copy the inspiration.

Create something unique.
"""

    with st.spinner("✨ AI is designing..."):

        design = fashion_chat(prompt)

    st.session_state.current_design = design

    st.success("Design created successfully!")

    st.markdown(design)


# ----------------------------------------
# Image Card
# ----------------------------------------

def image_card(image, index, search):

    with st.container(border=True):

        st.image(

            image["url"],

            use_container_width=True

        )

        st.markdown(
            f"**📸 {image['photographer']}**"
        )

        st.caption(image["title"])

        st.progress(0.92)

        st.caption("Luxury Score • 92%")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(

                "❤️ Save",

                key=f"save_{index}",

                use_container_width=True

            ):

                save_inspiration(image)

        with col2:

            if st.button(

                "✨ Generate",

                key=f"generate_{index}",

                use_container_width=True

            ):

                generate_similar(search)

        col3, col4 = st.columns(2)

        with col3:

            if st.button(

                "🤖 Analyze",

                key=f"analysis_{index}",

                use_container_width=True

            ):

                ai_analysis(image)

        with col4:

            if st.button(

                "🎨 Studio",

                key=f"studio_{index}",

                use_container_width=True

            ):

                st.success(
                    "Open AI Design Studio from the sidebar."
                )


# ----------------------------------------
# Gallery
# ----------------------------------------

def gallery(images, search):

    st.subheader("🖼 Inspiration Gallery")

    cols = st.columns(4)

    for index, image in enumerate(images):

        with cols[index % 4]:

            image_card(
                image,
                index,
                search
            )

# ----------------------------------------
# Saved Inspirations
# ----------------------------------------

def saved_inspirations():

    st.divider()
    st.subheader("❤️ Saved Inspirations")

    saved = st.session_state.saved_inspirations

    if not saved:

        st.info("You haven't saved any inspiration yet.")
        return

    cols = st.columns(4)

    for index, image in enumerate(saved):

        with cols[index % 4]:

            with st.container(border=True):

                st.image(
                    image["url"],
                    use_container_width=True
                )

                st.caption(image["title"])

                if st.button(
                    "🗑 Remove",
                    key=f"remove_{index}",
                    use_container_width=True
                ):

                    st.session_state.saved_inspirations.remove(image)

                    st.rerun()


# ----------------------------------------
# Moodboard
# ----------------------------------------

def moodboard():

    st.divider()

    st.subheader("📄 AI Moodboard")

    if st.button(
        "Generate Moodboard",
        use_container_width=True
    ):

        prompt = """
Create a professional fashion moodboard.

Return:

# Theme

# Color Palette

# Recommended Fabrics

# Accessories

# Fashion Direction

# Target Audience

# Styling Advice
"""

        with st.spinner("Creating moodboard..."):

            result = fashion_chat(prompt)

        st.markdown(result)


# ----------------------------------------
# Collection Builder
# ----------------------------------------

def collection_builder():

    st.divider()

    st.subheader("🎯 Collection Builder")

    collection_name = st.text_input(
        "Collection Name"
    )

    if st.button(
        "Build Collection",
        use_container_width=True
    ):

        prompt = f"""
Create a luxury fashion collection.

Collection Name:

{collection_name}

Return:

# Collection Story

# Theme

# Look 1

# Look 2

# Look 3

# Look 4

# Look 5

# Color Palette

# Fabrics

# Accessories

# Marketing Direction
"""

        with st.spinner("Building collection..."):

            collection = fashion_chat(prompt)

        st.session_state.collections.append(collection)

        st.success("Collection created!")

        st.markdown(collection)


# ----------------------------------------
# Main Page
# ----------------------------------------

def render_fashion_inspiration():

    hero()

    dashboard()

    trending_search = trending()

    search = search_box(trending_search or "")

    filters()

    if not search:

        st.info(
            "Search for fashion inspiration or choose a trending topic."
        )

        return

    images = get_images(search)

    if not images:

        st.warning("No inspiration found.")

        return

    gallery(images, search)

    saved_inspirations()

    moodboard()

    collection_builder()