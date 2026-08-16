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
    Create one Supabase client per Streamlit user session.

    The client must NOT be globally cached because it contains
    authentication state and PKCE information.
    """

    if "supabase_client" not in st.session_state:

        st.session_state.supabase_client = create_client(
            SUPABASE_URL,
            SUPABASE_KEY
        )

    return st.session_state.supabase_client


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

    Returns:
        (True, result)
        or
        (False, error_message)
    """

    full_name = (full_name or "").strip()
    email = (email or "").strip().lower()
    password = password or ""

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

        if not response.user:
            return False, "Unable to create account."

        # ----------------------------------------------------
        # EMAIL CONFIRMATION
        # ----------------------------------------------------

        if response.session is None:

            return (
                True,
                "Account created successfully. "
                "Please check your email and verify your account "
                "before logging in."
            )

        # ----------------------------------------------------
        # SESSION CREATED
        # ----------------------------------------------------

        return True, response.user

    except Exception as e:

        error_message = str(e)
        error_lower = error_message.lower()

        if (
            "already registered" in error_lower
            or "user already registered" in error_lower
        ):
            return (
                False,
                "An account with this email already exists."
            )

        return False, error_message


# ============================================================
# EMAIL / PASSWORD LOGIN
# ============================================================

def authenticate_user(
    email,
    password
):
    """
    Authenticate a user using Supabase email/password.

    Returns:
        (
            user_id,
            full_name,
            email
        )

    or None if authentication fails.
    """

    email = (email or "").strip().lower()
    password = password or ""

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

        if not response.user:
            return None

        user = response.user

        user_id = user.id
        user_email = user.email

        full_name = None

        if user.user_metadata:

            full_name = (
                user.user_metadata.get("full_name")
                or user.user_metadata.get("name")
            )

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

    except Exception as e:

        print(
            "EMAIL LOGIN ERROR:",
            repr(e)
        )

        return None


# ============================================================
# GOOGLE REDIRECT URL
# ============================================================

def get_google_redirect_url():
    """
    Get the deployed Streamlit redirect URL
    from Streamlit Cloud secrets.
    """

    redirect_url = st.secrets.get(
        "GOOGLE_REDIRECT_URL"
    )

    if not redirect_url:

        raise RuntimeError(
            "GOOGLE_REDIRECT_URL is missing from "
            "Streamlit secrets."
        )

    return redirect_url.rstrip("/")


# ============================================================
# GOOGLE LOGIN
# ============================================================

def get_google_login_url():
    """
    Generate the Google OAuth login URL.
    """

    try:

        supabase = get_supabase()

        redirect_url = get_google_redirect_url()

        response = supabase.auth.sign_in_with_oauth(
            {
                "provider": "google",
                "options": {
                    "redirect_to": redirect_url
                }
            }
        )

        if not response:

            raise RuntimeError(
                "Supabase did not return an OAuth response."
            )

        if not response.url:

            raise RuntimeError(
                "Supabase did not return a Google OAuth URL."
            )

        return response.url

    except Exception as e:

        print(
            "GOOGLE LOGIN ERROR:",
            repr(e)
        )

        return None


# ============================================================
# GOOGLE CALLBACK
# ============================================================

def handle_google_callback(oauth_code):
    """
    Exchange the Google/Supabase OAuth authorization code
    for a Supabase session and return the authenticated user.

    Returns:
        {
            "id": user_id,
            "full_name": full_name,
            "email": email
        }

        or None if authentication fails.
    """

    if not oauth_code:

        print(
            "GOOGLE CALLBACK ERROR: "
            "Missing OAuth code."
        )

        return None

    try:

        supabase = get_supabase()

        # ----------------------------------------------------
        # EXCHANGE AUTHORIZATION CODE FOR SESSION
        # ----------------------------------------------------

        response = supabase.auth.exchange_code_for_session(
            {
                "auth_code": oauth_code
            }
        )

        if not response:

            print(
                "GOOGLE CALLBACK ERROR: "
                "No response from Supabase."
            )

            return None

        # ----------------------------------------------------
        # GET USER FROM RESPONSE
        # ----------------------------------------------------

        user = None

        if hasattr(response, "user"):

            user = response.user

        # ----------------------------------------------------
        # FALLBACK TO SESSION USER
        # ----------------------------------------------------

        if user is None and hasattr(
            response,
            "session"
        ):

            session = response.session

            if session and hasattr(
                session,
                "user"
            ):

                user = session.user

        # ----------------------------------------------------
        # FALLBACK TO CURRENT USER
        # ----------------------------------------------------

        if user is None:

            current_user = get_current_user()

            if current_user:

                return current_user

            print(
                "GOOGLE CALLBACK ERROR: "
                "Supabase returned no authenticated user."
            )

            return None

        # ----------------------------------------------------
        # GET USER NAME
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # RETURN USER
        # ----------------------------------------------------

        return {
            "id": user.id,
            "full_name": full_name,
            "email": user.email
        }

    except Exception as e:

        print(
            "GOOGLE CALLBACK ERROR TYPE:",
            type(e).__name__
        )

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

    Returns:
        {
            "id": user_id,
            "full_name": full_name,
            "email": email
        }

        or None.
    """

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
            "GET CURRENT USER ERROR:",
            repr(e)
        )

        return None


# ============================================================
# GET USER
# ============================================================

def get_user(user_id):
    """
    Return the currently authenticated user only if
    their Supabase ID matches user_id.
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

    except Exception as e:

        print(
            "GET USER ERROR:",
            repr(e)
        )

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