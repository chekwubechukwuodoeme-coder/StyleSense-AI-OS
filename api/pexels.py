import requests
from config import PEXELS_API_KEY

URL = "https://api.pexels.com/v1/search"


def search_fashion(query, per_page=30):

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": per_page
    }

    response = requests.get(
        URL,
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        return response.json()["photos"]

    return []