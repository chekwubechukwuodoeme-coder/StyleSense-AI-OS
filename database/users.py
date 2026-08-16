import streamlit as st
from supabase import create_client


# ============================================================
# SUPABASE CONFIG
# ============================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


# ============================================================
# SUPABASE CLIENT
# ============================================================

@st.cache_resource
def get_supabase():

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )


# ============================================================
# REGISTER
# ============================================================

def create_user(full_name, email, password):

    full_name = full_name.strip()
    email = email.strip().lower()
    password = password.strip()

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

        if response.session is None:

            return (
                True,
                "Account created! Please check your email and "
                "confirm your account before logging in."
            )

        return True, response.user

    except Exception as e:

        error = str(e).lower()

        if (
            "already registered" in error
            or "user already registered" in error
        ):
            return False, "An account with this email already exists."

        return False, str(e)


# ============================================================
# LOGIN
# ============================================================

def authenticate_user(email, password):

    email = email.strip().lower()

    if not email:
        return False, "Please enter your email."

    if not password:
        return False, "Please enter your password."

    try:

        supabase = get_supabase()

        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not response or not response.user:
            return False, "Login failed. No user was returned."

        user = response.user

        user_email = user.email or email

        full_name = None

        if user.user_metadata:
            full_name = user.user_metadata.get("full_name")

        if not full_name:
            full_name = user_email.split("@")[0]

        return True, {
            "id": user.id,
            "full_name": full_name,
            "email": user_email
        }

    except Exception as e:

        error = str(e)

        print("LOGIN ERROR:", error)

        error_lower = error.lower()

        if "email not confirmed" in error_lower:

            return False, (
                "Your email has not been confirmed. "
                "Please check your email and click the confirmation link."
            )

        if "invalid login credentials" in error_lower:
            return False, "Invalid email or password."

        if "user not found" in error_lower:
            return False, "No account was found with this email."

        return False, f"Login error: {error}"


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user():

    try:

        supabase = get_supabase()

        response = supabase.auth.get_user()

        if not response or not response.user:
            return None

        user = response.user

        user_email = user.email

        full_name = (
            user.user_metadata.get("full_name")
            if user.user_metadata
            else None
        )

        if not full_name:

            full_name = (
                user_email.split("@")[0]
                if user_email
                else "User"
            )

        return {
            "id": user.id,
            "full_name": full_name,
            "email": user_email
        }

    except Exception as e:

        print("GET CURRENT USER ERROR:", e)

        return None


# ============================================================
# GET USER BY ID
# ============================================================

def get_user(user_id):

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

    except Exception as e:

        print("GET USER ERROR:", e)

        return None

# ============================================================
# GOOGLE LOGIN
# ============================================================

def sign_in_with_google():

    try:

        supabase = get_supabase()

        redirect_url = "https://stylesenseai-os.streamlit.app"

        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": redirect_url
            }
        })

        print("GOOGLE OAUTH RESPONSE:", response)

        return response.url

    except Exception as e:

        print("GOOGLE LOGIN ERROR:", repr(e))

        return f"ERROR: {repr(e)}"

# ============================================================
# LOGOUT
# ============================================================

def logout_user():

    try:

        supabase = get_supabase()

        supabase.auth.sign_out()

        return True

    except Exception as e:

        print("LOGOUT ERROR:", e)

        return False