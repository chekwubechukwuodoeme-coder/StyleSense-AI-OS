import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load local .env
load_dotenv()

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Get API key from Streamlit Cloud Secrets if needed
if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        GEMINI_API_KEY = None

# Make sure API key exists
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found.")

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(prompt):
    """
    Send a text prompt to Gemini and return the generated response.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text

        return "❌ Gemini returned an empty response."

    except Exception as e:
        st.error(f"Gemini API Error: {type(e).__name__}: {e}")
        return "❌ Unable to get a response from Gemini."