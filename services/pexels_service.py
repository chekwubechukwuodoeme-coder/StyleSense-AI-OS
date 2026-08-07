import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")

URL = "https://api.pexels.com/v1/search"


def search_fashion_images(query, per_page=15):

    headers = {
        "Authorization": API_KEY
    }

    params = {
        "query": query,
        "per_page": per_page,
        "orientation": "portrait"
    }

    response = requests.get(
        URL,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    images = []

    for photo in data.get("photos", []):

        images.append({
            "id": photo["id"],
            "title": photo.get("alt", "Fashion"),
            "photographer": photo["photographer"],
            "url": photo["src"]["large"],
            "original": photo["src"]["original"]
        })

    return images