import streamlit as st

from ai import fashion_chat


def render_fashion_trends():

    st.header("🔥 AI Fashion Trends")

    region = st.selectbox(
        "Region",
        [
            "Global",
            "Africa",
            "Nigeria",
            "Europe",
            "USA"
        ]
    )

    season = st.selectbox(
        "Season",
        [
            "Spring",
            "Summer",
            "Autumn",
            "Winter",
            "All Season"
        ]
    )

    if st.button(
        "Generate Fashion Trends",
        use_container_width=True
    ):

        prompt = f"""
You are one of the world's best fashion trend forecasters.

Analyze the latest trends.

Region:
{region}

Season:
{season}

Return:

# Trending Colors

# Trending Outfits

# Trending Fabrics

# Trending Shoes

# Trending Accessories

# Trending Hairstyles

# Celebrity Inspiration

# Luxury Fashion Brands

# Fashion Prediction For Next Month

# Business Opportunities

Use beautiful Markdown.
"""

        with st.spinner("Analyzing fashion trends..."):

            trends = fashion_chat(prompt)

        st.success("Trend report generated!")

        st.markdown(trends)