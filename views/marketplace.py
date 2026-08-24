import streamlit as st

from database.marketplace import (
    init_marketplace_table,
    create_listing,
    get_listings,
    get_listing,
    get_user_listings,
    update_listing,
    delete_listing,
    add_listing_images,
    get_listing_images,
    delete_listing_image,
    get_listing_image_count,
    MARKETPLACE_CATEGORIES,
    LISTING_TYPES,
)


# ============================================================
# HELPERS
# ============================================================

MAX_MARKETPLACE_IMAGES = 10


def listing_icon(listing_type):

    if listing_type == "Product":
        return "🛍️"

    if listing_type == "Service":
        return "🛠️"

    return "📦"


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
        number = (
            "234"
            + number[1:]
        )

    return (
        f"https://wa.me/{number}"
    )


# ============================================================
# DISPLAY LISTING IMAGES
# ============================================================

def display_listing_images(
    listing_id,
    fallback_image_url="",
    height=350
):

    images = get_listing_images(
        listing_id
    )

    # --------------------------------------------------------
    # New uploaded images
    # --------------------------------------------------------

    if images:

        image_data = [
            image[2]
            for image in images
            if image[2]
        ]

        if image_data:

            if len(image_data) == 1:

                st.image(
                    image_data[0],
                    use_container_width=True
                )

            else:

                image_cols = st.columns(
                    min(
                        len(image_data),
                        3
                    )
                )

                for index, image in enumerate(
                    image_data
                ):

                    with image_cols[
                        index % len(image_cols)
                    ]:

                        st.image(
                            image,
                            use_container_width=True
                        )

            return

    # --------------------------------------------------------
    # Legacy URL image
    # --------------------------------------------------------

    if fallback_image_url:

        st.image(
            fallback_image_url,
            use_container_width=True
        )

        return

    # --------------------------------------------------------
    # Empty image
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div style="
            height:{height}px;
            display:flex;
            align-items:center;
            justify-content:center;
            background:#f5f5f5;
            border-radius:15px;
            font-size:100px;
        ">
            📸
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LISTING DETAILS
# ============================================================

