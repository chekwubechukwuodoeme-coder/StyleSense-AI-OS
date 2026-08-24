import streamlit as st


def render_pricing():

    st.title("💰 Pricing")

    st.caption(
        "Calculate production cost, profit margin and recommended selling prices for your garments."
    )

    # ============================================================
    # PRICING CALCULATOR
    # ============================================================

    st.subheader("🧮 Garment Pricing Calculator")

    col1, col2 = st.columns(2)

    with col1:

        garment_name = st.text_input(
            "Garment Name",
            placeholder="e.g. Luxury Evening Gown",
            key="pricing_garment_name",
        )

        material_cost = st.number_input(
            "Fabric & Material Cost",
            min_value=0.0,
            step=500.0,
            key="pricing_material_cost",
        )

        labor_cost = st.number_input(
            "Labor Cost",
            min_value=0.0,
            step=500.0,
            key="pricing_labor_cost",
        )

    with col2:

        overhead_cost = st.number_input(
            "Overhead Cost",
            min_value=0.0,
            step=500.0,
            key="pricing_overhead_cost",
        )

        additional_cost = st.number_input(
            "Additional Cost",
            min_value=0.0,
            step=500.0,
            key="pricing_additional_cost",
        )

        profit_margin = st.number_input(
            "Profit Margin (%)",
            min_value=0.0,
            max_value=1000.0,
            value=30.0,
            step=5.0,
            key="pricing_profit_margin",
        )

    # ============================================================
    # CALCULATE
    # ============================================================

    if st.button(
        "🧮 Calculate Price",
        type="primary",
        use_container_width=True,
    ):

        if not garment_name.strip():

            st.error(
                "Please enter the garment name."
            )

            return

        total_cost = (
            material_cost
            + labor_cost
            + overhead_cost
            + additional_cost
        )

        profit_amount = (
            total_cost
            * profit_margin
            / 100
        )

        selling_price = (
            total_cost
            + profit_amount
        )

        st.session_state.pricing_result = {
            "garment": garment_name.strip(),
            "material_cost": material_cost,
            "labor_cost": labor_cost,
            "overhead_cost": overhead_cost,
            "additional_cost": additional_cost,
            "total_cost": total_cost,
            "profit_margin": profit_margin,
            "profit_amount": profit_amount,
            "selling_price": selling_price,
        }

    # ============================================================
    # RESULTS
    # ============================================================

    pricing_result = st.session_state.get(
        "pricing_result"
    )

    if pricing_result:

        st.divider()

        st.subheader("📊 Pricing Breakdown")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:

            st.metric(
                "Total Production Cost",
                f"₦{pricing_result['total_cost']:,.2f}",
            )

        with result_col2:

            st.metric(
                "Expected Profit",
                f"₦{pricing_result['profit_amount']:,.2f}",
            )

        with result_col3:

            st.metric(
                "Recommended Price",
                f"₦{pricing_result['selling_price']:,.2f}",
            )

        st.divider()

        st.write(
            f"### 👗 {pricing_result['garment']}"
        )

        breakdown_col1, breakdown_col2 = st.columns(2)

        with breakdown_col1:

            st.write(
                f"🧵 **Materials:** "
                f"₦{pricing_result['material_cost']:,.2f}"
            )

            st.write(
                f"✂️ **Labor:** "
                f"₦{pricing_result['labor_cost']:,.2f}"
            )

            st.write(
                f"🏭 **Overhead:** "
                f"₦{pricing_result['overhead_cost']:,.2f}"
            )

        with breakdown_col2:

            st.write(
                f"➕ **Additional Costs:** "
                f"₦{pricing_result['additional_cost']:,.2f}"
            )

            st.write(
                f"📈 **Profit Margin:** "
                f"{pricing_result['profit_margin']:.1f}%"
            )

            st.write(
                f"💰 **Profit:** "
                f"₦{pricing_result['profit_amount']:,.2f}"
            )

    # ============================================================
    # SAVED PRICING
    # ============================================================

    st.divider()

    st.subheader("📚 Pricing Records")

    if "pricing_records" not in st.session_state:

        st.session_state.pricing_records = []

    if pricing_result:

        if st.button(
            "💾 Save This Pricing",
            use_container_width=True,
        ):

            st.session_state.pricing_records.append(
                pricing_result.copy()
            )

            st.success(
                "✅ Pricing saved successfully."
            )

            st.rerun()

    pricing_records = st.session_state.pricing_records

    if not pricing_records:

        st.info(
            "No pricing records saved yet."
        )

        return

    for index, record in enumerate(
        pricing_records
    ):

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [2, 2, 1]
            )

            with col1:

                st.markdown(
                    f"### 👗 {record['garment']}"
                )

                st.write(
                    f"Production Cost: "
                    f"₦{record['total_cost']:,.2f}"
                )

            with col2:

                st.write(
                    f"Profit: "
                    f"₦{record['profit_amount']:,.2f}"
                )

                st.write(
                    f"Margin: "
                    f"{record['profit_margin']:.1f}%"
                )

                st.write(
                    f"Recommended Price: "
                    f"₦{record['selling_price']:,.2f}"
                )

            with col3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_pricing_{index}",
                ):

                    st.session_state.pricing_records.pop(
                        index
                    )

                    st.rerun()