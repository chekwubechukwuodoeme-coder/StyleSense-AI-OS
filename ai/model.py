import os
import base64
import io

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# GET OPENAI API KEY
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    try:
        OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        OPENAI_API_KEY = None


if not OPENAI_API_KEY:
    raise ValueError(
        "❌ OPENAI_API_KEY not found."
    )


# ============================================================
# OPENAI CLIENT
# ============================================================

@st.cache_resource
def get_openai_client():
    """
    Create the OpenAI client once and reuse it.
    This prevents Streamlit from recreating the client
    on every script rerun.
    """

    return OpenAI(
        api_key=OPENAI_API_KEY
    )


client = get_openai_client()


# ============================================================
# FAST MODEL
# ============================================================

OPENAI_MODEL = "gpt-5-mini"


# ============================================================
# TEXT AI
# ============================================================

def ask_openai(prompt):
    """
    Fast text generation using OpenAI.
    """

    if not prompt:
        return "❌ Empty prompt."

    try:

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
            max_output_tokens=1200,
        )

        if response.output_text:
            return response.output_text

        return "❌ OpenAI returned an empty response."

    except Exception as e:

        st.error(
            f"❌ OpenAI API Error: "
            f"{type(e).__name__}: {e}"
        )

        return (
            "❌ Unable to get a response from OpenAI."
        )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def ask_gemini(prompt):
    """
    Compatibility wrapper.

    StyleSense is NOT using the Gemini API.

    Older modules may still call ask_gemini().
    Those calls are redirected to OpenAI.
    """

    return ask_openai(prompt)


# ============================================================
# OPENAI VISION
# ============================================================

def ask_openai_vision(
    prompt,
    image_data
):
    """
    Send text + image to OpenAI.
    """

    if not prompt:
        return "❌ Empty prompt."

    if not image_data:
        return "❌ No image provided."

    try:

        response = client.responses.create(

            model=OPENAI_MODEL,

            input=[
                {
                    "role": "user",

                    "content": [

                        {
                            "type": "input_text",
                            "text": prompt
                        },

                        {
                            "type": "input_image",
                            "image_url": image_data
                        }

                    ]
                }
            ],

            max_output_tokens=1200,
        )

        if response.output_text:

            return response.output_text

        return (
            "❌ OpenAI returned an empty "
            "image analysis."
        )

    except Exception as e:

        st.error(
            f"❌ OpenAI Vision Error: "
            f"{type(e).__name__}: {e}"
        )

        return None


# ============================================================
# OUTFIT ANALYZER
# ============================================================

def analyze_outfit(image):
    """
    Analyze an uploaded outfit image using OpenAI vision.
    """

    try:

        # ----------------------------------------------------
        # CONVERT TO PIL IMAGE
        # ----------------------------------------------------

        if not isinstance(
            image,
            Image.Image
        ):

            image = Image.open(image)


        # ----------------------------------------------------
        # RGB
        # ----------------------------------------------------

        if image.mode != "RGB":

            image = image.convert("RGB")


        # ----------------------------------------------------
        # RESIZE
        # ----------------------------------------------------

        max_size = 1200

        if max(image.size) > max_size:

            image.thumbnail(
                (
                    max_size,
                    max_size
                ),
                Image.Resampling.LANCZOS
            )


        # ----------------------------------------------------
        # JPEG COMPRESSION
        # ----------------------------------------------------

        image_bytes = io.BytesIO()

        image.save(
            image_bytes,
            format="JPEG",
            quality=82,
            optimize=True
        )

        image_bytes = image_bytes.getvalue()


        # ----------------------------------------------------
        # BASE64
        # ----------------------------------------------------

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")


        image_data = (
            "data:image/jpeg;base64,"
            + image_base64
        )


        # ----------------------------------------------------
        # PROMPT
        # ----------------------------------------------------

        prompt = """
You are an expert fashion stylist and image analyst
for StyleSense AI OS.

Analyze ONLY what is visibly present in the uploaded image.

Do not invent brands, prices, measurements,
fabric composition, or clothing pieces.

Analyze:

- Clothing
- Silhouette
- Fit
- Proportions
- Colors
- Patterns
- Fabric appearance
- Footwear
- Accessories
- Layering
- Styling
- Overall aesthetic

Return EXACTLY:

# Style

# Strengths

# Weaknesses

# Color Harmony

# Accessories

# Improvement Suggestions

Be specific, concise and practical.
"""


        # ----------------------------------------------------
        # OPENAI VISION
        # ----------------------------------------------------

        return ask_openai_vision(
            prompt=prompt,
            image_data=image_data
        )


    except Exception as e:

        st.error(
            f"❌ Outfit Analysis Error: "
            f"{type(e).__name__}: {e}"
        )

        return None