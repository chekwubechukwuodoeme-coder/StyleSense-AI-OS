import streamlit as st

from database.users import (
    update_user_profile,
    upload_profile_image,
)


# ============================================================
# SETTINGS PAGE
# ============================================================

def render_settings():

    # ========================================================
    # SESSION STATE
    # ========================================================

    if "settings_section" not in st.session_state:
        st.session_state.settings_section = "Account"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "saved_designs" not in st.session_state:
        st.session_state.saved_designs = []

    # ========================================================
    # SETTINGS HEADER
    # ========================================================

    st.title("⚙️ Settings")

    st.caption(
        "Customize and manage your StyleSense AI experience."
    )

    st.divider()

    # ========================================================
    # SETTINGS NAVIGATION
    # ========================================================

    settings_sections = [
        ("👤", "Account"),
        ("🎨", "Appearance"),
        ("🤖", "AI Preferences"),
        ("👗", "Fashion Preferences"),
        ("🔔", "Notifications"),
        ("💬", "Chat & Data"),
        ("📚", "Design Library"),
        ("🛍️", "Marketplace"),
        ("🌍", "Regional Settings"),
        ("🔐", "Privacy & Security"),
        ("⚙️", "Advanced"),
    ]

    for i, (icon, name) in enumerate(settings_sections):

        if st.button(
            f"{icon}  {name}",
            key=f"settings_nav_{i}",
            use_container_width=True,
        ):

            st.session_state.settings_section = name

            st.rerun()

    st.divider()

    # ========================================================
    # CURRENT SECTION
    # ========================================================

    selected = st.session_state.settings_section

    # ========================================================
    # ACCOUNT
    # ========================================================

    if selected == "Account":

        st.header("👤 Account")

        st.caption(
            "Manage your personal information and profile picture."
        )

        st.divider()

        # ----------------------------------------------------
        # CURRENT PROFILE DATA
        # ----------------------------------------------------

        current_name = (
            st.session_state.get("user_name")
            or ""
        )

        current_profession = (
            st.session_state.get("user_profession")
            or "Fashion Designer"
        )

        current_avatar = (
            st.session_state.get("user_avatar_url")
            or ""
        )

        # ----------------------------------------------------
        # PROFILE PICTURE
        # ----------------------------------------------------

        st.subheader("Profile Picture")

        if current_avatar:

            st.image(
                current_avatar,
                width=120,
            )

        else:

            first_letter = (
                current_name[:1].upper()
                if current_name
                else "U"
            )

            st.write(
                f"Current profile initial: {first_letter}"
            )

        uploaded_avatar = st.file_uploader(
            "Choose a new profile picture",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp",
            ],
            key="profile_avatar_upload",
            help="Upload a JPG, JPEG, PNG or WEBP image.",
        )

        if uploaded_avatar:

            st.image(
                uploaded_avatar,
                width=120,
                caption="New profile picture",
            )

        remove_avatar = False

        if current_avatar:

            remove_avatar = st.checkbox(
                "Remove current profile picture",
                key="remove_profile_avatar",
            )

        st.divider()

        # ----------------------------------------------------
        # PROFILE INFORMATION
        # ----------------------------------------------------

        st.subheader("Profile Information")

        profile_name = st.text_input(
            "Full Name",
            value=current_name,
            key="settings_profile_name",
        )

        profile_profession = st.text_input(
            "Profession",
            value=current_profession,
            key="settings_profile_profession",
            placeholder="Fashion Designer",
        )

        # ----------------------------------------------------
        # SAVE PROFILE
        # ----------------------------------------------------

        if st.button(
            "Save Profile Changes",
            type="primary",
            use_container_width=True,
            key="save_profile_changes",
        ):

            if not profile_name.strip():

                st.error(
                    "Please enter your full name."
                )

                st.stop()

            if not profile_profession.strip():

                st.error(
                    "Please enter your profession."
                )

                st.stop()

            # Start with current avatar
            avatar_url = current_avatar

            # Remove avatar
            if remove_avatar:

                avatar_url = ""

            # Upload new avatar
            elif uploaded_avatar:

                with st.spinner(
                    "Uploading profile picture..."
                ):

                    (
                        upload_success,
                        new_avatar_url,
                        upload_message,
                    ) = upload_profile_image(
                        uploaded_avatar
                    )

                if not upload_success:

                    st.error(
                        upload_message
                    )

                    st.stop()

                avatar_url = new_avatar_url

            # Save profile
            success, message = update_user_profile(
                profile_name.strip(),
                profile_profession.strip(),
                avatar_url,
            )

            if success:

                st.session_state.user_name = (
                    profile_name.strip()
                )

                st.session_state.user_profession = (
                    profile_profession.strip()
                )

                st.session_state.user_avatar_url = (
                    avatar_url
                )

                st.session_state.open_profile_settings = (
                    False
                )

                st.success(
                    "Profile updated successfully."
                )

                st.rerun()

            else:

                st.error(
                    message
                )

    # ========================================================
    # APPEARANCE
    # ========================================================

    elif selected == "Appearance":

        st.header("🎨 Appearance")

        st.caption(
            "Customize how StyleSense looks across your workspace."
        )

        st.divider()

        # ----------------------------------------------------
        # THEME
        # ----------------------------------------------------

        appearance = st.selectbox(
            "Theme",
            [
                "System Default",
                "Light",
                "Dark",
            ],
            key="settings_appearance_theme",
        )

        # ----------------------------------------------------
        # ACCENT COLOR
        # ----------------------------------------------------

        accent_color = st.selectbox(
            "Accent Color",
            [
                "Emerald",
                "Amber",
                "Electric Lime",
                "Charcoal",
            ],
            key="settings_accent_color",
        )

        # ----------------------------------------------------
        # DENSITY
        # ----------------------------------------------------

        interface_density = st.selectbox(
            "Interface Density",
            [
                "Comfortable",
                "Compact",
                "Spacious",
            ],
            key="settings_interface_density",
        )

        # ----------------------------------------------------
        # ANIMATIONS
        # ----------------------------------------------------

        enable_animations = st.toggle(
            "Enable interface animations",
            value=True,
            key="settings_animations",
        )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        if st.button(
            "Save Appearance",
            type="primary",
            use_container_width=True,
            key="save_appearance",
        ):

            st.session_state.appearance_theme = appearance
            st.session_state.accent_color = accent_color
            st.session_state.interface_density = (
                interface_density
            )
            st.session_state.enable_animations = (
                enable_animations
            )

            st.success(
                "Appearance preferences saved."
            )

    # ========================================================
    # AI PREFERENCES
    # ========================================================

    elif selected == "AI Preferences":

        st.header("🤖 AI Preferences")

        st.caption(
            "Control how StyleSense AI works with you."
        )

        st.divider()

        # ----------------------------------------------------
        # CREATIVITY
        # ----------------------------------------------------

        ai_creativity = st.slider(
            "AI Creativity",
            min_value=1,
            max_value=10,
            value=7,
            help=(
                "Higher values make AI responses more "
                "creative and experimental."
            ),
            key="settings_ai_creativity",
        )

        # ----------------------------------------------------
        # RESPONSE STYLE
        # ----------------------------------------------------

        response_style = st.selectbox(
            "AI Response Style",
            [
                "Professional",
                "Creative",
                "Concise",
                "Detailed",
                "Friendly",
            ],
            key="settings_ai_response_style",
        )

        # ----------------------------------------------------
        # PROMPT ENHANCEMENT
        # ----------------------------------------------------

        enhance_prompts = st.toggle(
            "Automatically enhance my prompts",
            value=True,
            key="settings_enhance_prompts",
        )

        # ----------------------------------------------------
        # DESIGN RECOMMENDATIONS
        # ----------------------------------------------------

        design_recommendations = st.toggle(
            "Enable AI design recommendations",
            value=True,
            key="settings_design_recommendations",
        )

        # ----------------------------------------------------
        # AI MEMORY
        # ----------------------------------------------------

        remember_preferences = st.toggle(
            "Remember my fashion preferences",
            value=True,
            key="settings_remember_preferences",
        )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        if st.button(
            "Save AI Preferences",
            type="primary",
            use_container_width=True,
            key="save_ai_preferences",
        ):

            st.session_state.ai_creativity = (
                ai_creativity
            )

            st.session_state.ai_response_style = (
                response_style
            )

            st.session_state.enhance_prompts = (
                enhance_prompts
            )

            st.session_state.design_recommendations = (
                design_recommendations
            )

            st.session_state.remember_preferences = (
                remember_preferences
            )

            st.success(
                "AI preferences saved."
            )

    # ========================================================
    # FASHION PREFERENCES
    # ========================================================

    elif selected == "Fashion Preferences":

        st.header("👗 Fashion Preferences")

        st.caption(
            "Tell StyleSense what kind of fashion you create."
        )

        st.divider()

        # ----------------------------------------------------
        # FASHION CATEGORY
        # ----------------------------------------------------

        fashion_categories = st.multiselect(
            "Fashion Categories",
            [
                "Luxury",
                "Streetwear",
                "Casual",
                "Evening Wear",
                "Bridal",
                "African Fashion",
                "Menswear",
                "Womenswear",
                "Sportswear",
                "Ready-to-Wear",
            ],
            key="settings_fashion_categories",
        )

        # ----------------------------------------------------
        # FAVORITE STYLES
        # ----------------------------------------------------

        favorite_styles = st.multiselect(
            "Preferred Styles",
            [
                "Minimalist",
                "Classic",
                "Modern",
                "Avant-Garde",
                "Elegant",
                "Bold",
                "Traditional",
                "Contemporary",
                "Experimental",
            ],
            key="settings_favorite_styles",
        )

        # ----------------------------------------------------
        # FAVORITE FABRICS
        # ----------------------------------------------------

        favorite_fabrics = st.multiselect(
            "Preferred Fabrics",
            [
                "Silk",
                "Cotton",
                "Linen",
                "Denim",
                "Velvet",
                "Chiffon",
                "Lace",
                "Ankara",
                "Adire",
                "Leather",
            ],
            key="settings_favorite_fabrics",
        )

        # ----------------------------------------------------
        # COLOR PALETTE
        # ----------------------------------------------------

        preferred_colors = st.multiselect(
            "Preferred Colors",
            [
                "Rich Emerald Green",
                "Warm Amber",
                "Electric Lime Green",
                "Deep Slate Charcoal",
                "Black",
                "White",
                "Gold",
                "Orange",
                "Royal Blue",
                "Burgundy",
            ],
            key="settings_preferred_colors",
        )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        if st.button(
            "Save Fashion Preferences",
            type="primary",
            use_container_width=True,
            key="save_fashion_preferences",
        ):

            st.session_state.fashion_categories = (
                fashion_categories
            )

            st.session_state.favorite_styles = (
                favorite_styles
            )

            st.session_state.favorite_fabrics = (
                favorite_fabrics
            )

            st.session_state.preferred_colors = (
                preferred_colors
            )

            st.success(
                "Fashion preferences saved."
            )

    # ========================================================
    # NOTIFICATIONS
    # ========================================================

    elif selected == "Notifications":

        st.header("🔔 Notifications")

        st.caption(
            "Choose which StyleSense notifications you receive."
        )

        st.divider()

        email_notifications = st.toggle(
            "Email Notifications",
            value=True,
            key="settings_email_notifications",
        )

        ai_notifications = st.toggle(
            "AI Updates",
            value=True,
            key="settings_ai_notifications",
        )

        trend_notifications = st.toggle(
            "Fashion Trend Alerts",
            value=True,
            key="settings_trend_notifications",
        )

        marketplace_notifications = st.toggle(
            "Marketplace Notifications",
            value=True,
            key="settings_marketplace_notifications",
        )

        project_notifications = st.toggle(
            "Project Notifications",
            value=True,
            key="settings_project_notifications",
        )

        if st.button(
            "Save Notification Settings",
            type="primary",
            use_container_width=True,
            key="save_notifications",
        ):

            st.success(
                "Notification settings saved."
            )

    # ========================================================
    # CHAT & DATA
    # ========================================================

    elif selected == "Chat & Data":

        st.header("💬 Chat & Data")

        st.caption(
            "Manage your conversations and workspace data."
        )

        st.divider()

        st.subheader("Chat History")

        st.write(
            f"You currently have "
            f"{len(st.session_state.messages)} "
            f"messages in your current session."
        )

        if st.button(
            "🗑 Clear Chat History",
            use_container_width=True,
            key="clear_chat_history",
        ):

            st.session_state.messages = []

            st.success(
                "Chat history cleared."
            )

        st.divider()

        st.subheader("Workspace Data")

        st.write(
            "Your StyleSense workspace contains your "
            "projects, designs and AI activity."
        )

        if st.button(
            "Reset Current Session",
            use_container_width=True,
            key="reset_current_session",
        ):

            st.session_state.messages = []
            st.session_state.saved_designs = []

            st.success(
                "Current session data has been reset."
            )

    # ========================================================
    # DESIGN LIBRARY
    # ========================================================

    elif selected == "Design Library":

        st.header("📚 Design Library")

        st.caption(
            "Manage your saved AI fashion designs."
        )

        st.divider()

        st.write(
            f"Saved designs in this session: "
            f"{len(st.session_state.saved_designs)}"
        )

        if st.button(
            "🗑 Delete All Saved Designs",
            use_container_width=True,
            key="delete_saved_designs",
        ):

            st.session_state.saved_designs = []

            st.success(
                "All saved designs deleted."
            )

    # ========================================================
    # MARKETPLACE
    # ========================================================

    elif selected == "Marketplace":

        st.header("🛍️ Marketplace")

        st.caption(
            "Manage your StyleSense marketplace preferences."
        )

        st.divider()

        marketplace_visibility = st.selectbox(
            "Marketplace Visibility",
            [
                "Visible to everyone",
                "Visible to registered users",
                "Private",
            ],
            key="settings_marketplace_visibility",
        )

        allow_messages = st.toggle(
            "Allow buyers to contact me",
            value=True,
            key="settings_marketplace_messages",
        )

        show_contact_information = st.toggle(
            "Show contact information on listings",
            value=False,
            key="settings_marketplace_contact",
        )

        if st.button(
            "Save Marketplace Settings",
            type="primary",
            use_container_width=True,
            key="save_marketplace",
        ):

            st.success(
                "Marketplace settings saved."
            )

    # ========================================================
    # REGIONAL SETTINGS
    # ========================================================

    elif selected == "Regional Settings":

        st.header("🌍 Regional Settings")

        st.caption(
            "Manage language, currency and measurement preferences."
        )

        st.divider()

        language = st.selectbox(
            "Language",
            [
                "English",
            ],
            key="settings_language",
        )

        currency = st.selectbox(
            "Currency",
            [
                "NGN — Nigerian Naira",
                "USD — US Dollar",
                "GBP — British Pound",
                "EUR — Euro",
            ],
            key="settings_currency",
        )

        measurement = st.selectbox(
            "Measurement System",
            [
                "Metric",
                "Imperial",
            ],
            key="settings_measurement",
        )

        timezone = st.selectbox(
            "Time Zone",
            [
                "Africa/Lagos",
                "UTC",
                "Europe/London",
                "America/New_York",
            ],
            key="settings_timezone",
        )

        if st.button(
            "Save Regional Settings",
            type="primary",
            use_container_width=True,
            key="save_regional",
        ):

            st.success(
                "Regional settings saved."
            )

    # ========================================================
    # PRIVACY & SECURITY
    # ========================================================

    elif selected == "Privacy & Security":

        st.header("🔐 Privacy & Security")

        st.caption(
            "Manage your account privacy and security."
        )

        st.divider()

        st.subheader("Privacy")

        personalized_ai = st.toggle(
            "Allow personalized AI recommendations",
            value=True,
            key="settings_personalized_ai",
        )

        usage_analytics = st.toggle(
            "Allow anonymous usage analytics",
            value=True,
            key="settings_usage_analytics",
        )

        st.divider()

        st.subheader("Security")

        login_notifications = st.toggle(
            "Login notifications",
            value=True,
            key="settings_login_notifications",
        )

        if st.button(
            "Save Privacy Settings",
            type="primary",
            use_container_width=True,
            key="save_privacy",
        ):

            st.success(
                "Privacy and security settings saved."
            )

    # ========================================================
    # ADVANCED
    # ========================================================

    elif selected == "Advanced":

        st.header("⚙️ Advanced")

        st.caption(
            "Advanced StyleSense configuration."
        )

        st.divider()

        debug_mode = st.toggle(
            "Developer / Debug Mode",
            value=False,
            key="settings_debug_mode",
        )

        experimental_features = st.toggle(
            "Enable Experimental AI Features",
            value=False,
            key="settings_experimental_features",
        )

        confirm_actions = st.toggle(
            "Confirm destructive actions",
            value=True,
            key="settings_confirm_actions",
        )

        if st.button(
            "Save Advanced Settings",
            type="primary",
            use_container_width=True,
            key="save_advanced",
        ):

            st.success(
                "Advanced settings saved."
            )