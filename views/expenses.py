import streamlit as st


def render_expenses():

    st.title("💸 Expenses")

    st.caption(
        "Track and manage the money you spend running your fashion business."
    )

    # ============================================================
    # SESSION STATE
    # ============================================================

    if "expenses" not in st.session_state:
        st.session_state.expenses = []

    # ============================================================
    # EXPENSE SUMMARY
    # ============================================================

    expenses = st.session_state.expenses

    total_expenses = sum(
        expense["amount"]
        for expense in expenses
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Expenses",
            f"₦{total_expenses:,.2f}"
        )

    with col2:
        st.metric(
            "Expense Records",
            len(expenses)
        )

    with col3:

        categories_used = len(
            set(
                expense["category"]
                for expense in expenses
            )
        )

        st.metric(
            "Categories",
            categories_used
        )

    st.divider()

    # ============================================================
    # ADD EXPENSE
    # ============================================================

    st.subheader("➕ Add Expense")

    col1, col2 = st.columns(2)

    with col1:

        expense_name = st.text_input(
            "Expense Name",
            placeholder="e.g. Ankara Fabric",
            key="expense_name",
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=500.0,
            key="expense_amount",
        )

        category = st.selectbox(
            "Category",
            [
                "Fabric & Materials",
                "Labor",
                "Transportation",
                "Electricity",
                "Equipment",
                "Packaging",
                "Marketing",
                "Rent",
                "Tools",
                "Other",
            ],
            key="expense_category",
        )

    with col2:

        expense_date = st.date_input(
            "Expense Date",
            key="expense_date",
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash",
                "Bank Transfer",
                "Card",
                "Mobile Payment",
                "Other",
            ],
            key="expense_payment_method",
        )

        description = st.text_area(
            "Description",
            placeholder="Add additional details...",
            key="expense_description",
        )

    # ============================================================
    # SAVE EXPENSE
    # ============================================================

    if st.button(
        "💾 Save Expense",
        type="primary",
        use_container_width=True,
    ):

        if not expense_name.strip():

            st.error(
                "Please enter an expense name."
            )

            return

        if amount <= 0:

            st.error(
                "Please enter an amount greater than ₦0."
            )

            return

        expense = {
            "name": expense_name.strip(),
            "amount": amount,
            "category": category,
            "date": str(expense_date),
            "payment_method": payment_method,
            "description": description.strip(),
        }

        st.session_state.expenses.append(
            expense
        )

        st.success(
            "✅ Expense saved successfully."
        )

        st.rerun()

    # ============================================================
    # EXPENSE DIRECTORY
    # ============================================================

    st.divider()

    st.subheader("📋 Expense Records")

    if not expenses:

        st.info(
            "No expenses recorded yet."
        )

        return

    # ============================================================
    # FILTER
    # ============================================================

    category_filter = st.selectbox(
        "Filter by Category",
        [
            "All",
            "Fabric & Materials",
            "Labor",
            "Transportation",
            "Electricity",
            "Equipment",
            "Packaging",
            "Marketing",
            "Rent",
            "Tools",
            "Other",
        ],
        key="expense_category_filter",
    )

    filtered_expenses = [
        expense
        for expense in expenses
        if (
            category_filter == "All"
            or expense["category"] == category_filter
        )
    ]

    if not filtered_expenses:

        st.info(
            "No expenses found for this category."
        )

        return

    # ============================================================
    # EXPENSE LIST
    # ============================================================

    for index, expense in enumerate(
        filtered_expenses
    ):

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [2, 2, 1]
            )

            with col1:

                st.markdown(
                    f"### 💸 {expense['name']}"
                )

                st.write(
                    f"🏷️ **Category:** {expense['category']}"
                )

                st.write(
                    f"📅 **Date:** {expense['date']}"
                )

            with col2:

                st.write(
                    f"💰 **Amount:** ₦{expense['amount']:,.2f}"
                )

                st.write(
                    f"💳 **Payment:** {expense['payment_method']}"
                )

                if expense["description"]:

                    st.caption(
                        f"📝 {expense['description']}"
                    )

            with col3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_expense_{index}",
                ):

                    original_expense = (
                        filtered_expenses[index]
                    )

                    original_index = (
                        st.session_state.expenses.index(
                            original_expense
                        )
                    )

                    st.session_state.expenses.pop(
                        original_index
                    )

                    st.rerun()