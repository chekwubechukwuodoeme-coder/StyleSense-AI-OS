import streamlit as st


def render_production_manager():

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("🏭 Production Manager")

    st.caption(
        "Manage your fashion production workflow from "
        "design concept to finished garment."
    )

    st.divider()

    # ========================================================
    # SESSION STATE
    # ========================================================

    if "production_jobs" not in st.session_state:
        st.session_state.production_jobs = []

    # ========================================================
    # PRODUCTION OVERVIEW
    # ========================================================

    total_jobs = len(
        st.session_state.production_jobs
    )

    active_jobs = sum(
        1
        for job in st.session_state.production_jobs
        if job["status"] == "In Production"
    )

    completed_jobs = sum(
        1
        for job in st.session_state.production_jobs
        if job["status"] == "Completed"
    )

    pending_jobs = sum(
        1
        for job in st.session_state.production_jobs
        if job["status"] == "Pending"
    )

    overview = st.columns(4)

    with overview[0]:
        st.metric(
            "🏭 Total Jobs",
            total_jobs
        )

    with overview[1]:
        st.metric(
            "⚙ Active",
            active_jobs
        )

    with overview[2]:
        st.metric(
            "⏳ Pending",
            pending_jobs
        )

    with overview[3]:
        st.metric(
            "✅ Completed",
            completed_jobs
        )

    st.divider()

    # ========================================================
    # CREATE PRODUCTION JOB
    # ========================================================

    st.subheader("➕ Create Production Job")

    st.caption(
        "Create a production job for a garment or collection."
    )

    with st.form("production_job_form"):

        col1, col2 = st.columns(2)

        with col1:

            garment_name = st.text_input(
                "Garment / Product Name",
                placeholder="e.g. Emerald Evening Gown"
            )

            client_name = st.text_input(
                "Client",
                placeholder="e.g. Amaka Fashion House"
            )

            category = st.selectbox(
                "Category",
                [
                    "Dress",
                    "Gown",
                    "Suit",
                    "Shirt",
                    "Trousers",
                    "Skirt",
                    "Jacket",
                    "Traditional Wear",
                    "Streetwear",
                    "Other",
                ]
            )

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
                step=1
            )

        with col2:

            production_status = st.selectbox(
                "Production Status",
                [
                    "Pending",
                    "In Production",
                    "Quality Check",
                    "Completed",
                    "On Hold",
                ]
            )

            priority = st.selectbox(
                "Priority",
                [
                    "Normal",
                    "High",
                    "Urgent",
                ]
            )

            deadline = st.date_input(
                "Production Deadline"
            )

            assigned_to = st.text_input(
                "Assigned To",
                placeholder="e.g. Tailor / Production Team"
            )

        notes = st.text_area(
            "Production Notes",
            placeholder=(
                "Add special instructions, fabric details, "
                "construction notes or production requirements..."
            )
        )

        submitted = st.form_submit_button(
            "🏭 Create Production Job",
            use_container_width=True,
            type="primary",
        )

    # ========================================================
    # SAVE JOB
    # ========================================================

    if submitted:

        if not garment_name.strip():

            st.error(
                "Please enter the garment or product name."
            )

        else:

            job = {
                "id": total_jobs + 1,
                "garment_name": garment_name.strip(),
                "client": client_name.strip() or "No Client",
                "category": category,
                "quantity": quantity,
                "status": production_status,
                "priority": priority,
                "deadline": str(deadline),
                "assigned_to": (
                    assigned_to.strip()
                    or "Unassigned"
                ),
                "notes": notes.strip(),
                "progress": 0,
            }

            if production_status == "In Production":
                job["progress"] = 50

            elif production_status == "Quality Check":
                job["progress"] = 80

            elif production_status == "Completed":
                job["progress"] = 100

            st.session_state.production_jobs.append(
                job
            )

            st.success(
                f"Production job '{garment_name}' created successfully."
            )

            st.rerun()

    # ========================================================
    # PRODUCTION JOBS
    # ========================================================

    st.divider()

    st.subheader("📋 Production Jobs")

    if not st.session_state.production_jobs:

        st.info(
            "No production jobs yet. "
            "Create your first production job above."
        )

    else:

        for job in st.session_state.production_jobs:

            with st.container(border=True):

                header_col, status_col = st.columns(
                    [4, 1]
                )

                with header_col:

                    st.markdown(
                        f"### 🧵 {job['garment_name']}"
                    )

                    st.caption(
                        f"Client: {job['client']} • "
                        f"Category: {job['category']}"
                    )

                with status_col:

                    st.write(
                        f"**{job['status']}**"
                    )

                # ------------------------------------------------
                # JOB INFORMATION
                # ------------------------------------------------

                info = st.columns(4)

                with info[0]:

                    st.metric(
                        "Quantity",
                        job["quantity"]
                    )

                with info[1]:

                    st.metric(
                        "Priority",
                        job["priority"]
                    )

                with info[2]:

                    st.metric(
                        "Deadline",
                        job["deadline"]
                    )

                with info[3]:

                    st.metric(
                        "Progress",
                        f"{job['progress']}%"
                    )

                # ------------------------------------------------
                # PROGRESS
                # ------------------------------------------------

                st.progress(
                    job["progress"] / 100
                )

                # ------------------------------------------------
                # ASSIGNMENT
                # ------------------------------------------------

                st.caption(
                    f"👤 Assigned to: {job['assigned_to']}"
                )

                if job["notes"]:

                    st.caption(
                        f"📝 {job['notes']}"
                    )

                # ------------------------------------------------
                # PRODUCTION ACTIONS
                # ------------------------------------------------

                action1, action2, action3 = st.columns(3)

                with action1:

                    if st.button(
                        "⚙ Update Status",
                        key=f"update_status_{job['id']}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            f"edit_job_{job['id']}"
                        ] = True

                        st.rerun()

                with action2:

                    if st.button(
                        "📋 View Details",
                        key=f"view_job_{job['id']}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            f"view_job_{job['id']}"
                        ] = not st.session_state.get(
                            f"view_job_{job['id']}",
                            False
                        )

                        st.rerun()

                with action3:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_job_{job['id']}",
                        use_container_width=True,
                    ):

                        st.session_state.production_jobs = [
                            item
                            for item
                            in st.session_state.production_jobs
                            if item["id"] != job["id"]
                        ]

                        st.success(
                            "Production job deleted."
                        )

                        st.rerun()

                # ------------------------------------------------
                # UPDATE STATUS
                # ------------------------------------------------

                if st.session_state.get(
                    f"edit_job_{job['id']}",
                    False
                ):

                    new_status = st.selectbox(
                        "Production Status",
                        [
                            "Pending",
                            "In Production",
                            "Quality Check",
                            "Completed",
                            "On Hold",
                        ],
                        index=[
                            "Pending",
                            "In Production",
                            "Quality Check",
                            "Completed",
                            "On Hold",
                        ].index(job["status"]),
                        key=f"status_select_{job['id']}",
                    )

                    if st.button(
                        "Save Status",
                        key=f"save_status_{job['id']}",
                        type="primary",
                    ):

                        job["status"] = new_status

                        if new_status == "Pending":
                            job["progress"] = 0

                        elif new_status == "In Production":
                            job["progress"] = 50

                        elif new_status == "Quality Check":
                            job["progress"] = 80

                        elif new_status == "Completed":
                            job["progress"] = 100

                        elif new_status == "On Hold":
                            job["progress"] = 25

                        st.session_state[
                            f"edit_job_{job['id']}"
                        ] = False

                        st.success(
                            "Production status updated."
                        )

                        st.rerun()

                # ------------------------------------------------
                # VIEW DETAILS
                # ------------------------------------------------

                if st.session_state.get(
                    f"view_job_{job['id']}",
                    False
                ):

                    st.markdown(
                        "**Production Details**"
                    )

                    detail1, detail2 = st.columns(2)

                    with detail1:

                        st.write(
                            f"**Product:** {job['garment_name']}"
                        )

                        st.write(
                            f"**Client:** {job['client']}"
                        )

                        st.write(
                            f"**Category:** {job['category']}"
                        )

                        st.write(
                            f"**Quantity:** {job['quantity']}"
                        )

                    with detail2:

                        st.write(
                            f"**Status:** {job['status']}"
                        )

                        st.write(
                            f"**Priority:** {job['priority']}"
                        )

                        st.write(
                            f"**Deadline:** {job['deadline']}"
                        )

                        st.write(
                            f"**Assigned To:** {job['assigned_to']}"
                        )