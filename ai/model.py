import os
import io

import streamlit as st
from dotenv import load_dotenv
from google import genai
from PIL import Image


# ==========================
# LOAD ENVIRONMENT
# ==========================

load_dotenv()


# ==========================
# GET GEMINI API KEY
# ==========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        GEMINI_API_KEY = None


if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found.")


# ==========================
# GEMINI CLIENT
# ==========================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================
# TEXT AI
# ==========================

def ask_gemini(prompt):
    """
    Send a text-only prompt to Gemini.
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

        st.error(
            f"Gemini API Error: {type(e).__name__}: {e}"
        )

        return "❌ Unable to get a response from Gemini."


# ==========================
# OUTFIT IMAGE ANALYZER
# ==========================

def analyze_outfit(image):
    """
    Send an outfit image to Gemini for visual analysis.
    """

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    if image.mode != "RGB":
        image = image.convert("RGB")

    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG", quality=90)
    image_bytes = image_bytes.getvalue()

    image_part = {
        "inline_data": {
            "mime_type": "image/jpeg",
            "data": image_bytes
        }
    }

    prompt = """
You are an expert fashion stylist and image analyst.

Analyze the actual outfit shown in the uploaded image.

Do not ask the user to upload an image again.

Analyze the clothing pieces, silhouette, fit, colors, patterns,
fabric appearance, footwear, accessories, proportions, styling,
color coordination, and overall aesthetic.

Return exactly these sections:

# Style

# Strengths

# Weaknesses

# Color Harmony

# Accessories

# Improvement Suggestions

Be specific and base your analysis only on what is visible in the image.
"""

    models = [
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-flash-latest",
    ]

    last_error = None

    for model in models:

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=[
                        prompt,
                        image_part
                    ]
                )

                if response.text:
                    return response.text

                last_error = "Gemini returned an empty response."

            except Exception as e:

                last_error = e

                error_text = str(e)

                # Retry temporary server overload errors
                if "503" in error_text or "UNAVAILABLE" in error_text:

                    import time
                    time.sleep(2)

                    continue

                # Move to the next model for model-specific errors
                break

    st.error(
        f"Gemini Outfit Analysis failed: {last_error}"
    )

    return None