import streamlit as st

from services.news_service import get_fashion_news


# ============================================================
# SESSION STATE
# ============================================================

if "fashion_news_articles" not in st.session_state:
    st.session_state.fashion_news_articles = []

if "fashion_news_generated" not in st.session_state:
    st.session_state.fashion_news_generated = False


# ============================================================
# RENDER FASHION NEWS
# ============================================================

def render_fashion_news():

    st.header("📰 Today's Fashion News")

    st.caption(
        "Latest fashion industry news, designers, brands, trends, "
        "collections and style."
    )

    st.divider()

    # ========================================================
    # GENERATE / REFRESH NEWS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔄 Get Latest Fashion News",
            use_container_width=True
        ):

            with st.spinner(
                "Finding the latest fashion news..."
            ):

                try:

                    articles = get_fashion_news()

                    if articles:

                        st.session_state.fashion_news_articles = (
                            articles
                        )

                        st.session_state.fashion_news_generated = (
                            True
                        )

                        st.success(
                            f"Found {len(articles)} fashion articles."
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "No fashion news is available at the moment."
                        )

                except Exception as e:

                    st.error(
                        f"Unable to load fashion news: {e}"
                    )

    with col2:

        if st.session_state["fashion_news_articles"]:

            if st.button(
                "🗑️ Clear News",
                use_container_width=True
            ):

                st.session_state.fashion_news_articles = []

                st.session_state.fashion_news_generated = (
                    False
                )

                st.rerun()

    # ========================================================
    # GET SAVED NEWS
    # ========================================================

    articles = st.session_state["fashion_news_articles"]
    
    # ========================================================
    # FIRST VISIT
    # ========================================================

    if not articles:

        st.info(
            """
            📰 No fashion news has been loaded yet.

            Click **🔄 Get Latest Fashion News** to load the
            latest fashion industry stories.
            """
        )

        return

    # ========================================================
    # NEWS STATUS
    # ========================================================

    st.success(
        f"🟢 {len(articles)} fashion articles loaded."
    )

    st.caption(
        "Your news is saved for this session. "
        "You can visit other pages and return without generating again."
    )

    st.divider()

    # ========================================================
    # DISPLAY ARTICLES
    # ========================================================

    for index, article in enumerate(articles):

        # ====================================================
        # ARTICLE DATA
        # ====================================================

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

        source = article.get(
            "source",
            {}
        )

        if isinstance(source, dict):

            source_name = source.get(
                "name",
                "Fashion News"
            )

        else:

            source_name = "Fashion News"

        published_at = article.get(
            "publishedAt",
            ""
        )

        # ====================================================
        # ARTICLE CARD
        # ====================================================

        with st.container(border=True):

            st.subheader(
                title
            )

            # ------------------------------------------------
            # SOURCE
            # ------------------------------------------------

            meta_col1, meta_col2 = st.columns(2)

            with meta_col1:

                st.caption(
                    f"📰 {source_name}"
                )

            with meta_col2:

                if published_at:

                    st.caption(
                        f"📅 {published_at}"
                    )

            # ------------------------------------------------
            # IMAGE
            # ------------------------------------------------

            if image_url:

                try:

                    st.image(
                        image_url,
                        use_container_width=True
                    )

                except Exception:

                    pass

            # ------------------------------------------------
            # DESCRIPTION
            # ------------------------------------------------

            if description:

                st.write(
                    description
                )

            # ------------------------------------------------
            # READ ARTICLE
            # ------------------------------------------------

            if article_url:

                st.link_button(
                    "📖 Read Full Article",
                    article_url,
                    use_container_width=True
                )

        st.write("")