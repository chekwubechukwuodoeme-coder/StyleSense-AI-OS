import streamlit as st

from services.news_service import get_fashion_news


def render_fashion_news():

    st.header("📰 Today's Fashion News")

    st.caption(
        "Latest fashion industry news, designers, brands, trends, "
        "collections and style."
    )

    with st.spinner(
        "Finding the latest fashion news..."
    ):

        articles = get_fashion_news()

    if not articles:

        st.warning(
            "No fashion news is available at the moment."
        )

        return

    st.success(
        f"Found {len(articles)} fashion articles."
    )

    st.divider()

    for article in articles:

        title = article.get(
            "title",
            "Untitled"
        )

        description = article.get(
            "description",
            "No description available."
        )

        image_url = article.get(
            "urlToImage"
        )

        article_url = article.get(
            "url"
        )

        # ====================================================
        # ARTICLE CARD
        # ====================================================

        with st.container(border=True):

            st.subheader(title)

            if image_url:

                try:

                    st.image(
                        image_url,
                        use_container_width=True
                    )

                except Exception:

                    pass

            if description:

                st.write(description)

            if article_url:

                st.link_button(
                    "📖 Read Full Article",
                    article_url,
                    use_container_width=True
                )

        st.write("")