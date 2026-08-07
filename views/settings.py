import streamlit as st


def render_settings():

    st.header("⚙ Settings")

    st.write("Customize your StyleSense AI experience.")

    st.subheader("Chat")

    if st.button(
        "🗑 Clear Chat History",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.success("Chat history cleared.")

    st.divider()

    st.subheader("Design Library")

    if st.button(
        "🗑 Delete All Saved Designs",
        use_container_width=True
    ):

        st.session_state.saved_designs = []

        st.success("All saved designs deleted.")