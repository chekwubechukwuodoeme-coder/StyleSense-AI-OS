from google import genai
from config import GEMINI_API_KEY

if not GEMINI_API_KEY:
    raise ValueError(
        "❌ GEMINI_API_KEY not found."
    )

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-3.5-flash-lite"


def ask_gemini(prompt: str) -> str:
    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if response.text:
            return response.text

        return "⚠️ Empty response returned."

    except Exception as e:

        return f"""
# ⚠️ AI Service Error

Reason:

{e}
"""