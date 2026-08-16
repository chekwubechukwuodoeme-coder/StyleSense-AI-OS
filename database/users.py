import streamlit as st

from supabase import create_client
from supabase.client import ClientOptions


# ============================================================
# SUPABASE CONFIGURATION
# ============================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


# ============================================================
# STREAMLIT STORAGE
# ============================================================

class StreamlitStorage:
    """
    Storage adapter used by Supabase Auth.

    Supabase uses this storage to keep:
        - authentication session
        - refresh token
        - other temporary auth state

    Streamlit session_state is scoped to the current browser
    session, which prevents different users from sharing auth
    state.
    """

    def get_item(self, key):
        return st.session_state.get(
            f"_supabase_{key}"
        )

    def set_item(self, key, value):
        st.session_state[
            f"_supabase_{key}"
        ] = value

    def remove_item(self, key):
        st.session_state.pop(
            f"_supabase_{key}",
            None
        )


# ============================================================
# SUPABASE CLIENT
# ============================================================

def get_supabase():
    """
    Return the Supabase client for the current Streamlit
    browser session.

    Authentication state is stored per Streamlit session.
    """

    if "supabase_client" not in st.session_state:

        storage = StreamlitStorage()

        options = ClientOptions(
            flow_type="pkce",
            storage=storage,
            auto_refresh_token=True,
            persist_session=True,
        )

        st.session_state.supabase_client = create_client(
            SUPABASE_URL,
            SUPABASE_KEY,
            options=options,
        )

    return st.session_state.supabase_client


# ============================================================
# REGISTER
# ============================================================

def create_user(full_name, email, password):

    full_name = (full_name or "").strip()
    email = (email or "").strip().lower()
    password = password or ""

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
        # EMAIL CONFIRMATION REQUIRED
        # ----------------------------------------------------

        if response.session is None:

            return (
                True,
                "Account created successfully. "
                "Please check your email and verify your account "
                "before logging in."
            )

        # ----------------------------------------------------
        # SESSION CREATED IMMEDIATELY
        # ----------------------------------------------------

        return True, response.user

    except Exception as e:

        error = str(e)
        lower = error.lower()

        if (
            "already registered" in lower
            or "user already registered" in lower
            or "already exists" in lower
        ):

            return (
                False,
                "An account with this email already exists."
            )

        print(
            "CREATE USER ERROR:",
            repr(e)
        )

        return False, error


# ============================================================
# EMAIL LOGIN
# ============================================================

def authenticate_user(email, password):

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
            user.id,
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
# CURRENT USER
# ============================================================

def get_current_user():

    try:

        supabase = get_supabase()

        response = supabase.auth.get_user()

        if not response:
            return None

        user = getattr(
            response,
            "user",
            None
        )

        if not user:
            return None

        user_email = getattr(
            user,
            "email",
            None
        )

        user_metadata = getattr(
            user,
            "user_metadata",
            None
        )

        full_name = None

        if user_metadata:

            full_name = (
                user_metadata.get("full_name")
                or user_metadata.get("name")
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
            "email": user_email,
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

    try:

        supabase = get_supabase()

        supabase.auth.sign_out()

        # ----------------------------------------------------
        # CLEAR SUPABASE CLIENT
        # ----------------------------------------------------

        st.session_state.pop(
            "supabase_client",
            None
        )

        # ----------------------------------------------------
        # CLEAR SUPABASE STORAGE
        # ----------------------------------------------------

        for key in list(
            st.session_state.keys()
        ):

            if key.startswith(
                "_supabase_"
            ):

                del st.session_state[key]

        # ----------------------------------------------------
        # CLEAR APPLICATION AUTH STATE
        # ----------------------------------------------------

        st.session_state.logged_in = False

        st.session_state.user_id = None

        st.session_state.user_name = None

        st.session_state.user_email = None

        st.session_state.auth_page = "login"

        return True

    except Exception as e:

        print(
            "LOGOUT ERROR:",
            repr(e)
        )

        return False