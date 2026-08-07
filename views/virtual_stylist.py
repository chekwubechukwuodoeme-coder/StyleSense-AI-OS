import streamlit as st

from ai import fashion_chat


def render_virtual_stylist():

    st.header("👔 AI Virtual Stylist")

    event = st.selectbox(
        "Event",
        [
            "Wedding",
            "Office",
            "Date",
            "Party",
            "Church",
            "Graduation",
            "Birthday",
            "Photoshoot"
        ]
    )

    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female"
        ]
    )

    age = st.slider(
        "Age",
        15,
        70,
        25
    )

    skin = st.selectbox(
        "Skin Tone",
        [
            "Fair",
            "Brown",
            "Dark Brown",
            "Deep Black"
        ]
    )

    budget = st.selectbox(
        "Budget",
        [
            "₦50,000",
            "₦100,000",
            "₦200,000",
            "₦500,000",
            "Unlimited"
        ]
    )

    weather = st.selectbox(
        "Weather",
        [
            "Hot",
            "Cold",
            "Rainy"
        ]
    )

    if st.button(
        "Generate My Style",
        use_container_width=True
    ):

        prompt = f"""
You are the world's best celebrity stylist.

Create a complete styling recommendation.

Event:
{event}

Gender:
{gender}

Age:
{age}

Skin Tone:
{skin}

Budget:
{budget}

Weather:
{weather}

Return:

# Outfit

# Fabric

# Colors

# Shoes

# Accessories

# Hairstyle

# Fragrance

# Estimated Cost

# Styling Tips

Use beautiful Markdown.
"""

        with st.spinner("Creating your personalized style..."):

            answer = fashion_chat(prompt)

        st.success("Your style guide is ready!")

        st.markdown(answer)