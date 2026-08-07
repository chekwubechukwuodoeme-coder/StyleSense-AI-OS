import streamlit as st


def show_success(message):

    st.success(message)


def section(title):

    st.markdown(f"## {title}")