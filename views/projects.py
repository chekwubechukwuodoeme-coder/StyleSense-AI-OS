import streamlit as st

from database.projects import (
    create_project,
    get_projects,
    delete_project
)


def render_projects():

    st.title("📂 Projects")

    st.caption(
        "Create and manage your fashion projects."
    )

    st.divider()

    user_id = st.session_state.get(
        "user_id"
    )

    # ========================================================
    # CREATE PROJECT
    # ========================================================

    st.subheader("Create New Project")

    with st.form(
        "create_project_form",
        clear_on_submit=True
    ):

        title = st.text_input(
            "Project Name",
            placeholder="e.g. Chekwube Empire"
        )

        description = st.text_area(
            "Description",
            placeholder="Describe your fashion project..."
        )

        category = st.selectbox(
            "Category",
            [
                "Luxury",
                "Wedding",
                "Streetwear",
                "Corporate",
                "Native Wear",
                "Ready-to-Wear",
                "Sportswear",
                "Other"
            ]
        )

        submitted = st.form_submit_button(
            "🚀 Create Project",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if not title.strip():

            st.error(
                "Please enter a project name."
            )

        else:

            create_project(
                title=title,
                description=description,
                category=category,
                user_id=user_id
            )

            st.success(
                f"Project '{title.strip()}' created successfully!"
            )

            st.rerun()

    st.divider()

    # ========================================================
    # YOUR PROJECTS
    # ========================================================

    st.subheader("Your Projects")

    projects = get_projects(
        user_id=user_id
    )

    if not projects:

        st.info(
            "No projects yet. Create your first project above."
        )

        return

    # ========================================================
    # PROJECTS
    # ========================================================

    for project in projects:

        (
            project_id,
            project_user_id,
            project_title,
            project_description,
            project_category,
            project_cover,
            project_created
        ) = project

        with st.container(
            border=True
        ):

            st.subheader(
                f"📁 {project_title}"
            )

            st.caption(
                f"🏷️ {project_category}"
            )

            if project_description:

                st.write(
                    project_description
                )

            else:

                st.caption(
                    "No description provided."
                )

            st.caption(
                f"Created: {project_created}"
            )

            col1, col2 = st.columns(2)

            # ------------------------------------------------
            # OPEN
            # ------------------------------------------------

            with col1:

                if st.button(
                    "🚀 Open Project",
                    key=f"projects_open_{project_id}",
                    use_container_width=True
                ):

                    st.session_state.current_project = {

                        "id": project_id,

                        "user_id": project_user_id,

                        "title": project_title,

                        "description": project_description,

                        "category": project_category,

                        "cover_image": project_cover,

                        "created_at": project_created
                    }

                    st.session_state.open_workspace = True

                    st.session_state.main_navigation = (
                        "Workspace"
                    )

                    st.rerun()

            # ------------------------------------------------
            # DELETE
            # ------------------------------------------------

            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"projects_delete_{project_id}",
                    use_container_width=True
                ):

                    delete_project(
                        project_id,
                        user_id=user_id
                    )

                    current_project = (
                        st.session_state.get(
                            "current_project"
                        )
                    )

                    if (
                        current_project
                        and current_project.get("id")
                        == project_id
                    ):

                        st.session_state.current_project = None

                        st.session_state.open_workspace = False

                    st.success(
                        "Project deleted."
                    )

                    st.rerun()