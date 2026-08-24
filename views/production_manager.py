import streamlit as st
from datetime import date, datetime

from database.database import get_connection


# ============================================================
# PRODUCTION STATUS
# ============================================================

PRODUCTION_STATUSES = [
    "Pending",
    "Cutting",
    "In Production",
    "Fitting",
    "Quality Check",
    "Completed",
    "On Hold",
]


STATUS_PROGRESS = {
    "Pending": 0,
    "Cutting": 20,
    "In Production": 50,
    "Fitting": 70,
    "Quality Check": 85,
    "Completed": 100,
    "On Hold": 25,
}


PRIORITIES = [
    "Normal",
    "High",
    "Urgent",
]


# ============================================================
# USER
# ============================================================

def get_user_id():

    return st.session_state.get(
        "user_id"
    )


# ============================================================
# MEASUREMENT PROFILE DATABASE
# ============================================================

def get_measurement_profiles():

    user_id = get_user_id()

    if not user_id:
        return []

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                client_name,
                category,
                unit
            FROM measurement_profiles
            WHERE user_id = ?
            ORDER BY client_name
            """,
            (str(user_id),)
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "client_name": row[1],
                "category": row[2],
                "unit": row[3],
            }
            for row in rows
        ]

    except Exception as e:

        st.error(
            f"Unable to load measurement profiles: {e}"
        )

        return []

    finally:

        conn.close()


# ============================================================
# TECH PACK DATABASE
# ============================================================

def get_tech_packs():

    user_id = get_user_id()

    if not user_id:
        return []

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                design_name,
                category,
                fabric,
                colour
            FROM tech_packs
            WHERE user_id = ?
            ORDER BY design_name
            """,
            (str(user_id),)
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "design_name": row[1],
                "category": row[2],
                "fabric": row[3],
                "colour": row[4],
            }
            for row in rows
        ]

    except Exception as e:

        st.error(
            f"Unable to load tech packs: {e}"
        )

        return []

    finally:

        conn.close()


# ============================================================
# CLIENTS
# ============================================================

def get_client_names():

    user_id = get_user_id()

    if not user_id:
        return []

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name
            FROM clients
            WHERE user_id = ?
            ORDER BY name
            """,
            (str(user_id),)
        )

        rows = cursor.fetchall()

        return [
            row[0]
            for row in rows
            if row[0]
        ]

    except Exception:

        return []

    finally:

        conn.close()


# ============================================================
# PRODUCTION ORDERS
# ============================================================

def get_production_orders():

    user_id = get_user_id()

    if not user_id:
        return []

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                client_name,
                design_name,
                measurement_profile_id,
                tech_pack_id,
                fabric,
                quantity,
                status,
                priority,
                start_date,
                due_date,
                assigned_to,
                notes,
                created_at,
                updated_at
            FROM production_orders
            WHERE user_id = ?
            ORDER BY
                CASE priority
                    WHEN 'Urgent' THEN 1
                    WHEN 'High' THEN 2
                    ELSE 3
                END,
                due_date ASC,
                id DESC
            """,
            (str(user_id),)
        )

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    except Exception as e:

        st.error(
            f"Unable to load production jobs: {e}"
        )

        return []

    finally:

        conn.close()


# ============================================================
# CREATE PRODUCTION ORDER
# ============================================================

