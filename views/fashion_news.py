import streamlit as st

from services.news_service import get_fashion_news


def render_fashion_news():

    st.header("📰 Today's Fashion News")

    with st.spinner("Loading latest fashion news..."):

        articles = get_fashion_news()

    if not articles:
        st.warning("No news available at the moment.")
        return

    for article in articles:

        st.subheader(article["title"])

        if article.get("urlToImage"):
            st.image(
                article["urlToImage"],
                use_container_width=True
            )

        st.write(
            article.get(
                "description",
                "No description available."
            )
        )

        st.link_button(
            "📖 Read Full Article",
            article["url"],
            use_container_width=True
        )

        st.divider()