import os
import streamlit as st
from dotenv import load_dotenv
from google import genai


# Load local .env file
load_dotenv()


# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# If running on Streamlit Cloud, get it from Secrets
if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        GEMINI_API_KEY = None


# Make sure the API key exists
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found.")


# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(prompt):
    """
    Send a prompt to Gemini and return the generated text.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        raise Exception(f"Gemini API Error: {e}")