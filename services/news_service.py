import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

URL = "https://newsapi.org/v2/everything"


def get_fashion_news():

    params = {
        "q": "fashion OR luxury fashion OR celebrity style OR vogue",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()

    return response.json()["articles"]