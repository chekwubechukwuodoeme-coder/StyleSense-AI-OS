import os

from dotenv import load_dotenv
from supabase import create_client


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing from .env")


# ============================================================
# SUPABASE CLIENT
# ============================================================

def get_supabase():
    """
    Create a fresh Supabase client for each authentication
    operation.

    This is safer for Streamlit because different users should
    not share the same authentication session.
    """

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )


# ============================================================
# CREATE USER
# ============================================================

def create_user(
    full_name,
    email,
    password
):

    full_name = full_name.strip()
    email = email.strip().lower()

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

        if response.user is None:
            return False, "Unable to create account."

        return True, response.user

    except Exception as e:

        error_message = str(e)

        if "already registered" in error_message.lower():
            return False, "An account with this email already exists."

        return False, error_message


# ============================================================
# AUTHENTICATE USER
# ============================================================

def authenticate_user(
    email,
    password
):

    email = email.strip().lower()

    try:

        supabase = get_supabase()

        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not response.user:
            return None

        user = response.user

        user_id = user.id

        user_email = user.email

        full_name = (
            user.user_metadata.get("full_name")
            if user.user_metadata
            else None
        )

        if not full_name:
            full_name = user_email.split("@")[0]

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

def get_user(user_id):

    try:

        supabase = get_supabase()

        response = supabase.auth.get_user()

        if response and response.user:

            user = response.user

            if user.id != user_id:
                return None

            full_name = (
                user.user_metadata.get("full_name")
                if user.user_metadata
                else None
            )

            return (
                user.id,
                full_name,
                user.email
            )

        return None

    except Exception:

        return None