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
    Create a Supabase client.
    """

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )


# ============================================================
# CREATE USER / REGISTER
# ============================================================

def create_user(
    full_name,
    email,
    password
):

    full_name = full_name.strip()
    email = email.strip().lower()

    # --------------------------------------------------------
    # Validation
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

        response = supabase.auth.sign_up({
            "email": email,
            "password": password,

            "options": {
                "data": {
                    "full_name": full_name
                }
            }
        })

        # ----------------------------------------------------
        # Check user
        # ----------------------------------------------------

        if response.user is None:

            return False, "Unable to create account."

        return True, response.user

    except Exception as e:

        error_message = str(e)

        # ----------------------------------------------------
        # Existing account
        # ----------------------------------------------------

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

        return False, error_message


# ============================================================
# LOGIN
# ============================================================

def authenticate_user(
    email,
    password
):

    email = email.strip().lower()

    if not email or not password:

        return None

    try:

        supabase = get_supabase()

        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        # ----------------------------------------------------
        # Make sure authentication succeeded
        # ----------------------------------------------------

        if not response.user:

            return None

        user = response.user

        # ----------------------------------------------------
        # Supabase user ID
        # ----------------------------------------------------

        user_id = user.id

        # ----------------------------------------------------
        # Email
        # ----------------------------------------------------

        user_email = user.email

        # ----------------------------------------------------
        # Full name
        # ----------------------------------------------------

        full_name = None

        if user.user_metadata:

            full_name = user.user_metadata.get(
                "full_name"
            )

        # ----------------------------------------------------
        # Fallback name
        # ----------------------------------------------------

        if not full_name:

            full_name = user_email.split("@")[0]

        # ----------------------------------------------------
        # Return exactly what views/auth.py expects
        # ----------------------------------------------------

        return (
            user_id,
            full_name,
            user_email
        )

    except Exception:

        return None


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user():

    try:

        supabase = get_supabase()

        response = supabase.auth.get_user()

        if not response:

            return None

        if not response.user:

            return None

        user = response.user

        full_name = None

        if user.user_metadata:

            full_name = user.user_metadata.get(
                "full_name"
            )

        if not full_name:

            full_name = user.email.split("@")[0]

        return {
            "id": user.id,
            "full_name": full_name,
            "email": user.email
        }

    except Exception:

        return None


# ============================================================
# GET USER BY ID
# ============================================================

def get_user(user_id):

    """
    Returns the currently authenticated user if the
    Supabase ID matches.
    """

    try:

        user = get_current_user()

        if not user:

            return None

        if str(user["id"]) != str(user_id):

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

    try:

        supabase = get_supabase()

        supabase.auth.sign_out()

        return True

    except Exception:

        return False