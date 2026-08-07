import streamlit as st

from database.projects import (
    create_project,
    get_projects,
    delete_project
)

def render_projects():

    st.title("📂 Projects")

    st.subheader("Create New Project")

    title = st.text_input("Project Name")

    description = st.text_area("Description")

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

    if st.button("Create Project"):

        if title.strip():

            create_project(
                title,
                description,
                category
            )

            st.success("Project created successfully!")

            st.rerun()

    st.divider()

    st.subheader("Your Projects")

    projects = get_projects()

    if not projects:

        st.info("No projects yet.")

        return

    for project in projects:

        project_id, title, description, category, created = project

        with st.container(border=True):

            st.subheader(title)

            st.caption(category)

            st.write(description)

            col1, col2 = st.columns(2)

            with col1:

                st.button(
                    "Open",
                    key=f"open_{project_id}"
                )

            with col2:

                if st.button(
                    "Delete",
                    key=f"delete_{project_id}"
                ):

                    delete_project(project_id)

                    st.rerun()