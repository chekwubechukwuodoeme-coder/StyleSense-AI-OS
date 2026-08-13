import streamlit as st

from database.marketplace import (
    init_marketplace_table,
    create_listing,
    get_listings,
    get_listing,
    get_user_listings,
    update_listing,
    delete_listing,
    MARKETPLACE_CATEGORIES,
    LISTING_TYPES,
)


# ============================================================
# HELPERS
# ============================================================

def listing_icon(listing_type):

    if listing_type == "Product":
        return "🛍️"

    if listing_type == "Professional":
        return "👤"

    return "🛠️"


def whatsapp_url(number):
    if not number:
        return None

    number = (
        number.strip()
        .replace(" ", "")
        .replace("-", "")
        .replace("+", "")
    )

    if number.startswith("0"):
        number = "234" + number[1:]

    return f"https://wa.me/{number}"


# ============================================================
# LISTING DETAILS
# ============================================================

def render_listing_details(listing_id):

    listing = get_listing(listing_id)

    if not listing:

        st.error("Listing not found.")

        if st.button("← Back to Marketplace"):
            st.session_state.marketplace_view = "explore"
            st.rerun()

        return

    (
        listing_id,
        listing_user_id,
        title,
        listing_type,
        category,
        seller_name,
        location,
        description,
        price,
        image_url,
        phone,
        whatsapp,
        created_at,
    ) = listing

    if st.button("← Back to Marketplace"):

        st.session_state.marketplace_view = "explore"
        st.rerun()

    st.divider()

    # ========================================================
    # MAIN LISTING
    # ========================================================

    col1, col2 = st.columns([1, 1])

    with col1:

        if image_url:

            st.image(
                image_url,
                use_container_width=True
            )

        else:

            st.markdown(
                f"""
                <div style="
                    height:350px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:#f5f5f5;
                    border-radius:15px;
                    font-size:100px;
                ">
                    {listing_icon(listing_type)}
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:

        st.title(title)

        st.caption(
            f"{listing_type} • {category}"
        )

        if price:

            st.subheader(
                f"💰 {price}"
            )

        if location:

            st.write(
                f"📍 **Location:** {location}"
            )

        st.divider()

        st.subheader("About this listing")

        if description:

            st.write(description)

        else:

            st.info(
                "No description provided."
            )

        st.divider()

        st.subheader("Seller")

        st.write(
            f"👤 **{seller_name}**"
        )

        # ----------------------------------------------------
        # Contact buttons
        # ----------------------------------------------------

        contact_col1, contact_col2 = st.columns(2)

        with contact_col1:

            if whatsapp:

                url = whatsapp_url(whatsapp)

                st.link_button(
                    "💬 WhatsApp",
                    url,
                    use_container_width=True
                )

        with contact_col2:

            if phone:

                phone_number = (
                    phone
                    .replace(" ", "")
                    .replace("-", "")
                )

                st.link_button(
                    "📞 Call",
                    f"tel:{phone_number}",
                    use_container_width=True
                )

    st.divider()

    # ========================================================
    # SELLER INFORMATION
    # ========================================================

    st.subheader("👤 Seller Information")

    seller_col1, seller_col2 = st.columns(2)

    with seller_col1:

        st.write(
            f"**Seller:** {seller_name}"
        )

    with seller_col2:

        if location:

            st.write(
                f"**Location:** {location}"
            )

    st.caption(
        f"Listing posted: {created_at}"
    )


# ============================================================
# CREATE LISTING
# ============================================================

def render_create_listing():

    if not st.session_state.get("logged_in", False):

        st.warning(
            "Please login or create an account before creating a marketplace listing."
        )

        return

    st.subheader("➕ Create Marketplace Listing")

    st.write(
        "Sell a fashion product, promote your "
        "professional services, or advertise your "
        "fashion business."
    )

    st.divider()

    listing_type = st.selectbox(
        "What are you listing?",
        LISTING_TYPES,
        key="create_listing_type"
    )

    title = st.text_input(
        "Listing Title",
        placeholder=(
            "e.g. Premium Ankara Fabric"
        )
    )

    category = st.selectbox(
        "Category",
        MARKETPLACE_CATEGORIES,
        key="create_listing_category"
    )

    seller_name = st.text_input(
        "Business / Seller Name",
        placeholder="e.g. Chekwube Empire"
    )

    location = st.text_input(
        "Location",
        placeholder="Owerri, Nigeria"
    )

    description = st.text_area(
        "Description",
        placeholder=(
            "Describe your product, service, "
            "professional experience, etc."
        ),
        height=150
    )

    price = st.text_input(
        "Price / Price Range",
        placeholder="e.g. ₦25,000"
    )

    st.subheader("📸 Listing Image")

    image_url = st.text_input(
        "Image URL",
        placeholder="https://example.com/image.jpg"
    )

    phone = st.text_input(
        "Phone Number",
        placeholder="08012345678"
    )

    whatsapp = st.text_input(
        "WhatsApp Number",
        placeholder="08012345678 or 2348012345678"
    )

    st.divider()

    if st.button(
        "🚀 Publish Listing",
        type="primary",
        use_container_width=True
    ):

        if not title.strip():

            st.error(
                "Please enter a listing title."
            )

            return

        if not seller_name.strip():

            st.error(
                "Please enter your business or "
                "seller name."
            )

            return

        if not location.strip():

            st.error(
                "Please enter your location."
            )

            return

        if not description.strip():

            st.error(
                "Please provide a description."
            )

            return

        create_listing(

            user_id=st.session_state.user_id,
            title=title,
            listing_type=listing_type,
            category=category,
            seller_name=seller_name,
            location=location,
            description=description,
            price=price,
            image_url=image_url,
            phone=phone,
            whatsapp=whatsapp,
        )

        st.success(
            "✅ Listing published successfully!"
        )

        st.session_state.marketplace_view = "explore"

        st.rerun()


# ============================================================
# EDIT LISTING
# ============================================================

def render_edit_listing(listing_id):

    listing = get_listing(listing_id)

    if not listing:

        st.error("Listing not found.")

        return

    (
        listing_id,
        listing_user_id,
        old_title,
        old_listing_type,
        old_category,
        old_seller_name,
        old_location,
        old_description,
        old_price,
        old_image_url,
        old_phone,
        old_whatsapp,
        created_at,
    ) = listing

    st.subheader("✏️ Edit Listing")

    title = st.text_input(
        "Listing Title",
        value=old_title or ""
    )

    listing_type = st.selectbox(
        "Listing Type",
        LISTING_TYPES,
        index=(
            LISTING_TYPES.index(old_listing_type)
            if old_listing_type in LISTING_TYPES
            else 0
        )
    )

    category = st.selectbox(
        "Category",
        MARKETPLACE_CATEGORIES,
        index=(
            MARKETPLACE_CATEGORIES.index(old_category)
            if old_category in MARKETPLACE_CATEGORIES
            else 0
        )
    )

    seller_name = st.text_input(
        "Seller Name",
        value=old_seller_name or ""
    )

    location = st.text_input(
        "Location",
        value=old_location or ""
    )

    description = st.text_area(
        "Description",
        value=old_description or "",
        height=150
    )

    price = st.text_input(
        "Price",
        value=old_price or ""
    )

    image_url = st.text_input(
        "Image URL",
        value=old_image_url or ""
    )

    phone = st.text_input(
        "Phone",
        value=old_phone or ""
    )

    whatsapp = st.text_input(
        "WhatsApp",
        value=old_whatsapp or ""
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Save Changes",
            type="primary",
            use_container_width=True
        ):

            update_listing(
                listing_id=listing_id,
                user_id=st.session_state.user_id,
                title=title,
                listing_type=listing_type,
                category=category,
                seller_name=seller_name,
                location=location,
                description=description,
                price=price,
                image_url=image_url,
                phone=phone,
                whatsapp=whatsapp,
            )

            st.success(
                "✅ Listing updated."
            )

            st.session_state.marketplace_view = "explore"

            st.rerun()

    with col2:

        if st.button(
            "🗑️ Delete Listing",
            use_container_width=True
        ):

            st.session_state.confirm_delete = True

    if st.session_state.get(
        "confirm_delete",
        False
    ):

        st.warning(
            "Are you sure you want to permanently "
            "delete this listing?"
        )

        confirm_col1, confirm_col2 = st.columns(2)

        with confirm_col1:

            if st.button(
                "Yes, Delete",
                type="primary",
                use_container_width=True
            ):

                delete_listing(
                    listing_id=listing_id,
                    user_id=st.session_state.user_id
                )

                st.session_state.confirm_delete = False

                st.session_state.marketplace_view = "explore"

                st.success(
                    "Listing deleted."
                )

                st.rerun()

        with confirm_col2:

            if st.button(
                "Cancel",
                use_container_width=True
            ):

                st.session_state.confirm_delete = False

                st.rerun()


# ============================================================
# EXPLORE MARKETPLACE
# ============================================================

def render_explore():

    st.subheader("🔎 Explore Marketplace")

    search = st.text_input(
        "🔍 Search",
        placeholder=(
            "Search clothes, fabrics, shoes, "
            "designers, tailors..."
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        category = st.selectbox(
            "Category",
            ["All"] + MARKETPLACE_CATEGORIES,
            key="explore_category"
        )

    with col2:

        listing_type = st.selectbox(
            "Listing Type",
            ["All"] + LISTING_TYPES,
            key="explore_listing_type"
        )

    with col3:

        location = st.text_input(
            "📍 Location",
            placeholder="Owerri",
            key="explore_location"
        )

    st.divider()

    listings = get_listings(
        search=search,
        category=category,
        listing_type=listing_type,
        location=location,
    )

    if not listings:

        st.info(
            "No marketplace listings found."
        )

        st.markdown(
            """
            ### 🚀 Be the first to list something!

            You can list:

            👕 Clothing  
            🧵 Fabrics  
            👟 Shoes  
            👜 Bags  
            💍 Jewelry  
            👗 Fashion services  
            ✂️ Tailoring  
            📸 Photography  
            💄 Makeup  
            🏭 Manufacturing
            """
        )

        return

    st.caption(
        f"{len(listings)} listing(s) found"
    )

    # ========================================================
    # CARD GRID
    # ========================================================

    for row_start in range(
        0,
        len(listings),
        3
    ):

        row = listings[
            row_start:row_start + 3
        ]

        cols = st.columns(3)

        for col, listing in zip(
            cols,
            row
        ):

            (
                listing_id,
                listing_user_id,
                title,
                listing_type_value,
                category_value,
                seller_name,
                listing_location,
                description,
                price,
                image_url,
                phone,
                whatsapp,
                created_at,
            ) = listing

            with col:

                with st.container(
                    border=True
                ):

                    if image_url:

                        st.image(
                            image_url,
                            use_container_width=True
                        )

                    else:

                        st.markdown(
                            f"""
                            <div style="
                                height:180px;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                background:#f5f5f5;
                                border-radius:10px;
                                font-size:60px;
                            ">
                                {listing_icon(
                                    listing_type_value
                                )}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.subheader(title)

                    st.caption(
                        f"{listing_type_value} • "
                        f"{category_value}"
                    )

                    if price:

                        st.markdown(
                            f"### 💰 {price}"
                        )

                    if listing_location:

                        st.caption(
                            f"📍 {listing_location}"
                        )

                    if description:

                        short_description = (
                            description[:120]
                        )

                        if len(description) > 120:

                            short_description += "..."

                        st.write(
                            short_description
                        )

                    st.write(
                        f"👤 **{seller_name}**"
                    )

                    if st.button(
                        "👁️ View Details",
                        key=f"view_{listing_id}",
                        use_container_width=True
                    ):

                        st.session_state.selected_listing_id = (
                            listing_id
                        )

                        st.session_state.marketplace_view = (
                            "details"
                        )

                        st.rerun()


# ============================================================
# MAIN MARKETPLACE
# ============================================================
def render_my_listings():

    if not st.session_state.get("logged_in", False):

        st.warning(
            "Please login to view your listings."
        )

        return

    user_id = st.session_state.user_id

    listings = get_user_listings(user_id)

    st.subheader("📦 My Listings")

    if not listings:

        st.info(
            "You haven't created any marketplace listings yet."
        )

        return

    st.caption(
        f"You have {len(listings)} listing(s)."
    )

    for listing in listings:

        (
            listing_id,
            listing_user_id,
            title,
            listing_type,
            category,
            seller_name,
            location,
            description,
            price,
            image_url,
            phone,
            whatsapp,
            created_at,
        ) = listing

        with st.container(border=True):

            col1, col2 = st.columns([1, 3])

            with col1:

                if image_url:

                    st.image(
                        image_url,
                        use_container_width=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div style="
                            height:150px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            background:#f5f5f5;
                            border-radius:10px;
                            font-size:60px;
                        ">
                            {listing_icon(listing_type)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with col2:

                st.subheader(title)

                st.caption(
                    f"{listing_type} • {category}"
                )

                if price:
                    st.write(f"💰 **{price}**")

                if location:
                    st.caption(f"📍 {location}")

                if description:
                    st.write(description[:200])

                st.caption(
                    f"Posted: {created_at}"
                )

                if st.button(
                    "✏️ Edit",
                    key=f"edit_my_listing_{listing_id}"
                ):

                    st.session_state.selected_listing_id = listing_id
                    st.session_state.marketplace_view = "edit"
                    st.rerun()


def render_marketplace():

    init_marketplace_table()

    if "marketplace_view" not in st.session_state:

        st.session_state.marketplace_view = "explore"

    st.title("🛍️ Fashion Marketplace")

    st.write(
        "Discover clothing, fabrics, shoes, bags, "
        "fashion professionals, services, manufacturers "
        "and everything fashion-related."
    )

    st.divider()

    # ========================================================
    # DETAILS
    # ========================================================

    if (
        st.session_state.marketplace_view
        == "details"
    ):

        render_listing_details(
            st.session_state.selected_listing_id
        )

        return

    # ========================================================
    # EDIT
    # ========================================================

    if (
        st.session_state.marketplace_view
        == "edit"
    ):

        render_edit_listing(
            st.session_state.selected_listing_id
        )

        return

    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3 = st.tabs([
        "🔎 Explore",
        "➕ Create Listing",
        "📦 My Listings",
    ])

    with tab1:

        render_explore()

    with tab2:

        render_create_listing()

    with tab3:

        render_my_listings()