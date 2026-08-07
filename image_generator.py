import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise Exception("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=API_KEY)


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
        raise Exception(f"OpenAI Image Error: {e}")