def render_listing_details(
    listing_id
):

    listing = get_listing(
        listing_id
    )

    if not listing:

        st.error(
            "Listing not found."
        )

        if st.button(
            "← Back to Marketplace"
        ):

            st.session_state.marketplace_view = (
                "explore"
            )

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

    if st.button(
        "← Back to Marketplace"
    ):

        st.session_state.marketplace_view = (
            "explore"
        )

        st.rerun()

    st.divider()

    # ========================================================
    # MAIN LISTING
    # ========================================================

    col1, col2 = st.columns(
        [1, 1]
    )

    with col1:

        display_listing_images(
            listing_id=listing_id,
            fallback_image_url=image_url,
            height=350
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

        st.subheader(
            "About this listing"
        )

        if description:

            st.write(
                description
            )

        else:

            st.info(
                "No description provided."
            )

        st.divider()

        st.subheader(
            "Seller"
        )

        st.write(
            f"👤 **{seller_name}**"
        )

        # ----------------------------------------------------
        # Contact buttons
        # ----------------------------------------------------

        contact_col1, contact_col2 = (
            st.columns(2)
        )

        with contact_col1:

            if whatsapp:

                url = whatsapp_url(
                    whatsapp
                )

                if url:

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
    # ALL PRODUCT IMAGES
    # ========================================================

    listing_images = (
        get_listing_images(
            listing_id
        )
    )

    if len(listing_images) > 1:

        st.subheader(
            f"📸 Product Photos ({len(listing_images)})"
        )

        gallery_cols = st.columns(
            3
        )

        for index, image_row in enumerate(
            listing_images
        ):

            image_data = image_row[2]

            if not image_data:
                continue

            with gallery_cols[
                index % 3
            ]:

                st.image(
                    image_data,
                    use_container_width=True
                )

    # ========================================================
    # SELLER INFORMATION
    # ========================================================

    st.subheader(
        "👤 Seller Information"
    )

    seller_col1, seller_col2 = (
        st.columns(2)
    )

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

    if not st.session_state.get(
        "logged_in",
        False
    ):

        st.warning(
            "Please login or create an account "
            "before creating a marketplace listing."
        )

        return

    st.subheader(
        "➕ Create Marketplace Listing"
    )

    st.write(
        "Sell fashion products or offer "
        "fashion-related services to customers."
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
            "e.g. Premium Ankara Fabric "
            "or Custom Tailoring"
        ),
        key="create_listing_title"
    )

    category = st.selectbox(
        "Category",
        MARKETPLACE_CATEGORIES,
        key="create_listing_category"
    )

    seller_name = st.text_input(
        "Business / Seller Name",
        placeholder="e.g. Chekwube Empire",
        key="create_listing_seller_name"
    )

    location = st.text_input(
        "Location",
        placeholder="Owerri, Nigeria",
        key="create_listing_location"
    )

    description = st.text_area(
        "Description",
        placeholder=(
            "Describe your product, service, "
            "professional experience, etc."
        ),
        height=150,
        key="create_listing_description"
    )

    price = st.text_input(
        "Price / Price Range",
        placeholder="e.g. ₦25,000",
        key="create_listing_price"
    )

    # ========================================================
    # PRODUCT IMAGES
    # ========================================================

    st.subheader(
        "📸 Product Images"
    )

    st.caption(
        "Upload clear photos of your product. "
        "You can upload up to 10 images."
    )

    uploaded_images = st.file_uploader(
        "Choose product images",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ],
        accept_multiple_files=True,
        key="create_listing_images"
    )

    if uploaded_images:

        if len(uploaded_images) > MAX_MARKETPLACE_IMAGES:

            st.error(
                f"You can upload a maximum of "
                f"{MAX_MARKETPLACE_IMAGES} images."
            )

        else:

            st.success(
                f"📸 {len(uploaded_images)} "
                f"image(s) selected."
            )

            preview_cols = st.columns(
                min(
                    len(uploaded_images),
                    5
                )
            )

            for index, uploaded_file in enumerate(
                uploaded_images
            ):

                with preview_cols[
                    index % len(preview_cols)
                ]:

                    st.image(
                        uploaded_file,
                        caption=(
                            f"Photo {index + 1}"
                        ),
                        use_container_width=True
                    )

    phone = st.text_input(
        "Phone Number",
        placeholder="08012345678",
        key="create_listing_phone"
    )

    whatsapp = st.text_input(
        "WhatsApp Number",
        placeholder=(
            "08012345678 or 2348012345678"
        ),
        key="create_listing_whatsapp"
    )

    st.divider()

    # ========================================================
    # PUBLISH
    # ========================================================

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
                "Please enter your business "
                "or seller name."
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

        if (
            uploaded_images
            and len(uploaded_images)
            > MAX_MARKETPLACE_IMAGES
        ):

            st.error(
                f"Please select no more than "
                f"{MAX_MARKETPLACE_IMAGES} images."
            )

            return

        # ----------------------------------------------------
        # Create listing
        # ----------------------------------------------------

        listing_id = create_listing(

            user_id=st.session_state.user_id,

            title=title,

            listing_type=listing_type,

            category=category,

            seller_name=seller_name,

            location=location,

            description=description,

            price=price,

            # Kept empty because images are now uploaded.
            image_url="",

            phone=phone,

            whatsapp=whatsapp,
        )

        # ----------------------------------------------------
        # Save uploaded images
        # ----------------------------------------------------

        if uploaded_images:

            add_listing_images(
                listing_id=listing_id,
                uploaded_images=uploaded_images
            )

        st.success(
            "✅ Listing published successfully!"
        )

        st.session_state.marketplace_view = (
            "explore"
        )

        st.rerun()


# ============================================================
# EDIT LISTING
# ============================================================

