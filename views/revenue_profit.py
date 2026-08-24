import streamlit as st
from datetime import datetime


# ============================================================
# REVENUE & PROFIT
# ============================================================

def render_revenue_profit():

    st.title("💰 Revenue & Profit")

    st.caption(
        "Track your fashion business revenue, expenses and profitability."
    )

    # ========================================================
    # SESSION DATA
    # ========================================================

    orders = st.session_state.get(
        "orders",
        []
    )

    expenses = st.session_state.get(
        "expenses",
        []
    )

    # ========================================================
    # CALCULATE REVENUE
    # ========================================================

    total_revenue = 0.0
    total_paid = 0.0
    outstanding = 0.0

    for order in orders:

        try:

            order_total = float(
                order.get(
                    "total",
                    order.get(
                        "price",
                        order.get(
                            "amount",
                            0
                        )
                    )
                ) or 0
            )

        except (ValueError, TypeError):

            order_total = 0.0

        try:

            amount_paid = float(
                order.get(
                    "amount_paid",
                    order.get(
                        "paid",
                        0
                    )
                ) or 0
            )

        except (ValueError, TypeError):

            amount_paid = 0.0

        total_revenue += order_total
        total_paid += amount_paid

        balance = order_total - amount_paid

        if balance > 0:

            outstanding += balance

    # ========================================================
    # CALCULATE EXPENSES
    # ========================================================

    total_expenses = 0.0

    for expense in expenses:

        try:

            amount = float(
                expense.get(
                    "amount",
                    0
                ) or 0
            )

        except (ValueError, TypeError):

            amount = 0.0

        total_expenses += amount

    # ========================================================
    # PROFIT
    # ========================================================

    net_profit = (
        total_revenue
        - total_expenses
    )

    if total_revenue > 0:

        profit_margin = (
            net_profit
            / total_revenue
        ) * 100

    else:

        profit_margin = 0.0

    # ========================================================
    # FINANCIAL OVERVIEW
    # ========================================================

    st.subheader("📊 Financial Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "💰 Total Revenue",
            f"₦{total_revenue:,.2f}"
        )

    with col2:

        st.metric(
            "💵 Amount Paid",
            f"₦{total_paid:,.2f}"
        )

    with col3:

        st.metric(
            "💸 Expenses",
            f"₦{total_expenses:,.2f}"
        )

    with col4:

        st.metric(
            "📈 Net Profit",
            f"₦{net_profit:,.2f}"
        )

    with col5:

        st.metric(
            "📊 Profit Margin",
            f"{profit_margin:.1f}%"
        )

    # ========================================================
    # OUTSTANDING PAYMENTS
    # ========================================================

    st.divider()

    st.subheader("🧾 Outstanding Payments")

    st.metric(
        "Amount Customers Still Owe",
        f"₦{outstanding:,.2f}"
    )

    if outstanding > 0:

        st.warning(
            "You have outstanding customer payments."
        )

    else:

        st.success(
            "All recorded orders have been fully paid."
        )

    # ========================================================
    # REVENUE VS EXPENSES
    # ========================================================

    st.divider()

    st.subheader("📈 Revenue vs Expenses")

    chart_data = {
        "Revenue": total_revenue,
        "Expenses": total_expenses,
        "Net Profit": net_profit,
    }

    st.bar_chart(
        chart_data
    )

    # ========================================================
    # ORDERS SUMMARY
    # ========================================================

    st.divider()

    st.subheader("👗 Order Revenue")

    if orders:

        order_rows = []

        for order in orders:

            try:

                order_total = float(
                    order.get(
                        "total",
                        order.get(
                            "price",
                            order.get(
                                "amount",
                                0
                            )
                        )
                    ) or 0
                )

            except (ValueError, TypeError):

                order_total = 0.0

            try:

                amount_paid = float(
                    order.get(
                        "amount_paid",
                        order.get(
                            "paid",
                            0
                        )
                    ) or 0
                )

            except (ValueError, TypeError):

                amount_paid = 0.0

            balance = max(
                order_total - amount_paid,
                0
            )

            order_rows.append(
                {
                    "Order":
                        order.get(
                            "order_number",
                            order.get(
                                "id",
                                "Order"
                            )
                        ),

                    "Client":
                        order.get(
                            "client_name",
                            "Unknown Client"
                        ),

                    "Total":
                        f"₦{order_total:,.2f}",

                    "Paid":
                        f"₦{amount_paid:,.2f}",

                    "Balance":
                        f"₦{balance:,.2f}",

                    "Status":
                        order.get(
                            "status",
                            "Pending"
                        ),
                }
            )

        st.dataframe(
            order_rows,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No orders have been recorded yet."
        )

    # ========================================================
    # EXPENSE SUMMARY
    # ========================================================

    st.divider()

    st.subheader("💸 Expense Summary")

    if expenses:

        expense_rows = []

        for expense in expenses:

            try:

                amount = float(
                    expense.get(
                        "amount",
                        0
                    ) or 0
                )

            except (ValueError, TypeError):

                amount = 0.0

            expense_rows.append(
                {
                    "Description":
                        expense.get(
                            "description",
                            expense.get(
                                "name",
                                "Expense"
                            )
                        ),

                    "Category":
                        expense.get(
                            "category",
                            "Other"
                        ),

                    "Amount":
                        f"₦{amount:,.2f}",

                    "Date":
                        expense.get(
                            "date",
                            ""
                        ),
                }
            )

        st.dataframe(
            expense_rows,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No expenses have been recorded yet."
        )

    # ========================================================
    # PROFIT STATUS
    # ========================================================

    st.divider()

    st.subheader("💡 Business Performance")

    if net_profit > 0:

        st.success(
            f"Your business is currently profitable with "
            f"₦{net_profit:,.2f} in net profit."
        )

    elif net_profit < 0:

        st.error(
            f"Your business is currently operating at a "
            f"loss of ₦{abs(net_profit):,.2f}."
        )

    else:

        st.info(
            "Your revenue and expenses are currently balanced."
        )

    # ========================================================
    # REFRESH
    # ========================================================

    st.divider()

    if st.button(
        "🔄 Refresh Financial Data",
        use_container_width=True
    ):

        st.rerun()