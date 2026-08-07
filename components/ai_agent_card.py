import streamlit as st

def agent_card(
    title,
    description,
    status="Ready"
):

    with st.container(border=True):

        st.subheader(title)

        st.write(description)

        st.success(status)