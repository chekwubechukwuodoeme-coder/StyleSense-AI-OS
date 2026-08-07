import streamlit as st


def render_design_library():

    st.header("📚 Saved Designs")

    if "saved_designs" not in st.session_state:
        st.session_state.saved_designs = []

    if not st.session_state.saved_designs:
        st.info("No saved designs yet.")
        return

    for i, item in enumerate(
        reversed(st.session_state.saved_designs),
        start=1
    ):

        with st.expander(f"Design {i}"):

            # Old saved designs (string)
            if isinstance(item, str):

                st.markdown(item)

            # New saved designs (dictionary)
            else:

                if item.get("image"):

                    st.image(
                        item["image"],
                        use_container_width=True
                    )

                st.markdown(item["design"])