import streamlit as st

from ai import fashion_chat


def render_fashion_magazine():

    st.header("📰 AI Fashion Magazine")

    category = st.selectbox(
        "Choose Category",
        [
            "Today's Trends",
            "Celebrity Fashion",
            "Luxury Brands",
            "African Fashion",
            "Street Style",
            "Fashion Business",
            "Editor's Picks"
        ]
    )

    if st.button(
        "Generate Magazine",
        use_container_width=True
    ):

        prompt = f"""
You are the editor-in-chief of a world-class fashion magazine.

Create today's fashion magazine for:

{category}

Include:

# Cover Story

# Latest Trends

# Celebrity Looks

# Designer Spotlight

# Styling Tips

# Must-Have Items

# Fashion Business

# AI Fashion Innovations

# Editor's Advice

Use professional Markdown formatting.
"""

        with st.spinner("Creating today's magazine..."):

            article = fashion_chat(prompt)

        st.success("Magazine generated!")

        st.markdown(article)