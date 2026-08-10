import os
import requests
import streamlit as st
from dotenv import load_dotenv

from ai.model import ask_gemini


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_API_URL = "https://newsapi.org/v2/everything"


# ============================================================
# CHECK WHETHER AN ARTICLE IS ACTUALLY FASHION NEWS
# ============================================================

def is_fashion_article(article):
    """
    Uses Gemini to determine whether an article is genuinely
    about fashion.

    The important rule is that fashion must be the PRIMARY
    SUBJECT of the article, not just something mentioned
    somewhere in the article.
    """

    title = article.get("title") or ""
    description = article.get("description") or ""
    content = article.get("content") or ""

    prompt = f"""
You are the chief editor of a professional fashion news platform
called StyleSense AI OS.

Your job is to decide whether the following article belongs in
the platform's FASHION NEWS section.

==================================================
ARTICLE
==================================================

TITLE:
{title}

DESCRIPTION:
{description}

CONTENT:
{content}

==================================================
PRIMARY SUBJECT RULE
==================================================

Classify the article according to its PRIMARY SUBJECT.

An article should be classified as FASHION only when fashion is
one of the MAIN subjects of the article.

Do NOT classify an article as fashion simply because the article
mentions a fashion designer, clothing, a dress, style, a model,
Vogue, or another fashion-related word.

The article must substantially focus on the fashion industry
or fashion itself.

==================================================
FASHION ARTICLES INCLUDE
==================================================

Examples include articles primarily about:

- Fashion designers
- Fashion houses
- Fashion brands
- Clothing brands
- New clothing collections
- Haute couture
- Couture
- Runway shows
- Fashion weeks
- Fashion trends
- Apparel
- Garments
- Textiles
- Fashion retail
- Fashion business
- Fashion industry developments
- Streetwear
- Menswear
- Womenswear
- Footwear
- Handbags
- Jewelry when discussed primarily as fashion
- Fashion accessories
- Fashion models
- Modeling campaigns
- Fashion photography
- Designer collaborations
- Fashion exhibitions
- Fashion awards
- Fashion events
- Celebrity fashion when the article is primarily about
  the celebrity's fashion, outfit, designer look, or style

==================================================
NON-FASHION ARTICLES
==================================================

Return NOT_FASHION when the primary subject is:

- Sports
- Baseball
- Football
- Basketball
- Politics
- Elections
- Government
- Movies
- Film
- Television
- Music
- Albums
- Songs
- General celebrity news
- Theater
- Books
- Crime
- Technology
- Science
- Health
- Business unrelated to fashion
- General entertainment
- History unrelated to fashion
- Weather
- Travel
- Food
- Religion
- Education
- General lifestyle

==================================================
IMPORTANT EXAMPLES
==================================================

EXAMPLE 1:

Title:
"Dior unveils its latest haute couture collection"

Classification:
FASHION

Reason:
The primary subject is a fashion collection.

--------------------------------------------------

EXAMPLE 2:

Title:
"Louis Vuitton announces new creative director"

Classification:
FASHION

Reason:
The primary subject is a fashion house and its creative
direction.

--------------------------------------------------

EXAMPLE 3:

Title:
"Judy Holliday's rise from cabaret performer to Hollywood star"

Article contains:
"Main Bocher, the American fashion designer..."

Classification:
NOT_FASHION

Reason:
The article is primarily about Judy Holliday's career and
Hollywood history. The fashion designer is only mentioned
incidentally.

--------------------------------------------------

EXAMPLE 4:

Title:
"Dodgers overcome blown Edwin Diaz save to end losing streak"

Classification:
NOT_FASHION

Reason:
The article is about baseball.

--------------------------------------------------

EXAMPLE 5:

Title:
"Taylor Swift stuns in a custom Dior gown at the awards"

Classification:
FASHION

Reason:
The primary subject is her fashion look and designer gown.

--------------------------------------------------

EXAMPLE 6:

Title:
"Taylor Swift announces her new album"

Classification:
NOT_FASHION

Reason:
The primary subject is music.

--------------------------------------------------

EXAMPLE 7:

Title:
"Actor wins Best Actor award at international film festival"

Classification:
NOT_FASHION

Reason:
The primary subject is film.

Even if the article describes what the actor was wearing,
it remains a film article unless fashion itself is a major
subject.

--------------------------------------------------

EXAMPLE 8:

Title:
"Zendaya's best red carpet fashion moments"

Classification:
FASHION

Reason:
The primary subject is fashion and red-carpet style.

==================================================
THE REMOVAL TEST
==================================================

Ask yourself:

"If I removed the fashion-related sentence from this article,
would the article still fundamentally be about something else?"

If YES:
Return NOT_FASHION.

If NO:
Return FASHION.

==================================================
VERY IMPORTANT
==================================================

Do not classify an article as FASHION merely because it contains
one or more of these words:

designer
fashion
style
model
dress
clothing
Vogue
luxury
runway
collection

These words may appear in non-fashion articles.

Look at the overall subject.

==================================================
FINAL RESPONSE
==================================================

Return ONLY ONE of these two values:

FASHION

NOT_FASHION
"""

    try:

        result = ask_gemini(prompt)

        if not result:
            return False

        result = result.strip().upper()

        # Only an exact FASHION response is accepted.
        if result == "FASHION":
            return True

        return False

    except Exception as e:

        # If Gemini cannot classify the article,
        # reject it rather than accidentally displaying
        # non-fashion news.
        print(
            f"Fashion classification error: {e}"
        )

        return False


