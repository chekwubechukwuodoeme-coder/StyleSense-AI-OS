import streamlit as st


def render_orders():

    st.title("🛒 Orders")

    st.caption(
        "Manage client orders, payments, production status and delivery dates."
    )

    # ============================================================
    # SESSION STATE
    # ============================================================

    if "orders" not in st.session_state:
        st.session_state.orders = []

    # ============================================================
    # CREATE ORDER
    # ============================================================

    st.subheader("➕ Create New Order")

    clients = st.session_state.get(
        "clients",
        []
    )

    client_names = [
        client["name"]
        for client in clients
    ]

    if client_names:

        client_name = st.selectbox(
            "Client",
            client_names,
            key="order_client",
        )

    else:

        client_name = st.text_input(
            "Client Name",
            placeholder="Enter client name",
            key="order_client_manual",
        )

        st.info(
            "No saved clients yet. Add a client from the Clients page."
        )

    col1, col2 = st.columns(2)

    with col1:

        garment = st.text_input(
            "Garment / Product",
            placeholder="e.g. Luxury Evening Gown",
            key="order_garment",
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1,
            key="order_quantity",
        )

        order_price = st.number_input(
            "Order Price",
            min_value=0.0,
            step=1000.0,
            key="order_price",
        )

    with col2:

        delivery_date = st.date_input(
            "Expected Delivery Date",
            key="order_delivery_date",
        )

        payment_status = st.selectbox(
            "Payment Status",
            [
                "Pending",
                "Partially Paid",
                "Paid",
            ],
            key="order_payment_status",
        )

        production_status = st.selectbox(
            "Production Status",
            [
                "Not Started",
                "In Production",
                "Fitting",
                "Completed",
                "Delivered",
            ],
            key="order_production_status",
        )

    notes = st.text_area(
        "Order Notes",
        placeholder="Add order details, special requests or instructions...",
        key="order_notes",
    )

    # ============================================================
    # SAVE ORDER
    # ============================================================

    if st.button(
        "💾 Save Order",
        type="primary",
        use_container_width=True,
    ):

        if not client_name.strip():

            st.error(
                "Please enter or select a client."
            )

            return

        if not garment.strip():

            st.error(
                "Please enter the garment or product."
            )

            return

        order = {
            "client": client_name.strip(),
            "garment": garment.strip(),
            "quantity": quantity,
            "price": order_price,
            "delivery_date": str(delivery_date),
            "payment_status": payment_status,
            "production_status": production_status,
            "notes": notes.strip(),
        }

        st.session_state.orders.append(
            order
        )

        st.success(
            "✅ Order created successfully."
        )

        st.rerun()

    # ============================================================
    # ORDER DIRECTORY
    # ============================================================

    st.divider()

    st.subheader("📋 Order Directory")

    orders = st.session_state.orders

    if not orders:

        st.info(
            "No orders created yet."
        )

        return

    # ============================================================
    # FILTERS
    # ============================================================

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        status_filter = st.selectbox(
            "Production Status",
            [
                "All",
                "Not Started",
                "In Production",
                "Fitting",
                "Completed",
                "Delivered",
            ],
            key="orders_status_filter",
        )

    with filter_col2:

        payment_filter = st.selectbox(
            "Payment Status",
            [
                "All",
                "Pending",
                "Partially Paid",
                "Paid",
            ],
            key="orders_payment_filter",
        )

    filtered_orders = []

    for order in orders:

        if (
            status_filter != "All"
            and order["production_status"] != status_filter
        ):
            continue

        if (
            payment_filter != "All"
            and order["payment_status"] != payment_filter
        ):
            continue

        filtered_orders.append(
            order
        )

    # ============================================================
    # ORDER CARDS
    # ============================================================

    for index, order in enumerate(
        filtered_orders
    ):

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [2, 2, 1]
            )

            with col1:

                st.markdown(
                    f"### 🧵 {order['garment']}"
                )

                st.write(
                    f"👤 **Client:** {order['client']}"
                )

                st.write(
                    f"📦 **Quantity:** {order['quantity']}"
                )

            with col2:

                st.write(
                    f"💰 **Price:** ₦{order['price']:,.2f}"
                )

                st.write(
                    f"📅 **Delivery:** {order['delivery_date']}"
                )

                st.write(
                    f"💳 **Payment:** {order['payment_status']}"
                )

                st.write(
                    f"🏭 **Production:** {order['production_status']}"
                )

            with col3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_order_{index}",
                ):

                    original_order = (
                        filtered_orders[index]
                    )

                    original_index = (
                        st.session_state.orders.index(
                            original_order
                        )
                    )

                    st.session_state.orders.pop(
                        original_index
                    )

                    st.rerun()

            if order["notes"]:

                st.caption(
                    f"📝 {order['notes']}"
                )