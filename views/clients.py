import streamlit as st


def render_clients():

    st.title("👥 Clients")

    st.caption(
        "Manage your fashion clients, contact information, "
        "measurements and order history."
    )

    # ============================================================
    # SESSION STATE
    # ============================================================

    if "clients" not in st.session_state:
        st.session_state.clients = []

    # ============================================================
    # SEARCH
    # ============================================================

    search = st.text_input(
        "🔍 Search Clients",
        placeholder="Search by client name, phone or email...",
        key="client_search",
    )

    st.divider()

    # ============================================================
    # ADD CLIENT
    # ============================================================

    st.subheader("➕ Add New Client")

    col1, col2 = st.columns(2)

    with col1:

        client_name = st.text_input(
            "Full Name",
            placeholder="Enter client name",
            key="new_client_name",
        )

        phone = st.text_input(
            "Phone Number",
            placeholder="+234...",
            key="new_client_phone",
        )

        email = st.text_input(
            "Email",
            placeholder="client@example.com",
            key="new_client_email",
        )

    with col2:

        location = st.text_input(
            "Location",
            placeholder="City / State",
            key="new_client_location",
        )

        client_type = st.selectbox(
            "Client Type",
            [
                "Individual",
                "VIP Client",
                "Corporate",
                "Boutique",
                "Other",
            ],
            key="new_client_type",
        )

        notes = st.text_area(
            "Notes",
            placeholder="Add client notes...",
            key="new_client_notes",
        )

    # ============================================================
    # SAVE CLIENT
    # ============================================================

    if st.button(
        "💾 Save Client",
        type="primary",
        use_container_width=True,
    ):

        if not client_name.strip():

            st.error(
                "Please enter the client's name."
            )

            return

        client = {
            "name": client_name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
            "location": location.strip(),
            "client_type": client_type,
            "notes": notes.strip(),
        }

        st.session_state.clients.append(client)

        st.success(
            f"✅ {client_name.strip()} has been added."
        )

        st.rerun()

    # ============================================================
    # CLIENT LIST
    # ============================================================

    st.divider()

    st.subheader("📋 Client Directory")

    clients = st.session_state.clients

    if search.strip():

        search_text = search.strip().lower()

        clients = [
            client
            for client in clients
            if (
                search_text in client["name"].lower()
                or search_text in client["phone"].lower()
                or search_text in client["email"].lower()
            )
        ]

    if not clients:

        if search.strip():

            st.info(
                "No clients match your search."
            )

        else:

            st.info(
                "No clients added yet."
            )

        return

    # ============================================================
    # CLIENT CARDS
    # ============================================================

    for index, client in enumerate(clients):

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [2, 2, 1]
            )

            with col1:

                st.markdown(
                    f"### 👤 {client['name']}"
                )

                st.caption(
                    client["client_type"]
                )

            with col2:

                if client["phone"]:

                    st.write(
                        f"📞 {client['phone']}"
                    )

                if client["email"]:

                    st.write(
                        f"✉️ {client['email']}"
                    )

                if client["location"]:

                    st.write(
                        f"📍 {client['location']}"
                    )

            with col3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_client_{index}",
                ):

                    original_index = (
                        st.session_state.clients.index(
                            client
                        )
                    )

                    st.session_state.clients.pop(
                        original_index
                    )

                    st.rerun()

            if client["notes"]:

                st.caption(
                    f"📝 {client['notes']}"
                )

            st.divider()

            action1, action2 = st.columns(2)

            with action1:

                if st.button(
                    "📏 Measurements",
                    key=f"client_measurements_{index}",
                    use_container_width=True,
                ):

                    st.session_state.main_navigation = (
                        "Measurements"
                    )

                    st.rerun()

            with action2:

                if st.button(
                    "🛒 Orders",
                    key=f"client_orders_{index}",
                    use_container_width=True,
                ):

                    st.session_state.main_navigation = (
                        "Orders"
                    )

                    st.rerun()