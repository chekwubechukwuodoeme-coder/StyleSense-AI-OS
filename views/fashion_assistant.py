import streamlit as st
from ai import fashion_chat

def render_fashion_assistant():

    st.header("🤖 Fashion Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for role, message in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(message)

    prompt = st.chat_input(
        "Ask me anything about fashion..."
    )

    if prompt:

        st.session_state.messages.append(
            ("user", prompt)
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                reply = fashion_chat(prompt)

                st.markdown(reply)

        st.session_state.messages.append(
            ("assistant", reply)
        )