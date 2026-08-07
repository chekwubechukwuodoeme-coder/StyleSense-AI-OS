import streamlit as st

from database.dashboard import (
    count_projects,
    count_designers,
    count_missions
)


def render_dashboard():

    st.title("👗 StyleSense AI OS")

    st.subheader("Your AI Fashion Operating System")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Projects",
            count_projects()
        )

    with col2:

        st.metric(
            "Designs",
            len(st.session_state.saved_designs)
        )

    with col3:

        st.metric(
            "Designers",
            count_designers()
        )

    with col4:

        st.metric(
            "AI Missions",
            count_missions()
        )

    st.divider()

    st.subheader("🚀 AI Modules")

    col1, col2 = st.columns(2)

    with col1:

        st.success("✅ AI Design Studio")

        st.success("✅ AI Design Editor")

        st.success("✅ Fashion Assistant")

        st.success("✅ Outfit Analyzer")

        st.success("✅ Logo Generator")

        st.success("✅ Fabric Advisor")

        st.success("✅ Color Matcher")

        st.success("✅ AI Virtual Stylist")

    with col2:

        st.success("✅ Fashion News")

        st.success("✅ Fashion Magazine")

        st.success("✅ Fashion Trends")

        st.success("✅ Design Library")

        st.success("✅ Find Designers")

        st.success("✅ Workspace")

        st.success("✅ Projects")

    st.divider()

    st.subheader("📊 Current Session")

    st.write(
        f"**Saved Designs:** {len(st.session_state.saved_designs)}"
    )

    st.write(
        f"**Chat Messages:** {len(st.session_state.messages)}"
    )

    st.divider()

    st.info(
        """
Welcome to **StyleSense AI OS**.

This platform helps fashion designers, brands, entrepreneurs, and creators:

- 👗 Generate fashion collections
- 🤖 Chat with AI specialists
- 🏢 Build fashion businesses
- 📈 Analyze trends
- 🎨 Create logos
- 📚 Organize projects
- 🧵 Get fabric recommendations
- 👔 Receive styling advice
- 📰 Read fashion news
- 🔥 Forecast fashion trends
"""
    )