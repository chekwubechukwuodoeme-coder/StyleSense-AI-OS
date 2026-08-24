import streamlit as st

from ai.ceo import ceo_agent


def render_workspace():

    # ==========================
    # CHECK PROJECT
    # ==========================

    project = st.session_state.get(
        "current_project"
    )

    if project is None:

        st.warning(
            "No project is currently open."
        )

        if st.button(
            "← Go to Projects",
            key="workspace_no_project_back"
        ):

            st.session_state.main_navigation = "Projects"

            st.rerun()

        return

    # ==========================
    # BACK BUTTON
    # ==========================

    if st.button(
        "← Back to Projects",
        key="back_to_projects"
    ):

        st.session_state.current_project = None

        st.session_state.open_workspace = False

        st.session_state.main_navigation = "Projects"


        st.rerun()

    # ==========================
    # WORKSPACE HEADER
    # ==========================

    st.title("🧠 AI Workspace")

    st.subheader(
        f"📁 {project['title']}"
    )

    st.caption(
        f"Category: {project.get('category', 'N/A')}"
    )

    if project.get("description"):

        st.write(
            project["description"]
        )

    st.divider()

    # ==========================
    # WORKSPACE TABS
    # ==========================

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
    # CEO
    # ==========================

    with tab1:

        st.subheader(
            "👔 CEO Workspace"
        )

        st.write(
            f"The CEO is working on: **{project['title']}**"
        )

        task = st.chat_input(
            "Give the CEO a mission..."
        )

        if task:

            st.success(
                "Mission Received"
            )

            progress = st.progress(0)

            status = st.empty()

            status.info(
                "👔 CEO is coordinating the AI team..."
            )

            progress.progress(25)

            try:

                result = ceo_agent(
                    task
                )

                progress.progress(100)

                status.success(
                    "✅ Executive report completed."
                )

                st.markdown(
                    result
                )

            except Exception as e:

                progress.empty()

                status.error(
                    "❌ CEO encountered an error."
                )

                st.exception(e)

    # ==========================
    # DEPARTMENTS
    # ==========================

    with tab2:

        st.subheader(
            "👥 AI Departments"
        )

        departments = [
            "👔 CEO",
            "👗 Designer",
            "💼 Business",
            "📢 Marketing",
            "💰 Finance",
            "🏭 Production",
            "🔍 Research",
            "📈 Trend",
            "👔 Stylist"
        ]

        for department in departments:

            st.success(
                department
            )

    # ==========================
    # FILES
    # ==========================

    with tab3:

        st.subheader(
            "📂 Project Files"
        )

        st.info(
            "Project files will appear here."
        )

    # ==========================
    # TASKS
    # ==========================

    with tab4:

        st.subheader(
            "📋 Project Tasks"
        )

        st.info(
            "CEO generated tasks will appear here."
        )

    # ==========================
    # REPORTS
    # ==========================

    with tab5:

        st.subheader(
            "📊 Project Reports"
        )

        st.info(
            "Executive reports will appear here."
        )