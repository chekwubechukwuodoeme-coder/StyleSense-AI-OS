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
    # CREATE PROJECT FORM
    # ==========================

    with st.form("create_project_form", clear_on_submit=True):

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
                "Native Wear"
            ]
        )

        submitted = st.form_submit_button(
            "🚀 Create Project",
            type="primary",
            use_container_width=True
        )

    # ==========================
    # CREATE PROJECT
    # ==========================

    if submitted:

        if not title.strip():

            st.error("Please enter a project name.")

        else:

            create_project(
                title.strip(),
                description.strip(),
                category
            )

            st.success(
                f"Project '{title.strip()}' created successfully!"
            )

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
            # OPEN PROJECT
            # ==========================

            with col1:

                if st.button(
                    "🚀 Open Project",
                    key=f"open_project_{project_id}",
                    use_container_width=True
                ):

                    st.session_state.current_project = {
                        "id": project_id,
                        "title": project_title,
                        "description": project_description,
                        "category": project_category,
                        "created_at": project_created
                    }

                    # Tell app to open workspace
                    st.session_state.open_workspace = True

                    st.rerun()

            # ==========================
            # DELETE PROJECT
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

                    # Clear current project if
                    # the deleted project was open
                    current_project = st.session_state.get(
                        "current_project"
                    )

                    if (
                        current_project
                        and current_project.get("id") == project_id
                    ):

                        st.session_state.current_project = None

                    st.rerun()