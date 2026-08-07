import streamlit as st

def project_card(
    title,
    status,
    progress,
    designs
):

    with st.container(border=True):

        st.subheader(title)

        st.write(f"Status: {status}")

        st.progress(progress)

        st.write(f"Designs: {designs}")

        st.button(
            "Open Workspace",
            key=title
        )