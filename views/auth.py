import streamlit as st

from database.users import (
    create_user,
    authenticate_user,
    get_google_login_url,
)


# ============================================================
# REGISTER
# ============================================================

def render_register():

    st.title("👗 Create Your StyleSense Account")

    st.write(
        "Join StyleSense AI OS and access your fashion workspace."
    )

    st.divider()

    # --------------------------------------------------------
    # FULL NAME
    # --------------------------------------------------------

    full_name = st.text_input(
        "Full Name",
        placeholder="Enter your full name",
        key="register_full_name"
    )

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    email = st.text_input(
        "Email",
        placeholder="you@example.com",
        key="register_email"
    )

    # --------------------------------------------------------
    # PASSWORD
    # --------------------------------------------------------

    password = st.text_input(
        "Password",
        type="password",
        placeholder="At least 6 characters",
        key="register_password"
    )

    # --------------------------------------------------------
    # CONFIRM PASSWORD
    # --------------------------------------------------------

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="register_confirm_password"
    )

    # --------------------------------------------------------
    # CREATE ACCOUNT
    # --------------------------------------------------------

    if st.button(
        "Create Account",
        type="primary",
        use_container_width=True
    ):

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not full_name.strip():

            st.error(
                "Please enter your full name."
            )

            return

        if not email.strip():

            st.error(
                "Please enter your email."
            )

            return

        if not password:

            st.error(
                "Please enter a password."
            )

            return

        if len(password) < 6:

            st.error(
                "Password must be at least 6 characters."
            )

            return

        if password != confirm_password:

            st.error(
                "Passwords do not match."
            )

            return

        # ----------------------------------------------------
        # CREATE USER
        # ----------------------------------------------------

        success, result = create_user(
            full_name=full_name,
            email=email,
            password=password
        )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if success:

            if isinstance(result, str):

                st.success(
                    f"✅ {result}"
                )

            else:

                st.success(
                    "✅ Account created successfully!"
                )

            st.info(
                "If email confirmation is enabled in "
                "Supabase, check your email before logging in."
            )

            # Move user to login page
            st.session_state.auth_page = "login"

            st.rerun()

        # ----------------------------------------------------
        # ERROR
        # ----------------------------------------------------

        else:

            st.error(
                f"❌ {result}"
            )

    # ========================================================
    # GOOGLE SIGN UP
    # ========================================================

    st.divider()

    st.subheader(
        "Or"
    )

    google_url = get_google_login_url()

    if google_url:

        st.link_button(
            "🔵 Sign up with Google",
            google_url,
            use_container_width=True
        )

    else:

        st.warning(
            "Google sign-in is currently unavailable. "
            "Please check your OAuth configuration."
        )

    # ========================================================
    # LOGIN
    # ========================================================

    st.divider()

    if st.button(
        "Already have an account? Login",
        use_container_width=True
    ):

        st.session_state.auth_page = "login"

        st.rerun()


# ============================================================
# LOGIN
# ============================================================

def render_login():

    st.title("👋 Welcome Back")

    st.write(
        "Login to your StyleSense AI OS account."
    )

    st.divider()

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    email = st.text_input(
        "Email",
        placeholder="you@example.com",
        key="login_email"
    )

    # --------------------------------------------------------
    # PASSWORD
    # --------------------------------------------------------

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="login_password"
    )

    # --------------------------------------------------------
    # EMAIL / PASSWORD LOGIN
    # --------------------------------------------------------

    if st.button(
        "🔐 Login",
        type="primary",
        use_container_width=True
    ):

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not email.strip():

            st.error(
                "Please enter your email."
            )

            return

        if not password:

            st.error(
                "Please enter your password."
            )

            return

        # ----------------------------------------------------
        # AUTHENTICATE
        # ----------------------------------------------------

        user = authenticate_user(
            email=email,
            password=password
        )

        # ----------------------------------------------------
        # LOGIN SUCCESS
        # ----------------------------------------------------

        if user:

            (
                user_id,
                full_name,
                user_email
            ) = user

            st.session_state.logged_in = True

            st.session_state.user_id = (
                user_id
            )

            st.session_state.user_name = (
                full_name
            )

            st.session_state.user_email = (
                user_email
            )

            st.session_state.auth_page = "login"

            st.success(
                f"Welcome back, {full_name}! 👋"
            )

            st.rerun()

        # ----------------------------------------------------
        # LOGIN FAILED
        # ----------------------------------------------------

        else:

            st.error(
                "❌ Invalid email or password."
            )

            st.info(
                "If you just created your account, "
                "make sure you have verified your email."
            )

    # ========================================================
    # GOOGLE LOGIN
    # ========================================================

    st.divider()

    st.subheader(
        "Or continue with"
    )

    google_url = get_google_login_url()

    if google_url:

        st.link_button(
            "🔵 Continue with Google",
            google_url,
            use_container_width=True
        )

    else:

        st.warning(
            "Google sign-in is currently unavailable. "
            "Please check your OAuth configuration."
        )

    # ========================================================
    # REGISTER
    # ========================================================

    st.divider()

    if st.button(
        "Create a new account",
        use_container_width=True
    ):

        st.session_state.auth_page = "register"

        st.rerun()


# ============================================================
# AUTH ROUTER
# ============================================================

def render_auth():

    # --------------------------------------------------------
    # DEFAULT AUTH PAGE
    # --------------------------------------------------------

    if "auth_page" not in st.session_state:

        st.session_state.auth_page = "login"

    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    if st.session_state.auth_page == "register":

        render_register()

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    else:

        render_login()