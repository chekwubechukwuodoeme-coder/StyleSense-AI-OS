import streamlit as st

from database.profiles import (
    init_profiles_table,
    create_profile,
    get_profiles
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

    "Other"
]


# ============================================================
# RENDER PROFILES
# ============================================================

def render_profiles():

    # Make sure database exists
    init_profiles_table()

    st.title("👗 Fashion Professionals")

    st.write(
        "Find designers, tailors, stylists, fabric sellers "
        "and other fashion professionals."
    )

    st.divider()

    tab1, tab2 = st.tabs([
        "🔎 Find Professionals",
        "➕ Create Profile"
    ])

    # ========================================================
    # FIND PROFESSIONALS
    # ========================================================

    with tab1:

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # PROFESSION FILTER
        # ----------------------------------------------------

        with col1:

            profession_options = [
                "All"
            ] + PROFESSION_OPTIONS

            profile_type = st.selectbox(
                "Profession",
                profession_options
            )

        # ----------------------------------------------------
        # LOCATION FILTER
        # ----------------------------------------------------

        with col2:

            location = st.text_input(
                "📍 Location",
                placeholder="e.g. Owerri"
            )

        st.divider()

        # ----------------------------------------------------
        # GET PROFILES
        # ----------------------------------------------------

        profiles = get_profiles(
            profile_type=profile_type,
            location=location
        )

        # ----------------------------------------------------
        # NO RESULTS
        # ----------------------------------------------------

        if not profiles:

            st.info(
                "No professionals found. "
                "Try another profession or location."
            )

        # ----------------------------------------------------
        # DISPLAY PROFILES
        # ----------------------------------------------------

        else:

            # Prevent duplicate display
            seen = set()

            for profile in profiles:

                (
                    profile_id,
                    name,
                    profession,
                    profile_location,
                    description,
                    specialties,
                    phone,
                    whatsapp,
                    image_url,
                    verified,
                    created_at
                ) = profile

                # --------------------------------------------
                # DUPLICATE CHECK
                # --------------------------------------------

                unique_key = (
                    name.lower().strip(),
                    profession.lower().strip(),
                    profile_location.lower().strip()
                )

                if unique_key in seen:
                    continue

                seen.add(unique_key)

                # --------------------------------------------
                # PROFILE CARD
                # --------------------------------------------

                with st.container(border=True):

                    col1, col2 = st.columns([1, 3])

                    # ----------------------------------------
                    # IMAGE
                    # ----------------------------------------

                    with col1:

                        if image_url:

                            try:

                                st.image(
                                    image_url,
                                    use_container_width=True
                                )

                            except Exception:

                                st.markdown("## 👤")

                        else:

                            st.markdown("## 👤")

                    # ----------------------------------------
                    # PROFILE INFORMATION
                    # ----------------------------------------

                    with col2:

                        title = name

                        if verified:

                            title += " ✅"

                        st.subheader(title)

                        st.caption(
                            f"👤 {profession}"
                        )

                        if profile_location:

                            st.caption(
                                f"📍 {profile_location}"
                            )

                        if description:

                            st.write(description)

                        if specialties:

                            st.write(
                                f"✨ {specialties}"
                            )

                        # ------------------------------------
                        # CONTACT
                        # ------------------------------------

                        contact_col1, contact_col2 = st.columns(2)

                        with contact_col1:

                            if whatsapp:

                                whatsapp_number = (
                                    whatsapp
                                    .replace("+", "")
                                    .replace(" ", "")
                                    .replace("-", "")
                                )

                                st.link_button(
                                    "💬 WhatsApp",
                                    f"https://wa.me/{whatsapp_number}"
                                )

                        with contact_col2:

                            if phone:

                                st.write(
                                    f"📞 {phone}"
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
        # NAME
        # ----------------------------------------------------

        name = st.text_input(
            "Business / Professional Name",
            placeholder="e.g. Chekwube Fashion House"
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
            placeholder="Owerri, Nigeria"
        )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = st.text_area(
            "Description",
            placeholder=(
                "Tell customers what you do..."
            )
        )

        # ----------------------------------------------------
        # SPECIALTIES
        # ----------------------------------------------------

        specialties = st.text_input(
            "Specialties",
            placeholder=(
                "Native Wear, Shirts, Trousers, Streetwear"
            )
        )

        # ----------------------------------------------------
        # PHONE
        # ----------------------------------------------------

        phone = st.text_input(
            "Phone Number",
            placeholder="08012345678"
        )

        # ----------------------------------------------------
        # WHATSAPP
        # ----------------------------------------------------

        whatsapp = st.text_input(
            "WhatsApp Number",
            placeholder="2348012345678"
        )

        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------

        image_url = st.text_input(
            "Profile Image URL",
            placeholder="https://..."
        )

        st.divider()

        # ----------------------------------------------------
        # PUBLISH
        # ----------------------------------------------------

        if st.button(
            "🚀 Publish Profile",
            type="primary",
            use_container_width=True
        ):

            # -----------------------------------------------
            # VALIDATION
            # -----------------------------------------------

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

            # -----------------------------------------------
            # CREATE PROFILE
            # -----------------------------------------------

            profile_id = create_profile(
                name=name,
                profile_type=profession,
                location=location,
                description=description,
                specialties=specialties,
                phone=phone,
                whatsapp=whatsapp,
                image_url=image_url
            )

            # -----------------------------------------------
            # DUPLICATE
            # -----------------------------------------------

            if profile_id is None:

                st.warning(
                    "⚠️ A profile with the same name, "
                    "profession and location already exists."
                )

                return

            # -----------------------------------------------
            # SUCCESS
            # -----------------------------------------------

            st.success(
                "✅ Your fashion profile has been published!"
            )

            st.rerun()