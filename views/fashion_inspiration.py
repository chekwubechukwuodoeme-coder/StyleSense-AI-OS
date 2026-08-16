import io
import urllib.request
import re

import streamlit as st

from services.pexels_service import search_fashion_images

from ai import (
    fashion_chat,
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "saved_inspirations": [],
    "selected_images": [],
    "collections": [],
    "current_design": "",
    "saved_designs": [],

    # Design Studio connection
    "open_design_studio": False,
    "studio_reference_image_url": None,
    "studio_reference_title": "",
    "studio_reference_photographer": "",
}


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# TRENDING SEARCHES
# ============================================================

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
    "Modern Native Wear",

]


# ============================================================
# HERO
# ============================================================

def hero():

    st.title("💡 Fashion Inspiration")

    st.caption(
        """
Discover premium fashion inspiration from around the world
and transform ideas into AI-powered fashion concepts.
"""
    )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    st.divider()

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Saved",
            len(st.session_state.saved_inspirations)
        )

    with m2:

        st.metric(
            "Collections",
            len(st.session_state.collections)
        )

    with m3:

        st.metric(
            "AI Designs",
            len(st.session_state.saved_designs)
        )

    with m4:

        st.metric(
            "AI Status",
            "🟢 Online"
        )

    st.divider()


# ============================================================
# TRENDING
# ============================================================

def trending():

    st.subheader("🔥 Trending Fashion")

    cols = st.columns(4)

    selected = None

    for i, trend in enumerate(TRENDING):

        if cols[i % 4].button(
            trend,
            use_container_width=True,
            key=f"trend_{i}"
        ):

            selected = trend

    return selected


# ============================================================
# SEARCH
# ============================================================

def search_box(default_value=""):

    return st.text_input(
        "🔎 Search Inspiration",
        value=default_value,
        placeholder=(
            "Luxury Ankara, Streetwear, "
            "Wedding Suit..."
        )
    )


# ============================================================
# FILTERS
# ============================================================

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
        "country": country,
    }


# ============================================================
# SEARCH PEXELS
# ============================================================

def get_images(search):

    if not search:
        return []

    try:

        with st.spinner(
            "🔍 Searching fashion inspiration..."
        ):

            return search_fashion_images(search)

    except Exception as e:

        st.error(
            f"Fashion inspiration search failed: {e}"
        )

        return []


# ============================================================
# DOWNLOAD ORIGINAL PEXELS IMAGE
# ============================================================

def download_image_bytes(url):

    if not url:
        return None

    try:

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            return response.read()

    except Exception as e:

        st.warning(
            f"Unable to download this image: {e}"
        )

        return None


# ============================================================
# SAFE FILE NAME
# ============================================================

def safe_filename(title):

    title = title or "fashion_inspiration"

    title = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        title
    )

    return title[:80].strip("_") or "fashion_inspiration"


# ============================================================
# SAVE INSPIRATION
# ============================================================

def save_inspiration(image):

    image_id = image.get("id")

    exists = any(
        item.get("id") == image_id
        for item in st.session_state.saved_inspirations
    )

    if not exists:

        st.session_state.saved_inspirations.append(
            image
        )

        st.toast(
            "❤️ Inspiration Saved",
            icon="❤️"
        )

    else:

        st.info(
            "This inspiration is already saved."
        )


# ============================================================
# SEND TO DESIGN STUDIO
# ============================================================

def send_to_design_studio(image):

    st.session_state.studio_reference_image_url = (
        image.get("url")
    )

    st.session_state.studio_reference_title = (
        image.get(
            "title",
            "Fashion Inspiration"
        )
    )

    st.session_state.studio_reference_photographer = (
        image.get(
            "photographer",
            "Pexels"
        )
    )

    st.session_state.open_design_studio = True

    st.rerun()


# ============================================================
# AI ANALYSIS
# ============================================================

def ai_analysis(image):

    st.markdown(
        "### 🤖 AI Fashion Analysis"
    )

    prompt = f"""
Analyze this fashion inspiration.

Title:
{image.get('title', '')}

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

    try:

        with st.spinner(
            "🤖 AI is analyzing the inspiration..."
        ):

            result = fashion_chat(prompt)

        st.markdown(result)

    except Exception as e:

        st.error(
            f"AI analysis failed: {e}"
        )


# ============================================================
# GENERATE SIMILAR CONCEPT
# ============================================================

def generate_similar(search):

    prompt = f"""
Create a completely original luxury fashion design.

Fashion inspiration/search:
{search}

Include:

# Design Concept

# Luxury Features

# Color Palette

# Fabrics

# Tailoring

# Accessories

# Shoes

# Hairstyle

# Styling Tips

Do not copy an existing design.

