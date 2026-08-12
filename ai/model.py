import os
import io
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai
from PIL import Image


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# GET GEMINI API KEY
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        GEMINI_API_KEY = None


if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found.")


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# GEMINI MODEL
# =========================================================

GEMINI_MODEL = "gemini-3.6-flash"


# =========================================================
# TEXT AI
# =========================================================

def ask_gemini(prompt):
    """
    Send a text-only prompt to Gemini.
    """

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if response.text:
            return response.text

        return "❌ Gemini returned an empty response."

    except Exception as e:

        error_text = str(e)

        # -------------------------------------------------
        # RATE LIMIT / QUOTA ERROR
        # -------------------------------------------------

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

            st.error(
                "⚠️ Gemini API quota/rate limit reached. "
                "Please wait and try again, or check your Gemini "
                "API billing/quota."
            )

        # -------------------------------------------------
        # MODEL ERROR
        # -------------------------------------------------

        elif "404" in error_text or "NOT_FOUND" in error_text:

            st.error(
                f"❌ Gemini model error: {error_text}"
            )

        # -------------------------------------------------
        # OTHER ERROR
        # -------------------------------------------------

        else:

            st.error(
                f"❌ Gemini API Error: "
                f"{type(e).__name__}: {e}"
            )

        return "❌ Unable to get a response from Gemini."


# =========================================================
# OUTFIT IMAGE ANALYZER
# =========================================================

def analyze_outfit(image):
    """
    Send an outfit image to Gemini for visual analysis.
    """

    try:

        # -------------------------------------------------
        # CONVERT INPUT TO PIL IMAGE
        # -------------------------------------------------

        if not isinstance(image, Image.Image):
            image = Image.open(image)

        if image.mode != "RGB":
            image = image.convert("RGB")


        # -------------------------------------------------
        # CONVERT IMAGE TO JPEG BYTES
        # -------------------------------------------------

        image_bytes = io.BytesIO()

        image.save(
            image_bytes,
            format="JPEG",
            quality=90
        )

        image_bytes = image_bytes.getvalue()


        # -------------------------------------------------
        # IMAGE PART
        # -------------------------------------------------

        image_part = {
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }
        }


        # -------------------------------------------------
        # FASHION ANALYSIS PROMPT
        # -------------------------------------------------

        prompt = """
You are an expert fashion stylist and image analyst.

Analyze the actual outfit shown in the uploaded image.

Do not ask the user to upload an image again.

Analyze:

- clothing pieces
- silhouette
- fit
- colors
- patterns
- fabric appearance
- footwear
- accessories
- proportions
- styling
- color coordination
- overall aesthetic

Base your analysis ONLY on what is actually visible
in the uploaded image.

Return exactly these sections:

# Style

# Strengths

# Weaknesses

# Color Harmony

# Accessories

# Improvement Suggestions

Be specific, practical, and honest.
"""


        # -------------------------------------------------
        # SEND IMAGE + PROMPT TO GEMINI
        # -------------------------------------------------

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                prompt,
                image_part
            ]
        )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        if response.text:

            return response.text

        return "❌ Gemini returned an empty analysis."


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        error_text = str(e)


        # -------------------------------------------------
        # RATE LIMIT
        # -------------------------------------------------

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

            st.error(
                "⚠️ Gemini API quota/rate limit reached. "
                "Please wait and try again, or check your "
                "Gemini API billing/quota."
            )


        # -------------------------------------------------
        # MODEL NOT FOUND
        # -------------------------------------------------

        elif "404" in error_text or "NOT_FOUND" in error_text:

            st.error(
                f"❌ Gemini model error: {error_text}"
            )


        # -------------------------------------------------
        # OTHER ERROR
        # -------------------------------------------------

        else:

            st.error(
                f"❌ Gemini Outfit Analysis Error: "
                f"{type(e).__name__}: {e}"
            )


        return None