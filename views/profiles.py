import streamlit as st

from database.profiles import (
    init_profiles_table,
    create_profile,
    get_profiles,
    get_profile,
    get_user_profiles,
    update_profile,
    delete_profile,
)


# ============================================================
# PROFESSION OPTIONS
# ============================================================

PROFESSION_OPTIONS = [

    "Fashion Designer",

    "Tailor",

    "Fashion Stylist",

    "Personal Stylist",

    "Fashion Consultant",

    "Bag Maker",

    "Jewelry Designer",

    "Fashion Photographer",

    "Fashion Videographer",

    "Makeup Artist",

    "Hair Stylist",

    "Barber",

    "Fashion Model",

    "Fashion Influencer",

    "Fashion Content Creator",

    "Fashion Manufacturer",

    "Garment Manufacturer",

    "Textile Manufacturer",

    "Fashion Production Company",

    "Fashion Brand",

    "Fashion Boutique",

    "Fashion Store",

    "Fashion Illustrator",

    "Fashion Pattern Maker",

    "Fashion Embroidery Specialist",

    "Fashion Printer",

    "Fashion Dyer",

    "Fashion Event Planner",

    "Fashion Show Organizer",

    "Other",
]


# ============================================================
# IMAGE HELPERS
# ============================================================

MAX_IMAGE_SIZE = 5 * 1024 * 1024


def validate_profile_image(uploaded_file):

    if uploaded_file is None:

        return None, ""

    image_bytes = uploaded_file.getvalue()

    if not image_bytes:

        return None, ""

    if len(image_bytes) > MAX_IMAGE_SIZE:

        st.error(
            "Profile image is too large. "
            "Please choose an image smaller than 5 MB."
        )

        return None, ""

    mime_type = (
        uploaded_file.type
        or "image/jpeg"
    )

    if not mime_type.startswith("image/"):

        st.error(
            "Please upload a valid image file."
        )

        return None, ""

    return image_bytes, mime_type


def display_profile_image(
    image_data,
    image_url=""
):

    if image_data:

        try:

            st.image(
                image_data,
                use_container_width=True
            )

            return

        except Exception:

            pass

    # --------------------------------------------------------
    # OLD URL COMPATIBILITY
    # --------------------------------------------------------

    if image_url:

        try:

            st.image(
                image_url,
                use_container_width=True
            )

            return

        except Exception:

            pass

    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            height:180px;
            display:flex;
            align-items:center;
            justify-content:center;
            background:#f5f5f5;
            border-radius:12px;
            font-size:70px;
        ">
            👤
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RENDER PROFILE EDITOR
# ============================================================

