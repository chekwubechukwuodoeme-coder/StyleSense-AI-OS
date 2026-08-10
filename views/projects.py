import streamlit as st

from database.projects import (
    create_project,
    get_projects,
    delete_project
)


def render_projects():

    st.title("📂 Projects")

    st.subheader("Create New Project")

    # ==========================
    # CREATE PROJECT
    # ==========================

    title = st.text_input(
        "Project Name",
        key="project_name"
    )

    description = st.text_area(
        "Description",
        key="project_description"
    )

    category = st.selectbox(
        "Category",
        [
            "Luxury",
            "Wedding",
            "Streetwear",
            "Corporate",
            "Native Wear"
        ],
        key="project_category"
    )

    if st.button(
        "Create Project",
        type="primary",
        key="create_project_button"
    ):

        if not title.strip():

            st.error("Please enter a project name.")

        else:

            create_project(
                title.strip(),
                description.strip(),
                category
            )

            st.success(
                f"Project '{title}' created successfully!"
            )

            # Clear inputs
            st.session_state.project_name = ""
            st.session_state.project_description = ""

            st.rerun()

    st.divider()

    # ==========================
    # PROJECT LIST
    # ==========================

    st.subheader("Your Projects")

    projects = get_projects()

    if not projects:

        st.info(
            "No projects yet. Create your first project above."
        )

        return

    # ==========================
    # DISPLAY PROJECTS
    # ==========================

    for project in projects:

        project_id = project[0]
        project_title = project[1]
        project_description = project[2]
        project_category = project[3]
        project_created = project[4]

        with st.container(border=True):

            st.subheader(
                f"📁 {project_title}"
            )

            st.caption(
                f"Category: {project_category}"
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

            # ==========================
            # OPEN
            # ==========================

            with col1:

                if st.button(
                    "🚀 Open Project",
                    key=f"open_project_{project_id}",
                    use_container_width=True
                ):

                    # Save selected project
                    st.session_state.current_project = {
                        "id": project_id,
                        "title": project_title,
                        "description": project_description,
                        "category": project_category,
                        "created_at": project_created
                    }

                    # Tell app to show workspace
                    st.session_state.current_page = "🖥 Workspace"

                    st.rerun()

            # ==========================
            # DELETE
            # ==========================

            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_project_{project_id}",
                    use_container_width=True
                ):

                    delete_project(
                        project_id
                    )

                    # If deleted project was open
                    if (
                        st.session_state.get(
                            "current_project"
                        )
                        and
                        st.session_state.current_project.get(
                            "id"
                        ) == project_id
                    ):

                        st.session_state.current_project = None

                    st.success(
                        "Project deleted."
                    )

                    st.rerun()