Create something unique.
"""

    try:

        with st.spinner(
            "✨ AI is designing..."
        ):

            design = fashion_chat(prompt)

        st.session_state.current_design = design

        st.success(
            "✅ Design concept created successfully!"
        )

        st.markdown(design)

    except Exception as e:

        st.error(
            f"Design generation failed: {e}"
        )


# ============================================================
# IMAGE CARD
# ============================================================

def image_card(image, index, search):

    with st.container(border=True):

        image_url = image.get("url")

        if image_url:

            st.image(
                image_url,
                use_container_width=True
            )

        st.markdown(
            f"**📸 {image.get('photographer', 'Pexels')}**"
        )

        title = image.get(
            "title",
            "Fashion Inspiration"
        )

        st.caption(title)

        st.progress(0.92)

        st.caption(
            "Luxury Score • 92%"
        )

        # ====================================================
        # DOWNLOAD ORIGINAL
        # ====================================================

        image_bytes = download_image_bytes(
            image_url
        )

        if image_bytes:

            filename = safe_filename(title)

            st.download_button(
                "⬇️ Download Original",
                data=image_bytes,
                file_name=f"{filename}.jpg",
                mime="image/jpeg",
                use_container_width=True,
                key=f"download_original_{index}_{image.get('id', index)}"
            )

        # ====================================================
        # ROW 1
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "❤️ Save",
                key=f"save_{index}_{image.get('id', index)}",
                use_container_width=True
            ):

                save_inspiration(image)

        with col2:

            if st.button(
                "✨ Generate",
                key=f"generate_{index}_{image.get('id', index)}",
                use_container_width=True
            ):

                generate_similar(search)

        # ====================================================
        # ROW 2
        # ====================================================

        col3, col4 = st.columns(2)

        with col3:

            if st.button(
                "🤖 Analyze",
                key=f"analysis_{index}_{image.get('id', index)}",
                use_container_width=True
            ):

                ai_analysis(image)

        with col4:

            if st.button(
                "🎨 Studio",
                key=f"studio_{index}_{image.get('id', index)}",
                use_container_width=True
            ):

                send_to_design_studio(image)


# ============================================================
# GALLERY
# ============================================================

def gallery(images, search):

    st.subheader(
        "🖼️ Inspiration Gallery"
    )

    cols = st.columns(4)

    for index, image in enumerate(images):

        with cols[index % 4]:

            image_card(
                image,
                index,
                search
            )


# ============================================================
# SAVED INSPIRATIONS
# ============================================================

def saved_inspirations():

    st.divider()

    st.subheader(
        "❤️ Saved Inspirations"
    )

    saved = st.session_state.saved_inspirations

    if not saved:

        st.info(
            "You haven't saved any inspiration yet."
        )

        return

    cols = st.columns(4)

    for index, image in enumerate(saved):

        with cols[index % 4]:

            with st.container(border=True):

                image_url = image.get("url")

                if image_url:

                    st.image(
                        image_url,
                        use_container_width=True
                    )

                title = image.get(
                    "title",
                    "Fashion Inspiration"
                )

                st.caption(title)

                # --------------------------------------------
                # ORIGINAL DOWNLOAD
                # --------------------------------------------

                image_bytes = download_image_bytes(
                    image_url
                )

                if image_bytes:

                    st.download_button(
                        "⬇️ Download Original",
                        data=image_bytes,
                        file_name=(
                            f"Saved_Inspiration_{index + 1}.jpg"
                        ),
                        mime="image/jpeg",
                        use_container_width=True,
                        key=f"saved_download_{index}_{image.get('id', index)}"
                    )

                # --------------------------------------------
                # DESIGN STUDIO
                # --------------------------------------------

                if st.button(
                    "🎨 Use In Studio",
                    key=f"saved_studio_{index}_{image.get('id', index)}",
                    use_container_width=True
                ):

                    send_to_design_studio(image)

                # --------------------------------------------
                # DELETE
                # --------------------------------------------

                if st.button(
                    "🗑️ Remove",
                    key=f"remove_{index}_{image.get('id', index)}",
                    use_container_width=True
                ):

                    st.session_state.saved_inspirations.remove(
                        image
                    )

                    st.rerun()


# ============================================================
# MOODBOARD
# ============================================================

def moodboard():

    st.divider()

    st.subheader(
        "📄 AI Moodboard"
    )

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

        try:

            with st.spinner(
                "Creating moodboard..."
            ):

                result = fashion_chat(prompt)

            st.markdown(result)

        except Exception as e:

            st.error(
                f"Moodboard generation failed: {e}"
            )


# ============================================================
# COLLECTION BUILDER
# ============================================================

def collection_builder():

    st.divider()

    st.subheader(
        "🎯 Collection Builder"
    )

    collection_name = st.text_input(
        "Collection Name"
    )

    if st.button(
        "Build Collection",
        use_container_width=True
    ):

        if not collection_name.strip():

            st.warning(
                "Please enter a collection name."
            )

            return

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

        try:

            with st.spinner(
                "Building collection..."
            ):

                collection = fashion_chat(prompt)

            st.session_state.collections.append(
                collection
            )

            st.success(
                "✅ Collection created!"
            )

            st.markdown(collection)

        except Exception as e:

            st.error(
                f"Collection generation failed: {e}"
            )


# ============================================================
# MAIN PAGE
# ============================================================

def render_fashion_inspiration():

    hero()

    dashboard()

    trending_search = trending()

    search = search_box(
        trending_search or ""
    )

    filters()

    if not search:

        st.info(
            "Search for fashion inspiration "
            "or choose a trending topic."
        )

        return

    images = get_images(search)

    if not images:

        st.warning(
            "No inspiration found."
        )

        return

    gallery(
        images,
        search
    )

    saved_inspirations()

    moodboard()

    collection_builder()