def render_edit_profile(
    profile_id
):

    profile = get_profile(
        profile_id
    )

    if not profile:

        st.error(
            "Fashion profile not found."
        )

        return

    user_id = st.session_state.get(
        "user_id"
    )

    profile_user_id = profile[
        "user_id"
    ]

    if (
        profile_user_id is None
        or int(profile_user_id) != int(user_id)
    ):

        st.error(
            "You can only edit your own fashion profile."
        )

        return

    st.subheader(
        "✏️ Edit Fashion Profile"
    )

    st.caption(
        "Update your professional information "
        "or replace your profile image at any time."
    )

    st.divider()

    # ========================================================
    # CURRENT IMAGE
    # ========================================================

    st.markdown(
        "### 📸 Profile Image"
    )

    current_image = profile[
        "image_data"
    ]

    current_image_url = profile[
        "image_url"
    ]

    if current_image:

        display_profile_image(
            current_image,
            current_image_url
        )

    elif current_image_url:

        display_profile_image(
            None,
            current_image_url
        )

    else:

        st.info(
            "No profile image has been uploaded."
        )

    uploaded_image = st.file_uploader(
        "Change Profile Image",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ],
        accept_multiple_files=False,
        key=f"edit_profile_image_{profile_id}"
    )

    remove_image = st.checkbox(
        "Remove current profile image",
        key=f"remove_profile_image_{profile_id}"
    )

    # ========================================================
    # INFORMATION
    # ========================================================

    name = st.text_input(
        "Business / Professional Name",
        value=profile["name"] or ""
    )

    profile_type = st.selectbox(
        "Profession",
        PROFESSION_OPTIONS,
        index=(
            PROFESSION_OPTIONS.index(
                profile["profile_type"]
            )
            if profile["profile_type"]
            in PROFESSION_OPTIONS
            else 0
        ),
        key=f"edit_profession_{profile_id}"
    )

    location = st.text_input(
        "Location",
        value=profile["location"] or ""
    )

    description = st.text_area(
        "Description",
        value=profile["description"] or "",
        height=150
    )

    specialties = st.text_input(
        "Specialties",
        value=profile["specialties"] or "",
        placeholder=(
            "Native Wear, Shirts, Trousers, Streetwear"
        )
    )

    phone = st.text_input(
        "Phone Number",
        value=profile["phone"] or ""
    )

    whatsapp = st.text_input(
        "WhatsApp Number",
        value=profile["whatsapp"] or ""
    )

    st.divider()

    col1, col2 = st.columns(2)

    # ========================================================
    # SAVE
    # ========================================================

    with col1:

        if st.button(
            "💾 Save Changes",
            type="primary",
            use_container_width=True,
            key=f"save_profile_{profile_id}"
        ):

            if not name.strip():

                st.error(
                    "Please enter your name or business name."
                )

                return

            if not location.strip():

                st.error(
                    "Please enter your location."
                )

                return

            image_data = None

            image_mime_type = ""

            if uploaded_image:

                image_data, image_mime_type = (
                    validate_profile_image(
                        uploaded_image
                    )
                )

                if image_data is None:

                    return

            updated = update_profile(

                profile_id=profile_id,

                user_id=user_id,

                name=name,

                profile_type=profile_type,

                location=location,

                description=description,

                specialties=specialties,

                phone=phone,

                whatsapp=whatsapp,

                image_data=image_data,

                image_mime_type=image_mime_type,

                remove_image=remove_image
            )

            if updated:

                st.success(
                    "✅ Fashion profile updated and saved successfully."
                )

                st.session_state.profile_view = (
                    "my_profile"
                )

                st.rerun()

            else:

                st.error(
                    "Unable to update your profile. "
                    "Please check your information."
                )

    # ========================================================
    # DELETE
    # ========================================================

    with col2:

        if st.button(
            "🗑️ Delete Profile",
            use_container_width=True,
            key=f"delete_profile_{profile_id}"
        ):

            st.session_state[
                f"confirm_delete_profile_{profile_id}"
            ] = True

    # ========================================================
    # DELETE CONFIRMATION
    # ========================================================

    if st.session_state.get(
        f"confirm_delete_profile_{profile_id}",
        False
    ):

        st.warning(
            "Are you sure you want to permanently "
            "delete your fashion professional profile?"
        )

        confirm_col1, confirm_col2 = st.columns(2)

        with confirm_col1:

            if st.button(
                "Yes, Delete Profile",
                type="primary",
                use_container_width=True,
                key=f"confirm_delete_{profile_id}"
            ):

                deleted = delete_profile(
                    profile_id=profile_id,
                    user_id=user_id
                )

                st.session_state[
                    f"confirm_delete_profile_{profile_id}"
                ] = False

                if deleted:

                    st.success(
                        "Profile deleted successfully."
                    )

                    st.session_state.profile_view = (
                        "find"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to delete this profile."
                    )

        with confirm_col2:

            if st.button(
                "Cancel",
                use_container_width=True,
                key=f"cancel_delete_{profile_id}"
            ):

                st.session_state[
                    f"confirm_delete_profile_{profile_id}"
                ] = False

                st.rerun()


# ============================================================
# RENDER MY PROFILE
# ============================================================