# ============================================================
# GET FASHION NEWS
# ============================================================

def get_fashion_news():

    if not NEWS_API_KEY:

        raise ValueError(
            "❌ NEWS_API_KEY not found."
        )

    # ========================================================
    # NEWSAPI SEARCH
    # ========================================================

    params = {

        "q": (
            '"fashion" OR '
            '"fashion industry" OR '
            '"fashion designer" OR '
            '"fashion brand" OR '
            '"fashion house" OR '
            '"fashion week" OR '
            '"fashion collection" OR '
            '"fashion show" OR '
            '"haute couture" OR '
            '"couture" OR '
            '"runway" OR '
            '"apparel" OR '
            '"textile" OR '
            '"clothing" OR '
            '"streetwear" OR '
            '"menswear" OR '
            '"womenswear" OR '
            '"luxury fashion" OR '
            '"designer collection" OR '
            '"red carpet fashion"'
        ),

        "language": "en",

        "sortBy": "publishedAt",

        # Get more articles because Gemini will filter them.
        "pageSize": 50,

        "apiKey": NEWS_API_KEY,
    }

    # ========================================================
    # REQUEST NEWSAPI
    # ========================================================

    try:

        response = requests.get(
            NEWS_API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as e:

        st.error(
            f"❌ News API Error: {e}"
        )

        return []

    # ========================================================
    # GET ARTICLES
    # ========================================================

    articles = data.get(
        "articles",
        []
    )

    if not articles:

        return []

    # ========================================================
    # FILTER ARTICLES
    # ========================================================

    fashion_articles = []

    seen_urls = set()

    for article in articles:

        # ----------------------------------------------------
        # Skip articles without a URL
        # ----------------------------------------------------

        article_url = article.get("url")

        if not article_url:
            continue

        # ----------------------------------------------------
        # Remove duplicate articles
        # ----------------------------------------------------

        if article_url in seen_urls:
            continue

        seen_urls.add(article_url)

        # ----------------------------------------------------
        # Make sure the article has useful text
        # ----------------------------------------------------

        title = article.get("title") or ""
        description = article.get("description") or ""

        if not title.strip():

            continue

        # ----------------------------------------------------
        # Ask Gemini whether this is REALLY fashion news
        # ----------------------------------------------------

        if is_fashion_article(article):

            fashion_articles.append(article)

        # ----------------------------------------------------
        # Stop after collecting 20 valid fashion articles
        # ----------------------------------------------------

        if len(fashion_articles) >= 20:

            break

    return fashion_articles