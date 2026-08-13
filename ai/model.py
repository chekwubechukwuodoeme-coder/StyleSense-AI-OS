import os
import base64
import io

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# GET OPENAI API KEY
# =========================================================

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


# =========================================================
# OPENAI CLIENT
# =========================================================

client = OpenAI(
    api_key=OPENAI_API_KEY
)


# =========================================================
# DEFAULT MODEL
# =========================================================

OPENAI_MODEL = "gpt-5-mini"


# =========================================================
# TEXT AI
# =========================================================

def ask_openai(prompt):
    """
    Send a text-only prompt to OpenAI.
    """

    try:

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt
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


# =========================================================
# BACKWARD COMPATIBILITY
# =========================================================

def ask_gemini(prompt):
    """
    Compatibility wrapper.

    Existing StyleSense modules may still call
    ask_gemini(). Instead of Gemini, the request
    is now handled by OpenAI.

    This means we don't have to rewrite every
    existing file immediately.
    """

    return ask_openai(prompt)


# =========================================================
# IMAGE AI
# =========================================================

def ask_openai_vision(prompt, image_data):
    """
    Send text + image to OpenAI.

    image_data should be a data URL such as:

    data:image/jpeg;base64,....
    """

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
            ]
        )

        if response.output_text:

            return response.output_text

        return (
            "❌ OpenAI returned an empty image analysis."
        )

    except Exception as e:

        st.error(
            f"❌ OpenAI Vision Error: "
            f"{type(e).__name__}: {e}"
        )

        return None


# =========================================================
# OUTFIT IMAGE ANALYZER
# =========================================================

def analyze_outfit(image):
    """
    Analyze an uploaded outfit image using OpenAI vision.
    """

    try:

        # -------------------------------------------------
        # CONVERT INPUT TO PIL IMAGE
        # -------------------------------------------------

        if not isinstance(image, Image.Image):

            image = Image.open(image)


        # -------------------------------------------------
        # RGB
        # -------------------------------------------------

        if image.mode != "RGB":

            image = image.convert("RGB")


        # -------------------------------------------------
        # RESIZE LARGE IMAGE
        # -------------------------------------------------

        max_size = 1600

        if max(image.size) > max_size:

            image.thumbnail(
                (max_size, max_size),
                Image.Resampling.LANCZOS
            )


        # -------------------------------------------------
        # CONVERT TO JPEG
        # -------------------------------------------------

        image_bytes = io.BytesIO()

        image.save(
            image_bytes,
            format="JPEG",
            quality=90
        )

        image_bytes = image_bytes.getvalue()


        # -------------------------------------------------
        # BASE64
        # -------------------------------------------------

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")


        image_data = (
            "data:image/jpeg;base64,"
            + image_base64
        )


        # -------------------------------------------------
        # FASHION ANALYSIS PROMPT
        # -------------------------------------------------

        prompt = """
You are an expert fashion stylist, fashion designer,
fashion consultant, and fashion image analyst for
StyleSense AI OS.

Analyze the ACTUAL outfit visible in the uploaded image.

The image is already attached.

IMPORTANT:

Do NOT ask the user to upload another image.

Do NOT say that the image is missing.

Do NOT pretend that you cannot see the image.

Base your analysis ONLY on what is visibly present.

Do not invent:

- brands
- exact fabric composition
- prices
- measurements
- clothing pieces that are not visible
- accessories that are not visible

Analyze:

- clothing pieces
- silhouette
- fit
- proportions
- colors
- patterns
- fabric appearance
- footwear
- accessories
- layering
- styling
- color coordination
- overall aesthetic

Return EXACTLY these sections:

# Style

Describe the overall style and aesthetic of the outfit.

# Strengths

Explain what works particularly well.

# Weaknesses

Explain what could be improved.

# Color Harmony

Analyze how the colors work together.

# Accessories

Analyze the visible accessories and recommend
appropriate additions where useful.

# Improvement Suggestions

Give practical suggestions for improving the outfit,
including fit, proportions, colors, footwear,
accessories, or styling.

Be specific, practical, and honest.
"""


        # -------------------------------------------------
        # SEND IMAGE TO OPENAI
        # -------------------------------------------------

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