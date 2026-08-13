import streamlit as st

from database.users import (
    create_user,
    authenticate_user,
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

    full_name = st.text_input(
        "Full Name",
        placeholder="Enter your full name",
        key="register_full_name"
    )

    email = st.text_input(
        "Email",
        placeholder="you@example.com",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="At least 6 characters",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="register_confirm_password"
    )

    if st.button(
        "Create Account",
        type="primary",
        use_container_width=True
    ):

        if password != confirm_password:

            st.error("Passwords do not match.")

            return

        success, result = create_user(
            full_name=full_name,
            email=email,
            password=password
        )

        if success:

            st.success(
                "✅ Account created successfully!"
            )

            st.session_state.auth_page = "login"

            st.rerun()

        else:

            st.error(result)

    st.divider()

    if st.button(
        "Already have an account? Login"
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

    email = st.text_input(
        "Email",
        placeholder="you@example.com",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "🔐 Login",
        type="primary",
        use_container_width=True
    ):

        if not email or not password:

            st.error(
                "Please enter your email and password."
            )

            return

        user = authenticate_user(
            email=email,
            password=password
        )

        if user:

            user_id, full_name, user_email = user

            st.session_state.logged_in = True

            st.session_state.user_id = user_id

            st.session_state.user_name = full_name

            st.session_state.user_email = user_email

            st.session_state.auth_page = "login"

            st.success(
                f"Welcome back, {full_name}! 👋"
            )

            st.rerun()

        else:

            st.error(
                "❌ Invalid email or password."
            )

    st.divider()

    if st.button(
        "Create a new account"
    ):

        st.session_state.auth_page = "register"

        st.rerun()


# ============================================================
# AUTH ROUTER
# ============================================================

def render_auth():

    if "auth_page" not in st.session_state:

        st.session_state.auth_page = "login"

    if st.session_state.auth_page == "register":

        render_register()

    else:

        render_login()