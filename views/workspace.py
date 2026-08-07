import streamlit as st

from ai.ceo import ceo_agent


def render_workspace():

    st.title("🧠 AI Workspace")

    project = st.session_state.get(
        "current_project",
        {
            "title": "No Project Selected"
        }
    )

    st.subheader(project["title"])

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "💬 CEO",
            "👥 Departments",
            "📂 Files",
            "📋 Tasks",
            "📊 Reports"
        ]
    )

    # ==========================
    # CEO WORKSPACE
    # ==========================

    with tab1:

        st.subheader("👔 CEO Workspace")

        task = st.chat_input(
            "Give the CEO a mission..."
        )

        if task:

            st.success("Mission Received")

            progress = st.progress(0)

            status = st.empty()

            status.info("👔 CEO is coordinating the AI team...")

            progress.progress(25)

            result = ceo_agent(task)

            progress.progress(100)

            status.success("✅ Executive report completed.")

            st.markdown(result)

    # ==========================
    # AI DEPARTMENTS
    # ==========================

    with tab2:

        st.subheader("👥 AI Departments")

        st.success("👔 CEO")

        st.success("👗 Designer")

        st.success("💼 Business")

        st.success("📢 Marketing")

        st.success("💰 Finance")

        st.success("🏭 Production")

        st.success("🔍 Research")

        st.success("📈 Trend")

        st.success("👔 Stylist")

    # ==========================
    # PROJECT FILES
    # ==========================

    with tab3:

        st.info(
            "Project files will appear here."
        )

    # ==========================
    # TASKS
    # ==========================

    with tab4:

        st.info(
            "CEO generated tasks will appear here."
        )

    # ==========================
    # REPORTS
    # ==========================

    with tab5:

        st.info(
            "Executive reports will appear here."
        )