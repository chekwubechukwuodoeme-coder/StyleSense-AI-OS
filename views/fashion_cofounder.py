import streamlit as st

from ai.business import fashion_cofounder


def render_fashion_cofounder():

    st.title("🚀 AI Fashion Co-Founder")

    idea = st.text_area(
        "Describe the fashion business you want to build",
        height=200,
        placeholder="Example: I want to build a luxury African streetwear brand for university students."
    )

    if st.button(
        "🚀 Build My Fashion Brand",
        use_container_width=True
    ):

        if not idea.strip():
            st.warning("Please describe your business idea.")
            return

        with st.spinner("Building your fashion business..."):

            result = fashion_cofounder(idea)

        st.markdown(result)