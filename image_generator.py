import os
import base64
import io

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise Exception("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=API_KEY)


# ============================================================
# NORMAL IMAGE GENERATION
# ============================================================

def generate_image(prompt):

    try:

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_bytes = base64.b64decode(
            result.data[0].b64_json
        )

        return image_bytes

    except Exception as e:

        raise Exception(
            f"OpenAI Image Error: {e}"
        )


# ============================================================
# REFERENCE IMAGE → NEW DESIGN
# ============================================================

def generate_image_from_reference(
    image_file,
    prompt
):

    try:

        # ----------------------------------------------------
        # Read uploaded Streamlit file
        # ----------------------------------------------------

        image_bytes = image_file.getvalue()

        # ----------------------------------------------------
        # Convert to an in-memory file
        # ----------------------------------------------------

        image_buffer = io.BytesIO(
            image_bytes
        )

        image_buffer.name = (
            image_file.name
            if hasattr(image_file, "name")
            else "reference.png"
        )

        # ----------------------------------------------------
        # OpenAI Image Edit
        # ----------------------------------------------------

        result = client.images.edit(
            model="gpt-image-1",
            image=image_buffer,
            prompt=prompt,
            size="1024x1024"
        )

        # ----------------------------------------------------
        # Decode generated image
        # ----------------------------------------------------

        generated_image = base64.b64decode(
            result.data[0].b64_json
        )

        return generated_image

    except Exception as e:

        raise Exception(
            f"OpenAI Reference Image Error: {e}"
        )