import streamlit as st
from supabase import create_client


# ============================================================
# SUPABASE CONFIGURATION
# ============================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


# ============================================================
# SUPABASE CLIENT
# ============================================================

def get_supabase():
    """
    Create and return the Supabase client.
    """

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )


# ============================================================
# REGISTER USER
# ============================================================

def create_user(
    full_name,
    email,
    password
):
    """
    Create a new StyleSense user using Supabase Auth.
    """

    full_name = full_name.strip()
    email = email.strip().lower()

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not full_name:
        return False, "Please enter your full name."

    if not email:
        return False, "Please enter your email."

    if not password:
        return False, "Please enter a password."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    try:

        supabase = get_supabase()

        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name
                    }
                }
            }
        )

        # ----------------------------------------------------
        # CHECK RESPONSE
        # ----------------------------------------------------

        if not response.user:

            return (
                False,
                "Unable to create account."
            )

        # ----------------------------------------------------
        # IMPORTANT:
        # If Supabase email confirmation is enabled,
        # the account is created but the user must verify
        # their email before normal password login.
        # ----------------------------------------------------

        if response.session is None:

            return (
                True,
                "Account created successfully. "
                "Please check your email and verify your account "
                "before logging in."
            )

        return (
            True,
            response.user
        )

    except Exception as e:

        error_message = str(e)

        if "already registered" in error_message.lower():

            return (
                False,
                "An account with this email already exists."
            )

        if "user already registered" in error_message.lower():

            return (
                False,
                "An account with this email already exists."
            )

        return (
            False,
            error_message
        )


# ============================================================
# EMAIL / PASSWORD LOGIN
# ============================================================

def authenticate_user(
    email,
    password
):
    """
    Authenticate a user using email and password.

    Returns:

        (
            user_id,
            full_name,
            email
        )

    or None if authentication fails.
    """

    email = email.strip().lower()

    if not email or not password:

        return None

    try:

        supabase = get_supabase()

        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        # ----------------------------------------------------
        # CHECK USER
        # ----------------------------------------------------

        if not response.user:

            return None

        user = response.user

        # ----------------------------------------------------
        # USER ID
        # ----------------------------------------------------

        user_id = user.id

        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        user_email = user.email

        # ----------------------------------------------------
        # FULL NAME
        # ----------------------------------------------------

        full_name = None

        if user.user_metadata:

            full_name = user.user_metadata.get(
                "full_name"
            )

        # ----------------------------------------------------
        # FALLBACK NAME
        # ----------------------------------------------------

        if not full_name:

            full_name = (
                user_email.split("@")[0]
                if user_email
                else "User"
            )

        return (
            user_id,
            full_name,
            user_email
        )

    except Exception:

        return None


# ============================================================
# GOOGLE LOGIN
# ============================================================

def get_google_login_url():

    try:
        supabase = get_supabase()

        redirect_url = st.secrets["GOOGLE_REDIRECT_URL"].rstrip("/")

        response = supabase.auth.sign_in_with_oauth(
            {
                "provider": "google",
                "options": {
                    "redirect_to": redirect_url
                }
            }
        )

        return response.url

    except Exception as e:
        print("GOOGLE LOGIN ERROR:", repr(e))
        return None


# ============================================================
# GOOGLE CALLBACK
# ============================================================

def handle_google_callback(oauth_code):

    if not oauth_code:
        return None

    try:
        supabase = get_supabase()

        response = supabase.auth.exchange_code_for_session(
            {
                "auth_code": oauth_code
            }
        )

        user = None

        if hasattr(response, "user"):
            user = response.user

        if user is None and hasattr(response, "session"):
            session = response.session

            if session and hasattr(session, "user"):
                user = session.user

        if user is None:
            return get_current_user()

        full_name = None

        if user.user_metadata:
            full_name = (
                user.user_metadata.get("full_name")
                or user.user_metadata.get("name")
            )

        if not full_name:
            full_name = (
                user.email.split("@")[0]
                if user.email
                else "User"
            )

        return {
            "id": user.id,
            "full_name": full_name,
            "email": user.email
        }

    except Exception as e:
        print(
            "GOOGLE CALLBACK ERROR:",
            repr(e)
        )
        return None

        # ----------------------------------------------------
        # CHECK USER
        # ----------------------------------------------------

        if not response:

            return None

        if not response.user:

            return None

        user = response.user

        # ----------------------------------------------------
        # USER ID
        # ----------------------------------------------------

        user_id = user.id

        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        user_email = user.email

        # ----------------------------------------------------
        # FULL NAME
        # ----------------------------------------------------

        full_name = None

        if user.user_metadata:

            full_name = user.user_metadata.get(
                "full_name"
            )

        # Google sometimes provides the name
        # under different metadata fields.

        if not full_name and user.user_metadata:

            full_name = user.user_metadata.get(
                "name"
            )

        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        if not full_name:

            if user_email:

                full_name = (
                    user_email.split("@")[0]
                )

            else:

                full_name = "User"

        return {
            "id": user_id,
            "full_name": full_name,
            "email": user_email
        }

    except Exception as e:

        print(
            "GOOGLE CALLBACK ERROR:",
            repr(e)
        )

        return None


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user():
    """
    Return the currently authenticated Supabase user.
    """

    try:

        supabase = get_supabase()

        response = supabase.auth.get_user()

        if not response:

            return None

        if not response.user:

            return None

        user = response.user

        # ----------------------------------------------------
        # FULL NAME
        # ----------------------------------------------------

        full_name = None

        if user.user_metadata:

            full_name = user.user_metadata.get(
                "full_name"
            )

        if not full_name and user.user_metadata:

            full_name = user.user_metadata.get(
                "name"
            )

        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        if not full_name:

            if user.email:

                full_name = (
                    user.email.split("@")[0]
                )

            else:

                full_name = "User"

        return {
            "id": user.id,
            "full_name": full_name,
            "email": user.email
        }

    except Exception as e:

        print(
            "GET CURRENT USER ERROR:",
            repr(e)
        )

        return None


# ============================================================
# GET USER
# ============================================================

def get_user(
    user_id
):
    """
    Get the currently authenticated user if their
    Supabase ID matches the supplied ID.
    """

    try:

        user = get_current_user()

        if not user:

            return None

        if str(
            user["id"]
        ) != str(user_id):

            return None

        return (
            user["id"],
            user["full_name"],
            user["email"]
        )

    except Exception:

        return None


# ============================================================
# LOGOUT
# ============================================================

def logout_user():
    """
    Sign out the current Supabase user.
    """

    try:

        supabase = get_supabase()

        supabase.auth.sign_out()

        return True

    except Exception as e:

        print(
            "LOGOUT ERROR:",
            repr(e)
        )

        return False