def create_production_order(
    client_name,
    design_name,
    measurement_profile_id,
    tech_pack_id,
    fabric,
    quantity,
    status,
    priority,
    start_date,
    due_date,
    assigned_to,
    notes,
):

    user_id = get_user_id()

    if not user_id:

        return False, "No logged-in user found."

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO production_orders (

                user_id,
                client_name,
                design_name,

                measurement_profile_id,
                tech_pack_id,

                fabric,
                quantity,
                status,
                priority,

                start_date,
                due_date,

                assigned_to,
                notes

            )
            VALUES (
                ?, ?, ?,
                ?, ?,
                ?, ?, ?, ?,
                ?, ?,
                ?, ?
            )
            """,
            (
                str(user_id),

                client_name,
                design_name,

                measurement_profile_id,
                tech_pack_id,

                fabric,
                quantity,
                status,
                priority,

                str(start_date),
                str(due_date),

                assigned_to,
                notes,
            )
        )

        conn.commit()

        return True, (
            "Production job created successfully."
        )

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        conn.close()


# ============================================================
# UPDATE PRODUCTION ORDER
# ============================================================

def update_production_order(
    order_id,
    client_name,
    design_name,
    measurement_profile_id,
    tech_pack_id,
    fabric,
    quantity,
    status,
    priority,
    start_date,
    due_date,
    assigned_to,
    notes,
):

    user_id = get_user_id()

    if not user_id:

        return False, "No logged-in user found."

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE production_orders

            SET

                client_name = ?,
                design_name = ?,

                measurement_profile_id = ?,
                tech_pack_id = ?,

                fabric = ?,
                quantity = ?,

                status = ?,
                priority = ?,

                start_date = ?,
                due_date = ?,

                assigned_to = ?,
                notes = ?,

                updated_at = CURRENT_TIMESTAMP

            WHERE id = ?
            AND user_id = ?
            """,
            (
                client_name,
                design_name,

                measurement_profile_id,
                tech_pack_id,

                fabric,
                quantity,

                status,
                priority,

                str(start_date),
                str(due_date),

                assigned_to,
                notes,

                order_id,
                str(user_id),
            )
        )

        conn.commit()

        return True, (
            "Production job updated successfully."
        )

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        conn.close()


# ============================================================
# DELETE
# ============================================================

