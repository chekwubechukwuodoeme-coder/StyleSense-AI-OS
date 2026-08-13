import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_api_key():
    # Local development
    key = os.getenv("OPENAI_API_KEY")

    # Streamlit Cloud
    if not key:
        try:
            key = st.secrets.get("OPENAI_API_KEY")
        except Exception:
            key = None

    return key


OPENAI_API_KEY = get_api_key()

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY was not found. "
        "Add it to .env locally or Streamlit Secrets when deployed."
    )


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def ask_openai(prompt, model="gpt-5-mini"):
    """
    Send a text prompt to OpenAI.
    """

    try:

        response = client.responses.create(
            model=model,
            input=prompt
        )

        if response.output_text:
            return response.output_text

        return "❌ OpenAI returned an empty response."

    except Exception as e:

        st.error(
            f"OpenAI API Error: {type(e).__name__}: {e}"
        )

        return None