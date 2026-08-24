import streamlit as st


def render_inventory():

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("📦 Inventory")

    st.caption(
        "Track fabrics, trims, accessories and other "
        "materials used in your fashion production."
    )

    st.divider()

    # ========================================================
    # SESSION STATE
    # ========================================================

    if "inventory_items" not in st.session_state:

        st.session_state.inventory_items = []

    # ========================================================
    # INVENTORY CALCULATIONS
    # ========================================================

    total_items = len(
        st.session_state.inventory_items
    )

    total_quantity = sum(
        item["quantity"]
        for item in st.session_state.inventory_items
    )

    low_stock = sum(
        1
        for item in st.session_state.inventory_items
        if item["quantity"] <= item["low_stock_level"]
    )

    out_of_stock = sum(
        1
        for item in st.session_state.inventory_items
        if item["quantity"] <= 0
    )

    # ========================================================
    # INVENTORY OVERVIEW
    # ========================================================

    overview = st.columns(4)

    with overview[0]:

        st.metric(
            "📦 Items",
            total_items
        )

    with overview[1]:

        st.metric(
            "🔢 Total Stock",
            total_quantity
        )

    with overview[2]:

        st.metric(
            "⚠ Low Stock",
            low_stock
        )

    with overview[3]:

        st.metric(
            "❌ Out of Stock",
            out_of_stock
        )

    st.divider()

    # ========================================================
    # ADD INVENTORY ITEM
    # ========================================================

    st.subheader("➕ Add Inventory Item")

    st.caption(
        "Add a fabric, trim, accessory or production material."
    )

    with st.form("inventory_form"):

        col1, col2 = st.columns(2)

        with col1:

            item_name = st.text_input(
                "Item Name",
                placeholder="e.g. Emerald Silk"
            )

            category = st.selectbox(
                "Category",
                [
                    "Fabric",
                    "Thread",
                    "Buttons",
                    "Zippers",
                    "Beads",
                    "Lace",
                    "Embroidery",
                    "Accessories",
                    "Packaging",
                    "Other",
                ]
            )

            supplier = st.text_input(
                "Supplier",
                placeholder="e.g. Premium Textiles Ltd"
            )

        with col2:

            quantity = st.number_input(
                "Quantity",
                min_value=0.0,
                value=1.0,
                step=1.0
            )

            unit = st.selectbox(
                "Unit",
                [
                    "Meters",
                    "Yards",
                    "Pieces",
                    "Rolls",
                    "Kg",
                    "Grams",
                    "Litres",
                    "Units",
                ]
            )

            low_stock_level = st.number_input(
                "Low Stock Alert Level",
                min_value=0.0,
                value=5.0,
                step=1.0
            )

        unit_cost = st.number_input(
            "Unit Cost",
            min_value=0.0,
            value=0.0,
            step=100.0
        )

        storage_location = st.text_input(
            "Storage Location",
            placeholder="e.g. Shelf A2"
        )

        notes = st.text_area(
            "Notes",
            placeholder=(
                "Add color, material details, supplier notes "
                "or anything else..."
            )
        )

        submitted = st.form_submit_button(
            "📦 Add to Inventory",
            use_container_width=True,
            type="primary",
        )

    # ========================================================
    # SAVE INVENTORY ITEM
    # ========================================================

    if submitted:

        if not item_name.strip():

            st.error(
                "Please enter an item name."
            )

        else:

            item = {

                "id":
                    len(
                        st.session_state.inventory_items
                    ) + 1,

                "name":
                    item_name.strip(),

                "category":
                    category,

                "supplier":
                    supplier.strip() or "Not specified",

                "quantity":
                    quantity,

                "unit":
                    unit,

                "low_stock_level":
                    low_stock_level,

                "unit_cost":
                    unit_cost,

                "storage":
                    storage_location.strip()
                    or "Not specified",

                "notes":
                    notes.strip(),
            }

            st.session_state.inventory_items.append(
                item
            )

            st.success(
                f"{item_name} added to inventory."
            )

            st.rerun()

    # ========================================================
    # LOW STOCK ALERT
    # ========================================================

    low_stock_items = [

        item

        for item
        in st.session_state.inventory_items

        if (
            item["quantity"] <=
            item["low_stock_level"]
            and
            item["quantity"] > 0
        )
    ]

    if low_stock_items:

        st.divider()

        st.warning(
            f"⚠ {len(low_stock_items)} inventory item(s) "
            "are running low."
        )

    # ========================================================
    # INVENTORY SEARCH
    # ========================================================

    st.divider()

    st.subheader("📋 Inventory")

    search = st.text_input(
        "Search Inventory",
        placeholder=(
            "Search fabrics, trims, accessories..."
        ),
        label_visibility="collapsed",
    )

    category_filter = st.selectbox(
        "Filter by Category",
        [
            "All",
            "Fabric",
            "Thread",
            "Buttons",
            "Zippers",
            "Beads",
            "Lace",
            "Embroidery",
            "Accessories",
            "Packaging",
            "Other",
        ]
    )

    # ========================================================
    # FILTER ITEMS
    # ========================================================

    filtered_items = []

    for item in st.session_state.inventory_items:

        matches_search = (
            not search.strip()
            or search.lower()
            in item["name"].lower()
            or search.lower()
            in item["supplier"].lower()
        )

        matches_category = (
            category_filter == "All"
            or item["category"] == category_filter
        )

        if (
            matches_search
            and matches_category
        ):

            filtered_items.append(item)

    # ========================================================
    # EMPTY STATE
    # ========================================================

    if not filtered_items:

        if not st.session_state.inventory_items:

            st.info(
                "📦 Your inventory is empty. "
                "Add your first material above."
            )

        else:

            st.info(
                "No inventory items match your search."
            )

    # ========================================================
    # INVENTORY ITEMS
    # ========================================================

    else:

        for item in filtered_items:

            with st.container(border=True):

                # ------------------------------------------------
                # HEADER
                # ------------------------------------------------

                header_col, status_col = st.columns(
                    [4, 1]
                )

                with header_col:

                    st.markdown(
                        f"### 📦 {item['name']}"
                    )

                    st.caption(
                        f"{item['category']} • "
                        f"Supplier: {item['supplier']}"
                    )

                with status_col:

                    if item["quantity"] <= 0:

                        st.error(
                            "OUT OF STOCK"
                        )

                    elif (
                        item["quantity"]
                        <=
                        item["low_stock_level"]
                    ):

                        st.warning(
                            "LOW STOCK"
                        )

                    else:

                        st.success(
                            "IN STOCK"
                        )

                # ------------------------------------------------
                # ITEM INFORMATION
                # ------------------------------------------------

                info = st.columns(5)

                with info[0]:

                    st.metric(
                        "Quantity",
                        f"{item['quantity']} "
                        f"{item['unit']}"
                    )

                with info[1]:

                    st.metric(
                        "Unit Cost",
                        f"₦{item['unit_cost']:,.0f}"
                    )

                with info[2]:

                    total_value = (
                        item["quantity"]
                        *
                        item["unit_cost"]
                    )

                    st.metric(
                        "Stock Value",
                        f"₦{total_value:,.0f}"
                    )

                with info[3]:

                    st.metric(
                        "Alert Level",
                        item["low_stock_level"]
                    )

                with info[4]:

                    st.metric(
                        "Location",
                        item["storage"]
                    )

                # ------------------------------------------------
                # ACTIONS
                # ------------------------------------------------

                action1, action2, action3 = st.columns(3)

                with action1:

                    if st.button(
                        "➕ Add Stock",
                        key=f"add_stock_{item['id']}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            f"add_stock_mode_{item['id']}"
                        ] = True

                        st.rerun()

                with action2:

                    if st.button(
                        "➖ Remove Stock",
                        key=f"remove_stock_{item['id']}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            f"remove_stock_mode_{item['id']}"
                        ] = True

                        st.rerun()

                with action3:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_inventory_{item['id']}",
                        use_container_width=True,
                    ):

                        st.session_state.inventory_items = [

                            existing

                            for existing
                            in st.session_state.inventory_items

                            if existing["id"]
                            !=
                            item["id"]
                        ]

                        st.success(
                            "Inventory item deleted."
                        )

                        st.rerun()

                # ------------------------------------------------
                # ADD STOCK
                # ------------------------------------------------

                if st.session_state.get(
                    f"add_stock_mode_{item['id']}",
                    False
                ):

                    add_amount = st.number_input(
                        "Amount to add",
                        min_value=0.0,
                        value=1.0,
                        step=1.0,
                        key=f"add_amount_{item['id']}",
                    )

                    if st.button(
                        "Confirm Add",
                        key=f"confirm_add_{item['id']}",
                        type="primary",
                    ):

                        item["quantity"] += add_amount

                        st.session_state[
                            f"add_stock_mode_{item['id']}"
                        ] = False

                        st.success(
                            "Stock updated."
                        )

                        st.rerun()

                # ------------------------------------------------
                # REMOVE STOCK
                # ------------------------------------------------

                if st.session_state.get(
                    f"remove_stock_mode_{item['id']}",
                    False
                ):

                    remove_amount = st.number_input(
                        "Amount to remove",
                        min_value=0.0,
                        value=1.0,
                        step=1.0,
                        key=f"remove_amount_{item['id']}",
                    )

                    if st.button(
                        "Confirm Remove",
                        key=f"confirm_remove_{item['id']}",
                        type="primary",
                    ):

                        if remove_amount > item["quantity"]:

                            st.error(
                                "You cannot remove more stock "
                                "than is currently available."
                            )

                        else:

                            item["quantity"] -= (
                                remove_amount
                            )

                            st.session_state[
                                f"remove_stock_mode_{item['id']}"
                            ] = False

                            st.success(
                                "Stock updated."
                            )

                            st.rerun()

                # ------------------------------------------------
                # NOTES
                # ------------------------------------------------

                if item["notes"]:

                    st.caption(
                        f"📝 {item['notes']}"
                    )