def delete_production_order(order_id):

    user_id = get_user_id()

    if not user_id:

        return False, "No logged-in user found."

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM production_orders

            WHERE id = ?
            AND user_id = ?
            """,
            (
                order_id,
                str(user_id),
            )
        )

        conn.commit()

        return True, "Production job deleted."

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        conn.close()


# ============================================================
# SAFE DATE
# ============================================================

def parse_date(value):

    if not value:

        return date.today()

    try:

        return datetime.strptime(
            str(value),
            "%Y-%m-%d"
        ).date()

    except Exception:

        return date.today()


# ============================================================
# PRODUCTION MANAGER
# ============================================================

def render_production_manager():

    st.title("🏭 Production Manager")

    st.caption(
        "Manage your fashion production workflow from "
        "design concept to finished garment."
    )

    st.divider()

    # ========================================================
    # LOAD DATABASE DATA
    # ========================================================

    orders = get_production_orders()

    measurement_profiles = (
        get_measurement_profiles()
    )

    tech_packs = (
        get_tech_packs()
    )

    client_names = (
        get_client_names()
    )

    # ========================================================
    # OVERVIEW
    # ========================================================

    total_jobs = len(orders)

    pending_jobs = sum(
        1
        for job in orders
        if job["status"] == "Pending"
    )

    active_jobs = sum(
        1
        for job in orders
        if job["status"]
        in [
            "Cutting",
            "In Production",
            "Fitting",
        ]
    )

    quality_jobs = sum(
        1
        for job in orders
        if job["status"] == "Quality Check"
    )

    completed_jobs = sum(
        1
        for job in orders
        if job["status"] == "Completed"
    )

    urgent_jobs = sum(
        1
        for job in orders
        if job["priority"] == "Urgent"
    )

    overview = st.columns(6)

    with overview[0]:

        st.metric(
            "🏭 Total Jobs",
            total_jobs
        )

    with overview[1]:

        st.metric(
            "⏳ Pending",
            pending_jobs
        )

    with overview[2]:

        st.metric(
            "⚙ Active",
            active_jobs
        )

    with overview[3]:

        st.metric(
            "🔍 Quality Check",
            quality_jobs
        )

    with overview[4]:

        st.metric(
            "✅ Completed",
            completed_jobs
        )

    with overview[5]:

        st.metric(
            "🚨 Urgent",
            urgent_jobs
        )

    st.divider()

    # ========================================================
    # CREATE JOB
    # ========================================================

    st.subheader(
        "➕ Create Production Job"
    )

    st.caption(
        "Create a production order and connect it to "
        "the client's measurements and tech pack."
    )

    with st.form(
        "production_job_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        # ====================================================
        # PRODUCT
        # ====================================================

        with col1:

            design_name = st.text_input(
                "Garment / Product Name",
                placeholder="e.g. Emerald Evening Gown"
            )

            if client_names:

                client_options = [
                    "Select Client"
                ] + client_names

                selected_client = st.selectbox(
                    "Client",
                    client_options
                )

                client_name = (
                    ""
                    if selected_client == "Select Client"
                    else selected_client
                )

            else:

                client_name = st.text_input(
                    "Client",
                    placeholder="e.g. Amaka"
                )

            category = st.selectbox(
                "Garment Category",
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
                    "Bridal",
                    "Sportswear",
                    "Other",
                ]
            )

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
                step=1
            )

        # ====================================================
        # PRODUCTION
        # ====================================================

        with col2:

            production_status = st.selectbox(
                "Production Status",
                PRODUCTION_STATUSES
            )

            priority = st.selectbox(
                "Priority",
                PRIORITIES
            )

            start_date = st.date_input(
                "Production Start Date",
                value=date.today()
            )

            due_date = st.date_input(
                "Production Deadline",
                value=date.today()
            )

            assigned_to = st.text_input(
                "Assigned To",
                placeholder="e.g. Tailor / Production Team"
            )

        st.divider()

        # ====================================================
        # MEASUREMENT PROFILE
        # ====================================================

        st.markdown(
            "### 📏 Measurement Profile"
        )

        if measurement_profiles:

            measurement_options = [
                "No Measurement Profile"
            ]

            measurement_lookup = {}

            for profile in measurement_profiles:

                label = (
                    f"👤 {profile['client_name']} "
                    f"• {profile['category']} "
                    f"• {profile['unit'] or 'in'}"
                )

                measurement_options.append(
                    label
                )

                measurement_lookup[label] = (
                    profile["id"]
                )

            selected_measurement = st.selectbox(
                "Attach Client Measurements",
                measurement_options
            )

            measurement_profile_id = (
                None
                if selected_measurement
                == "No Measurement Profile"
                else measurement_lookup.get(
                    selected_measurement
                )
            )

        else:

            st.info(
                "No measurement profiles found. "
                "Create a measurement profile first."
            )

            measurement_profile_id = None

        # ====================================================
        # TECH PACK
        # ====================================================

        st.markdown(
            "### 📋 Tech Pack"
        )

        if tech_packs:

            tech_pack_options = [
                "No Tech Pack"
            ]

            tech_pack_lookup = {}

            for tech_pack in tech_packs:

                label = (
                    f"📋 {tech_pack['design_name']} "
                    f"• {tech_pack['category'] or 'Fashion'} "
                    f"• {tech_pack['fabric'] or 'Fabric not specified'}"
                )

                tech_pack_options.append(
                    label
                )

                tech_pack_lookup[label] = (
                    tech_pack["id"]
                )

            selected_tech_pack = st.selectbox(
                "Attach Tech Pack",
                tech_pack_options
            )

            tech_pack_id = (
                None
                if selected_tech_pack
                == "No Tech Pack"
                else tech_pack_lookup.get(
                    selected_tech_pack
                )
            )

        else:

            st.info(
                "No tech packs found. "
                "Create a tech pack first."
            )

            tech_pack_id = None

        # ====================================================
        # FABRIC
        # ====================================================

        fabric = st.text_input(
            "Fabric",
            placeholder=(
                "e.g. Italian crepe, linen, Ankara, silk"
            )
        )

        notes = st.text_area(
            "Production Notes",
            placeholder=(
                "Add fabric instructions, construction "
                "requirements, fitting notes, special "
                "instructions or quality requirements..."
            )
        )

        submitted = st.form_submit_button(
            "🏭 Create Production Job",
            use_container_width=True,
            type="primary",
        )

    # ========================================================
    # SAVE
    # ========================================================

    if submitted:

        if not design_name.strip():

            st.error(
                "Please enter the garment or product name."
            )

        elif not client_name.strip():

            st.error(
                "Please enter the client's name."
            )

        elif due_date < start_date:

            st.error(
                "Production deadline cannot be before "
                "the start date."
            )

        else:

            success, message = (
                create_production_order(
                    client_name=client_name.strip(),
                    design_name=design_name.strip(),

                    measurement_profile_id=(
                        measurement_profile_id
                    ),

                    tech_pack_id=(
                        tech_pack_id
                    ),

                    fabric=fabric.strip(),

                    quantity=quantity,

                    status=production_status,

                    priority=priority,

                    start_date=start_date,

                    due_date=due_date,

                    assigned_to=(
                        assigned_to.strip()
                        or "Unassigned"
                    ),

                    notes=notes.strip(),
                )
            )

            if success:

                st.success(
                    f"✅ {message}"
                )

                st.rerun()

            else:

                st.error(
                    f"❌ {message}"
                )

    # ========================================================
    # PRODUCTION JOBS
    # ========================================================

    st.divider()

    st.subheader(
        "📋 Production Jobs"
    )

    if not orders:

        st.info(
            "No production jobs yet. "
            "Create your first production job above."
        )

        return

    # ========================================================
    # SEARCH
    # ========================================================

    filter_col1, filter_col2, filter_col3 = (
        st.columns([2, 1, 1])
    )

    with filter_col1:

        search = st.text_input(
            "🔎 Search production jobs",
            placeholder=(
                "Search client, garment or assigned person..."
            ),
            key="production_search"
        ).strip().lower()

    with filter_col2:

        status_filter = st.selectbox(
            "Status",
            ["All"] + PRODUCTION_STATUSES,
            key="production_status_filter"
        )

    with filter_col3:

        priority_filter = st.selectbox(
            "Priority",
            ["All"] + PRIORITIES,
            key="production_priority_filter"
        )

    # ========================================================
    # FILTER
    # ========================================================

    filtered_orders = []

    for job in orders:

        searchable = " ".join(
            [
                str(job.get("client_name", "")),
                str(job.get("design_name", "")),
                str(job.get("assigned_to", "")),
                str(job.get("fabric", "")),
            ]
        ).lower()

        if search and search not in searchable:
            continue

        if (
            status_filter != "All"
            and job["status"] != status_filter
        ):
            continue

        if (
            priority_filter != "All"
            and job["priority"] != priority_filter
        ):
            continue

        filtered_orders.append(job)

    st.caption(
        f"Showing {len(filtered_orders)} "
        f"of {len(orders)} production jobs."
    )

    # ========================================================
    # DISPLAY
    # ========================================================

    for job in filtered_orders:

        job_id = job["id"]

        progress = STATUS_PROGRESS.get(
            job["status"],
            0
        )

        with st.container(border=True):

            header_col, status_col = st.columns(
                [4, 1]
            )

            with header_col:

                st.markdown(
                    f"### 🧵 {job['design_name']}"
                )

                st.caption(
                    f"Client: {job['client_name']} • "
                    f"Quantity: {job['quantity']}"
                )

            with status_col:

                st.markdown(
                    f"**{job['status']}**"
                )

                st.caption(
                    f"{job['priority']} Priority"
                )

            st.progress(
                progress / 100
            )

            st.caption(
                f"Production progress: {progress}%"
            )

            # =================================================
            # ATTACHMENT STATUS
            # =================================================

            attachment_col1, attachment_col2 = (
                st.columns(2)
            )

            with attachment_col1:

                if job.get(
                    "measurement_profile_id"
                ):

                    st.success(
                        "📏 Measurement Profile Attached"
                    )

                else:

                    st.warning(
                        "📏 No Measurement Profile"
                    )

            with attachment_col2:

                if job.get(
                    "tech_pack_id"
                ):

                    st.success(
                        "📋 Tech Pack Attached"
                    )

                else:

                    st.warning(
                        "📋 No Tech Pack"
                    )

            # =================================================
            # METRICS
            # =================================================

            info = st.columns(5)

            with info[0]:

                st.metric(
                    "Quantity",
                    job["quantity"]
                )

            with info[1]:

                st.metric(
                    "Start",
                    job["start_date"]
                )

            with info[2]:

                st.metric(
                    "Deadline",
                    job["due_date"]
                )

            with info[3]:

                st.metric(
                    "Fabric",
                    job["fabric"]
                    or "Not specified"
                )

            with info[4]:

                st.metric(
                    "Assigned",
                    job["assigned_to"]
                    or "Unassigned"
                )

            # =================================================
            # OVERDUE
            # =================================================

            due = parse_date(
                job["due_date"]
            )

            if (
                due < date.today()
                and job["status"] != "Completed"
            ):

                st.warning(
                    "⚠️ This production job is overdue."
                )

            # =================================================
            # ACTIONS
            # =================================================

            action1, action2, action3 = st.columns(3)

            with action1:

                if st.button(
                    "⚙ Update Status",
                    key=f"update_status_{job_id}",
                    use_container_width=True,
                ):

                    st.session_state[
                        f"editing_status_{job_id}"
                    ] = True

                    st.rerun()

            with action2:

                if st.button(
                    "✏️ Edit Job",
                    key=f"edit_job_{job_id}",
                    use_container_width=True,
                ):

                    st.session_state[
                        f"editing_job_{job_id}"
                    ] = True

                    st.rerun()

            with action3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_job_{job_id}",
                    use_container_width=True,
                ):

                    success, message = (
                        delete_production_order(
                            job_id
                        )
                    )

                    if success:

                        st.success(
                            message
                        )

                        st.rerun()

                    else:

                        st.error(
                            message
                        )

            # =================================================
            # STATUS EDITOR
            # =================================================

            if st.session_state.get(
                f"editing_status_{job_id}",
                False
            ):

                st.markdown(
                    "#### ⚙ Update Production Status"
                )

                status_col1, status_col2 = (
                    st.columns([2, 1])
                )

                with status_col1:

                    new_status = st.selectbox(
                        "Production Status",
                        PRODUCTION_STATUSES,
                        index=PRODUCTION_STATUSES.index(
                            job["status"]
                        ),
                        key=f"new_status_{job_id}",
                    )

                with status_col2:

                    st.write("")
                    st.write("")

                    if st.button(
                        "Save Status",
                        key=f"save_status_{job_id}",
                        type="primary",
                        use_container_width=True,
                    ):

                        success, message = (
                            update_production_order(

                                order_id=job_id,

                                client_name=job[
                                    "client_name"
                                ],

                                design_name=job[
                                    "design_name"
                                ],

                                measurement_profile_id=job[
                                    "measurement_profile_id"
                                ],

                                tech_pack_id=job[
                                    "tech_pack_id"
                                ],

                                fabric=job[
                                    "fabric"
                                ],

                                quantity=job[
                                    "quantity"
                                ],

                                status=new_status,

                                priority=job[
                                    "priority"
                                ],

                                start_date=parse_date(
                                    job[
                                        "start_date"
                                    ]
                                ),

                                due_date=parse_date(
                                    job[
                                        "due_date"
                                    ]
                                ),

                                assigned_to=job[
                                    "assigned_to"
                                ],

                                notes=job[
                                    "notes"
                                ],
                            )
                        )

                        if success:

                            st.session_state[
                                f"editing_status_{job_id}"
                            ] = False

                            st.success(
                                message
                            )

                            st.rerun()

                        else:

                            st.error(
                                message
                            )

            # =================================================
            # FULL EDITOR
            # =================================================

            if st.session_state.get(
                f"editing_job_{job_id}",
                False
            ):

                st.markdown(
                    "#### ✏️ Edit Production Job"
                )

                with st.form(
                    f"edit_production_{job_id}"
                ):

                    edit_col1, edit_col2 = (
                        st.columns(2)
                    )

                    with edit_col1:

                        edit_client = st.text_input(
                            "Client",
                            value=job[
                                "client_name"
                            ],
                        )

                        edit_design = st.text_input(
                            "Garment / Product",
                            value=job[
                                "design_name"
                            ],
                        )

                        edit_fabric = st.text_input(
                            "Fabric",
                            value=job[
                                "fabric"
                            ] or "",
                        )

                        edit_quantity = (
                            st.number_input(
                                "Quantity",
                                min_value=1,
                                value=int(
                                    job[
                                        "quantity"
                                    ] or 1
                                ),
                                step=1,
                            )
                        )

                    with edit_col2:

                        edit_status = st.selectbox(
                            "Status",
                            PRODUCTION_STATUSES,
                            index=PRODUCTION_STATUSES.index(
                                job["status"]
                            ),
                        )

                        edit_priority = st.selectbox(
                            "Priority",
                            PRIORITIES,
                            index=PRIORITIES.index(
                                job["priority"]
                            ),
                        )

                        edit_start = st.date_input(
                            "Start Date",
                            value=parse_date(
                                job[
                                    "start_date"
                                ]
                            ),
                        )

                        edit_due = st.date_input(
                            "Deadline",
                            value=parse_date(
                                job[
                                    "due_date"
                                ]
                            ),
                        )

                    # =================================================
                    # EDIT ATTACHMENTS
                    # =================================================

                    st.markdown(
                        "##### 📎 Attachments"
                    )

                    edit_measurement_options = [
                        "No Measurement Profile"
                    ]

                    edit_measurement_lookup = {}

                    for profile in measurement_profiles:

                        label = (
                            f"👤 {profile['client_name']} "
                            f"• {profile['category']} "
                            f"• {profile['unit'] or 'in'}"
                        )

                        edit_measurement_options.append(
                            label
                        )

                        edit_measurement_lookup[label] = (
                            profile["id"]
                        )

                    current_measurement_label = (
                        "No Measurement Profile"
                    )

                    for label, profile_id in (
                        edit_measurement_lookup.items()
                    ):

                        if (
                            profile_id
                            == job.get(
                                "measurement_profile_id"
                            )
                        ):

                            current_measurement_label = label
                            break

                    edit_selected_measurement = st.selectbox(
                        "Measurement Profile",
                        edit_measurement_options,
                        index=edit_measurement_options.index(
                            current_measurement_label
                        ),
                    )

                    edit_measurement_id = (
                        None
                        if edit_selected_measurement
                        == "No Measurement Profile"
                        else edit_measurement_lookup.get(
                            edit_selected_measurement
                        )
                    )

                    edit_tech_options = [
                        "No Tech Pack"
                    ]

                    edit_tech_lookup = {}

                    for tech_pack in tech_packs:

                        label = (
                            f"📋 {tech_pack['design_name']} "
                            f"• {tech_pack['category'] or 'Fashion'} "
                            f"• {tech_pack['fabric'] or 'Fabric not specified'}"
                        )

                        edit_tech_options.append(
                            label
                        )

                        edit_tech_lookup[label] = (
                            tech_pack["id"]
                        )

                    current_tech_label = (
                        "No Tech Pack"
                    )

                    for label, tech_id in (
                        edit_tech_lookup.items()
                    ):

                        if (
                            tech_id
                            == job.get(
                                "tech_pack_id"
                            )
                        ):

                            current_tech_label = label
                            break

                    edit_selected_tech = st.selectbox(
                        "Tech Pack",
                        edit_tech_options,
                        index=edit_tech_options.index(
                            current_tech_label
                        ),
                    )

                    edit_tech_id = (
                        None
                        if edit_selected_tech
                        == "No Tech Pack"
                        else edit_tech_lookup.get(
                            edit_selected_tech
                        )
                    )

                    edit_assigned = st.text_input(
                        "Assigned To",
                        value=job[
                            "assigned_to"
                        ] or "",
                    )

                    edit_notes = st.text_area(
                        "Production Notes",
                        value=job[
                            "notes"
                        ] or "",
                    )

                    save_edit = (
                        st.form_submit_button(
                            "💾 Save Changes",
                            type="primary",
                            use_container_width=True,
                        )
                    )

                if save_edit:

                    if not edit_client.strip():

                        st.error(
                            "Client name is required."
                        )

                    elif not edit_design.strip():

                        st.error(
                            "Garment name is required."
                        )

                    elif edit_due < edit_start:

                        st.error(
                            "Deadline cannot be before "
                            "the start date."
                        )

                    else:

                        success, message = (
                            update_production_order(

                                order_id=job_id,

                                client_name=(
                                    edit_client.strip()
                                ),

                                design_name=(
                                    edit_design.strip()
                                ),

                                measurement_profile_id=(
                                    edit_measurement_id
                                ),

                                tech_pack_id=(
                                    edit_tech_id
                                ),

                                fabric=(
                                    edit_fabric.strip()
                                ),

                                quantity=(
                                    edit_quantity
                                ),

                                status=(
                                    edit_status
                                ),

                                priority=(
                                    edit_priority
                                ),

                                start_date=(
                                    edit_start
                                ),

                                due_date=(
                                    edit_due
                                ),

                                assigned_to=(
                                    edit_assigned.strip()
                                    or "Unassigned"
                                ),

                                notes=(
                                    edit_notes.strip()
                                ),
                            )
                        )

                        if success:

                            st.session_state[
                                f"editing_job_{job_id}"
                            ] = False

                            st.success(
                                message
                            )

                            st.rerun()

                        else:

                            st.error(
                                message
                            )

            # =================================================
            # DETAILS
            # =================================================

            with st.expander(
                "📋 View Production Details"
            ):

                detail1, detail2 = st.columns(2)

                with detail1:

                    st.write(
                        f"**Client:** "
                        f"{job['client_name']}"
                    )

                    st.write(
                        f"**Garment:** "
                        f"{job['design_name']}"
                    )

                    st.write(
                        f"**Quantity:** "
                        f"{job['quantity']}"
                    )

                    st.write(
                        f"**Fabric:** "
                        f"{job['fabric'] or 'Not specified'}"
                    )

                    st.write(
                        f"**Assigned To:** "
                        f"{job['assigned_to'] or 'Unassigned'}"
                    )

                with detail2:

                    st.write(
                        f"**Status:** "
                        f"{job['status']}"
                    )

                    st.write(
                        f"**Priority:** "
                        f"{job['priority']}"
                    )

                    st.write(
                        f"**Start Date:** "
                        f"{job['start_date']}"
                    )

                    st.write(
                        f"**Deadline:** "
                        f"{job['due_date']}"
                    )

                    if job.get(
                        "measurement_profile_id"
                    ):

                        st.success(
                            "📏 Measurement profile attached"
                        )

                    else:

                        st.warning(
                            "📏 No measurement profile attached"
                        )

                    if job.get(
                        "tech_pack_id"
                    ):

                        st.success(
                            "📋 Tech pack attached"
                        )

                    else:

                        st.warning(
                            "📋 No tech pack attached"
                        )

                if job.get("notes"):

                    st.divider()

                    st.markdown(
                        "**Production Notes:**"
                    )

                    st.write(
                        job["notes"]
                    )