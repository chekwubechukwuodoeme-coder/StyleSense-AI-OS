import streamlit as st

from ai import fashion_chat


def render_fabric_advisor():

    st.header("🧵 Fabric Advisor")

    event = st.selectbox(
        "Event",
        [
            "Wedding",
            "Office",
            "School",
            "Party",
            "Church",
            "Outing"
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

    budget = st.selectbox(
        "Budget",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    if st.button(
        "Recommend Fabric",
        use_container_width=True
    ):

        prompt = f"""
You are a world-class textile expert.

Recommend the best fabric.

Event:
{event}

Weather:
{weather}

Budget:
{budget}

Return:

# Recommended Fabric

# Why It Fits

# Advantages

# Color Suggestions

# Care Instructions

# Estimated Cost

# Luxury Alternative
"""

        with st.spinner("Analyzing fabrics..."):

            answer = fashion_chat(prompt)

        st.success("Recommendation ready!")

        st.markdown(answer)