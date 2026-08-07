import streamlit as st

from ai import fashion_chat


def render_color_matcher():

    st.header("🎨 AI Color Matcher")

    color = st.selectbox(
        "Choose Main Color",
        [
            "Black",
            "White",
            "Gold",
            "Red",
            "Blue",
            "Green"
        ]
    )

    if st.button(
        "Generate Matches",
        use_container_width=True
    ):

        prompt = f"""
You are a luxury fashion color consultant.

The customer's primary color is:

{color}

Recommend:

# Best Matching Colors

# Luxury Outfit Ideas

# Matching Fabrics

# Shoe Recommendations

# Accessories

# Suitable Skin Tones

# Color Psychology

# Celebrity Inspiration

Use beautiful Markdown.
"""

        with st.spinner("Finding the best color combinations..."):

            answer = fashion_chat(prompt)

        st.success("Color combinations generated!")

        st.markdown(answer)