import streamlit as st
from PIL import Image

from ai import analyze_outfit


def render_outfit_analyzer():

    st.header("📸 AI Outfit Analyzer")

    uploaded_file = st.file_uploader(
        "Upload an outfit photo",
        type=["jpg", "jpeg", "png"]
    )

    if not uploaded_file:
        st.info("Upload an image to begin.")
        return

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Outfit",
        use_container_width=True
    )

    if st.button(
        "🔍 Analyze Outfit",
        use_container_width=True
    ):

        with st.spinner("Analyzing outfit..."):

            result = analyze_outfit(image)

        st.success("Analysis completed!")

        st.markdown(result)