def render_edit_listing(
    listing_id
):

    listing = get_listing(
        listing_id
    )

    if not listing:

        st.error(
            "Listing not found."
        )

        return

    # ========================================================
    # SECURITY CHECK
    # ========================================================

    if (
        listing[1]
        != st.session_state.user_id
    ):

        st.error(
            "You are not authorized to edit this listing."
        )

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

    st.subheader(
        "✏️ Edit Listing"
    )

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    title = st.text_input(
        "Listing Title",
        value=old_title or "",
        key=f"edit_title_{listing_id}"
    )

    listing_type = st.selectbox(
        "Listing Type",
        LISTING_TYPES,
        index=(
            LISTING_TYPES.index(
                old_listing_type
            )
            if old_listing_type
            in LISTING_TYPES
            else 0
        ),
        key=f"edit_listing_type_{listing_id}"
    )

    category = st.selectbox(
        "Category",
        MARKETPLACE_CATEGORIES,
        index=(
            MARKETPLACE_CATEGORIES.index(
                old_category
            )
            if old_category
            in MARKETPLACE_CATEGORIES
            else 0
        ),
        key=f"edit_category_{listing_id}"
    )

    seller_name = st.text_input(
        "Seller Name",
        value=old_seller_name or "",
        key=f"edit_seller_name_{listing_id}"
    )

    location = st.text_input(
        "Location",
        value=old_location or "",
        key=f"edit_location_{listing_id}"
    )

    description = st.text_area(
        "Description",
        value=old_description or "",
        height=150,
        key=f"edit_description_{listing_id}"
    )

    price = st.text_input(
        "Price",
        value=old_price or "",
        key=f"edit_price_{listing_id}"
    )

    # ========================================================
    # EXISTING IMAGES
    # ========================================================

    st.divider()

    st.subheader(
        "📸 Product Photos"
    )

    existing_images = get_listing_images(
        listing_id
    )

    if existing_images:

        st.caption(
            f"{len(existing_images)} saved image(s)"
        )

        for image_row in existing_images:

            (
                image_id,
                image_listing_id,
                image_data,
                filename,
                mime_type,
                sort_order,
                image_created_at,
            ) = image_row

            image_col, info_col, action_col = (
                st.columns(
                    [1.5, 2.5, 1]
                )
            )

            with image_col:

                if image_data:

                    st.image(
                        image_data,
                        width=180
                    )

            with info_col:

                st.write(
                    filename
                    or f"Product Photo {image_id}"
                )

                st.caption(
                    mime_type
                )

            with action_col:

                if st.button(
                    "🗑️ Delete",
                    key=(
                        f"delete_image_"
                        f"{listing_id}_"
                        f"{image_id}"
                    ),
                    use_container_width=True
                ):

                    deleted = (
                        delete_listing_image(
                            image_id=image_id,
                            listing_id=listing_id
                        )
                    )

                    if deleted:

                        st.success(
                            "Image deleted."
                        )

                    else:

                        st.error(
                            "Unable to delete image."
                        )

                    st.rerun()

            st.divider()

    else:

        # ----------------------------------------------------
        # Legacy URL image
        # ----------------------------------------------------

        if old_image_url:

            st.write(
                "Legacy listing image"
            )

            st.image(
                old_image_url,
                width=250
            )

            st.caption(
                "This listing still uses an old "
                "image URL. You can add uploaded "
                "images below."
            )

        else:

            st.info(
                "No product photos have been added yet."
            )

    # ========================================================
    # ADD MORE IMAGES
    # ========================================================

    current_image_count = (
        get_listing_image_count(
            listing_id
        )
    )

    remaining_slots = (
        MAX_MARKETPLACE_IMAGES
        - current_image_count
    )

    if remaining_slots > 0:

        st.subheader(
            "➕ Add More Photos"
        )

        st.caption(
            f"You can add {remaining_slots} "
            f"more image(s). Maximum: "
            f"{MAX_MARKETPLACE_IMAGES}."
        )

        new_images = st.file_uploader(
            "Choose additional product images",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ],
            accept_multiple_files=True,
            key=f"edit_images_{listing_id}"
        )

        if new_images:

            if len(new_images) > remaining_slots:

                st.error(
                    f"You can only add "
                    f"{remaining_slots} more image(s)."
                )

            else:

                st.success(
                    f"📸 {len(new_images)} "
                    f"new image(s) selected."
                )

                preview_cols = st.columns(
                    min(
                        len(new_images),
                        5
                    )
                )

                for index, uploaded_file in enumerate(
                    new_images
                ):

                    with preview_cols[
                        index % len(preview_cols)
                    ]:

                        st.image(
                            uploaded_file,
                            caption=(
                                f"New Photo "
                                f"{index + 1}"
                            ),
                            use_container_width=True
                        )

    else:

        st.info(
            f"You already have the maximum "
            f"of {MAX_MARKETPLACE_IMAGES} images."
        )

        new_images = []

    # ========================================================
    # CONTACT
    # ========================================================

    phone = st.text_input(
        "Phone",
        value=old_phone or "",
        key=f"edit_phone_{listing_id}"
    )

    whatsapp = st.text_input(
        "WhatsApp",
        value=old_whatsapp or "",
        key=f"edit_whatsapp_{listing_id}"
    )

    st.divider()

    # ========================================================
    # SAVE / DELETE
    # ========================================================

    col1, col2 = st.columns(
        2
    )

    with col1:

        if st.button(
            "💾 Save Changes",
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
                    "Please enter your seller name."
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

            if (
                new_images
                and len(new_images)
                > remaining_slots
            ):

                st.error(
                    f"You can only add "
                    f"{remaining_slots} more image(s)."
                )

                return

            # ------------------------------------------------
            # Update listing details
            # ------------------------------------------------

            updated = update_listing(

                listing_id=listing_id,

                user_id=st.session_state.user_id,

                title=title,

                listing_type=listing_type,

                category=category,

                seller_name=seller_name,

                location=location,

                description=description,

                price=price,

                # Keep legacy field unchanged.
                image_url=old_image_url or "",

                phone=phone,

                whatsapp=whatsapp,
            )

            # ------------------------------------------------
            # Save new images
            # ------------------------------------------------

            if updated and new_images:

                add_listing_images(
                    listing_id=listing_id,
                    uploaded_images=new_images
                )

            if updated:

                st.success(
                    "✅ Listing updated successfully."
                )

                st.session_state.marketplace_view = (
                    "explore"
                )

                st.rerun()

            else:

                st.error(
                    "Unable to update listing."
                )

    with col2:

        if st.button(
            "🗑️ Delete Listing",
            use_container_width=True
        ):

            st.session_state[
                "confirm_delete_listing"
            ] = True

    # ========================================================
    # DELETE CONFIRMATION
    # ========================================================

    if st.session_state.get(
        "confirm_delete_listing",
        False
    ):

        st.warning(
            "Are you sure you want to permanently "
            "delete this listing and all of its "
            "product photos?"
        )

        confirm_col1, confirm_col2 = (
            st.columns(2)
        )

        with confirm_col1:

            if st.button(
                "Yes, Delete Everything",
                type="primary",
                use_container_width=True
            ):

                deleted = delete_listing(
                    listing_id=listing_id,
                    user_id=st.session_state.user_id
                )

                if deleted:

                    st.session_state[
                        "confirm_delete_listing"
                    ] = False

                    st.session_state.marketplace_view = (
                        "explore"
                    )

                    st.success(
                        "Listing and all product photos "
                        "were deleted."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to delete listing."
                    )

        with confirm_col2:

            if st.button(
                "Cancel",
                use_container_width=True
            ):

                st.session_state[
                    "confirm_delete_listing"
                ] = False

                st.rerun()


# ============================================================
# EXPLORE MARKETPLACE
# ============================================================

def render_explore():

    st.subheader(
        "🔎 Explore Marketplace"
    )

    search = st.text_input(
        "🔍 Search",
        placeholder=(
            "Search clothes, fabrics, shoes, "
            "designers, tailors..."
        ),
        key="marketplace_search"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        category = st.selectbox(
            "Category",
            ["All"]
            + MARKETPLACE_CATEGORIES,
            key="explore_category"
        )

    with col2:

        listing_type = st.selectbox(
            "Listing Type",
            ["All"]
            + LISTING_TYPES,
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
            row_start:
            row_start + 3
        ]

        cols = st.columns(
            3
        )

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

                    # ------------------------------------------------
                    # Primary image
                    # ------------------------------------------------

                    listing_images = (
                        get_listing_images(
                            listing_id
                        )
                    )

                    if listing_images:

                        primary_image = (
                            listing_images[0][2]
                        )

                        st.image(
                            primary_image,
                            use_container_width=True
                        )

                        if len(
                            listing_images
                        ) > 1:

                            st.caption(
                                f"📸 "
                                f"{len(listing_images)} "
                                f"photos"
                            )

                    elif image_url:

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

                    st.subheader(
                        title
                    )

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

                        if len(
                            description
                        ) > 120:

                            short_description += "..."

                        st.write(
                            short_description
                        )

                    st.write(
                        f"👤 **{seller_name}**"
                    )

                    if st.button(
                        "👁️ View Details",
                        key=(
                            f"view_{listing_id}"
                        ),
                        use_container_width=True
                    ):

                        st.session_state[
                            "selected_listing_id"
                        ] = listing_id

                        st.session_state[
                            "marketplace_view"
                        ] = "details"

                        st.rerun()


# ============================================================
# MY LISTINGS
# ============================================================

def render_my_listings():

    if not st.session_state.get(
        "logged_in",
        False
    ):

        st.warning(
            "Please login to view your listings."
        )

        return

    user_id = (
        st.session_state.user_id
    )

    listings = get_user_listings(
        user_id
    )

    st.subheader(
        "📦 My Listings"
    )

    if not listings:

        st.info(
            "You haven't created any "
            "marketplace listings yet."
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

        with st.container(
            border=True
        ):

            col1, col2 = st.columns(
                [1, 3]
            )

            with col1:

                listing_images = (
                    get_listing_images(
                        listing_id
                    )
                )

                if listing_images:

                    st.image(
                        listing_images[0][2],
                        use_container_width=True
                    )

                    if len(
                        listing_images
                    ) > 1:

                        st.caption(
                            f"📸 "
                            f"{len(listing_images)} "
                            f"photos"
                        )

                elif image_url:

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
                            {listing_icon(
                                listing_type
                            )}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with col2:

                st.subheader(
                    title
                )

                st.caption(
                    f"{listing_type} • "
                    f"{category}"
                )

                if price:

                    st.write(
                        f"💰 **{price}**"
                    )

                if location:

                    st.caption(
                        f"📍 {location}"
                    )

                if description:

                    st.write(
                        description[:200]
                    )

                st.caption(
                    f"Posted: {created_at}"
                )

                if st.button(
                    "✏️ Edit",
                    key=(
                        f"edit_my_listing_"
                        f"{listing_id}"
                    )
                ):

                    st.session_state[
                        "selected_listing_id"
                    ] = listing_id

                    st.session_state[
                        "marketplace_view"
                    ] = "edit"

                    st.rerun()


# ============================================================
# MAIN MARKETPLACE
# ============================================================

def render_marketplace():

    init_marketplace_table()

    if (
        "marketplace_view"
        not in st.session_state
    ):

        st.session_state.marketplace_view = (
            "explore"
        )

    st.title(
        "🛍️ Fashion Marketplace"
    )

    st.write(
        "Discover fashion products and services "
        "from sellers, creators, and businesses."
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