import streamlit as st

def initialize_session():

    defaults = {

        "saved_designs": [],

        "messages": [],

        "current_design": "",

        "current_image": None

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value