def render_my_profile():

    user_id = st.session_state.get(
        "user_id"
    )

    if not user_id:

        st.warning(
            "Please login to manage your profile."
        )

        return

    profiles = get_user_profiles(
        user_id
    )

    st.subheader(
        "👤 My Fashion Profile"
    )

    if not profiles:

        st.info(
            "You haven't created a fashion professional "
            "profile yet."
        )

        if st.button(
            "➕ Create My Profile",
            type="primary"
        ):

            st.session_state.profile_view = (
                "create"
            )

            st.rerun()

        return

    # Normally one user profile is expected.
    # If multiple old profiles exist, display them all.

    for profile in profiles:

        with st.container(
            border=True
        ):

            col1, col2 = st.columns(
                [1, 3]
            )

            with col1:

                display_profile_image(
                    profile["image_data"],
                    profile["image_url"]
                )

            with col2:

                title = profile["name"]

                if profile["verified"]:

                    title += " ✅"

                st.subheader(
                    title
                )

                st.caption(
                    f"👤 {profile['profile_type']}"
                )

                if profile["location"]:

                    st.caption(
                        f"📍 {profile['location']}"
                    )

                if profile["description"]:

                    st.write(
                        profile["description"]
                    )

                if profile["specialties"]:

                    st.write(
                        f"✨ {profile['specialties']}"
                    )

                if profile["phone"]:

                    st.write(
                        f"📞 {profile['phone']}"
                    )

                if profile["whatsapp"]:

                    st.write(
                        f"💬 {profile['whatsapp']}"
                    )

                st.caption(
                    f"Created: {profile['created_at']}"
                )

                if st.button(
                    "✏️ Edit Profile",
                    key=f"edit_my_profile_{profile['id']}",
                    use_container_width=True
                ):

                    st.session_state.selected_profile_id = (
                        profile["id"]
                    )

                    st.session_state.profile_view = (
                        "edit"
                    )

                    st.rerun()


# ============================================================
# RENDER PROFILES
# ============================================================

