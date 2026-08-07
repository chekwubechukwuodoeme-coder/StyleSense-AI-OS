import streamlit as st
from ai import edit_design


def render_design_editor():

    st.header("✏ AI Design Editor")

    if "current_design" not in st.session_state:
        st.session_state.current_design = ""

    if not st.session_state.current_design:
        st.info("Generate a design first.")
        return

    st.markdown(st.session_state.current_design)

    instruction = st.text_area(
        "Describe what you want to change"
    )

    if st.button("✨ Edit Design"):

        with st.spinner("Updating design..."):

            updated = edit_design(
                st.session_state.current_design,
                instruction
            )

        st.session_state.current_design = updated

        st.markdown(updated)