def render_profiles():

    init_profiles_table()

    if "profile_view" not in st.session_state:

        st.session_state.profile_view = (
            "find"
        )

    st.title(
        "👗 Fashion Professionals"
    )

    st.write(
        "Find designers, tailors, stylists, fabric sellers "
        "and other fashion professionals."
    )

    st.divider()

    # ========================================================
    # EDIT VIEW
    # ========================================================

    if (
        st.session_state.profile_view
        == "edit"
    ):

        if st.button(
            "← Back to Fashion Professionals"
        ):

            st.session_state.profile_view = (
                "my_profile"
            )

            st.rerun()

        render_edit_profile(
            st.session_state.selected_profile_id
        )

        return

    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3 = st.tabs([
        "🔎 Find Professionals",
        "➕ Create Profile",
        "👤 My Profile"
    ])

    # ========================================================
    # FIND PROFESSIONALS
    # ========================================================

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            profession_options = [
                "All"
            ] + PROFESSION_OPTIONS

            profile_type = st.selectbox(
                "Profession",
                profession_options,
                key="find_profession"
            )

        with col2:

            location = st.text_input(
                "📍 Location",
                placeholder="e.g. Owerri",
                key="find_profession_location"
            )

        st.divider()

        profiles = get_profiles(
            profile_type=profile_type,
            location=location
        )

        if not profiles:

            st.info(
                "No professionals found. "
                "Try another profession or location."
            )

        else:

            seen = set()

            for profile in profiles:

                profile_id = profile["id"]

                name = profile["name"]

                profession = profile[
                    "profile_type"
                ]

                profile_location = profile[
                    "location"
                ]

                description = profile[
                    "description"
                ]

                specialties = profile[
                    "specialties"
                ]

                phone = profile[
                    "phone"
                ]

                whatsapp = profile[
                    "whatsapp"
                ]

                image_data = profile[
                    "image_data"
                ]

                image_url = profile[
                    "image_url"
                ]

                verified = profile[
                    "verified"
                ]

                unique_key = (

                    name.lower().strip(),

                    profession.lower().strip(),

                    profile_location.lower().strip()

                )

                if unique_key in seen:

                    continue

                seen.add(
                    unique_key
                )

                with st.container(
                    border=True
                ):

                    col1, col2 = st.columns(
                        [1, 3]
                    )

                    # ----------------------------------------
                    # IMAGE
                    # ----------------------------------------

                    with col1:

                        display_profile_image(
                            image_data,
                            image_url
                        )

                    # ----------------------------------------
                    # INFORMATION
                    # ----------------------------------------

                    with col2:

                        title = name

                        if verified:

                            title += " ✅"

                        st.subheader(
                            title
                        )

                        st.caption(
                            f"👤 {profession}"
                        )

                        if profile_location:

                            st.caption(
                                f"📍 {profile_location}"
                            )

                        if description:

                            st.write(
                                description
                            )

                        if specialties:

                            st.write(
                                f"✨ {specialties}"
                            )

                        contact_col1, contact_col2 = (
                            st.columns(2)
                        )

                        with contact_col1:

                            if whatsapp:

                                whatsapp_number = (

                                    whatsapp

                                    .replace(
                                        "+",
                                        ""
                                    )

                                    .replace(
                                        " ",
                                        ""
                                    )

                                    .replace(
                                        "-",
                                        ""
                                    )
                                )

                                if whatsapp_number.startswith(
                                    "0"
                                ):

                                    whatsapp_number = (
                                        "234"
                                        + whatsapp_number[1:]
                                    )

                                st.link_button(
                                    "💬 WhatsApp",
                                    f"https://wa.me/{whatsapp_number}",
                                    use_container_width=True
                                )

                        with contact_col2:

                            if phone:

                                phone_number = (
                                    phone
                                    .replace(
                                        " ",
                                        ""
                                    )
                                    .replace(
                                        "-",
                                        ""
                                    )
                                )

                                st.link_button(
                                    "📞 Call",
                                    f"tel:{phone_number}",
                                    use_container_width=True
                                )

    # ========================================================
    # CREATE PROFILE
    # ========================================================

    with tab2:

        st.subheader(
            "Create Your Fashion Profile"
        )

        st.write(
            "List yourself or your fashion business "
            "on StyleSense."
        )

        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------

        st.markdown(
            "### 📸 Profile Image"
        )

        st.caption(
            "Upload one professional image. "
            "You can replace it later."
        )

        profile_image = st.file_uploader(
            "Upload Profile Image",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ],
            accept_multiple_files=False,
            key="create_profile_image"
        )

        if profile_image:

            image_bytes = profile_image.getvalue()

            if len(image_bytes) <= MAX_IMAGE_SIZE:

                st.image(
                    image_bytes,
                    width=180
                )

            else:

                st.error(
                    "Profile image must be smaller than 5 MB."
                )

        # ----------------------------------------------------
        # NAME
        # ----------------------------------------------------

        name = st.text_input(
            "Business / Professional Name",
            placeholder="e.g. Chekwube Fashion House",
            key="create_profile_name"
        )

        # ----------------------------------------------------
        # PROFESSION
        # ----------------------------------------------------

        profession = st.selectbox(
            "Profession",
            PROFESSION_OPTIONS,
            key="create_profession"
        )

        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------

        location = st.text_input(
            "Location",
            placeholder="Owerri, Nigeria",
            key="create_profile_location"
        )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = st.text_area(
            "Description",
            placeholder=(
                "Tell customers what you do..."
            ),
            key="create_profile_description"
        )

        # ----------------------------------------------------
        # SPECIALTIES
        # ----------------------------------------------------

        specialties = st.text_input(
            "Specialties",
            placeholder=(
                "Native Wear, Shirts, Trousers, Streetwear"
            ),
            key="create_profile_specialties"
        )

        # ----------------------------------------------------
        # PHONE
        # ----------------------------------------------------

        phone = st.text_input(
            "Phone Number",
            placeholder="08012345678",
            key="create_profile_phone"
        )

        # ----------------------------------------------------
        # WHATSAPP
        # ----------------------------------------------------

        whatsapp = st.text_input(
            "WhatsApp Number",
            placeholder="2348012345678",
            key="create_profile_whatsapp"
        )

        st.divider()

        # ----------------------------------------------------
        # PUBLISH
        # ----------------------------------------------------

        if st.button(
            "🚀 Publish Profile",
            type="primary",
            use_container_width=True,
            key="publish_profile"
        ):

            if not name.strip():

                st.error(
                    "Please enter your name or business name."
                )

                return

            if not location.strip():

                st.error(
                    "Please enter your location."
                )

                return

            image_data = None

            image_mime_type = ""

            if profile_image:

                image_data, image_mime_type = (
                    validate_profile_image(
                        profile_image
                    )
                )

                if image_data is None:

                    return

            profile_id = create_profile(

                user_id=st.session_state.user_id,

                name=name,

                profile_type=profession,

                location=location,

                description=description,

                specialties=specialties,

                phone=phone,

                whatsapp=whatsapp,

                image_data=image_data,

                image_mime_type=image_mime_type
            )

            if profile_id is None:

                st.warning(
                    "⚠️ A profile with the same name, "
                    "profession and location already exists."
                )

                return

            st.success(
                "✅ Your fashion profile has been "
                "published and saved successfully!"
            )

            st.session_state.profile_view = (
                "my_profile"
            )

            st.rerun()

    # ========================================================
    # MY PROFILE
    # ========================================================

    with tab3:

        render_my_profile()