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
        - PKCE code verifier
        - authentication session
        - refresh token

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

    IMPORTANT:
    Do not use st.cache_resource here because authentication
    state must not be shared between different users.
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
# GOOGLE REDIRECT URL
# ============================================================

def get_google_redirect_url():

    redirect_url = st.secrets.get(
        "GOOGLE_REDIRECT_URL"
    )

    if not redirect_url:

        redirect_url = st.secrets.get(
            "APP_URL"
        )

    if not redirect_url:

        raise RuntimeError(
            "GOOGLE_REDIRECT_URL or APP_URL is missing "
            "from Streamlit secrets."
        )

    # Remove trailing slash so the redirect URI is consistent
    return redirect_url.rstrip("/")


# ============================================================
# GOOGLE LOGIN URL
# ============================================================

def get_google_login_url():

    """
    Generate the Google OAuth URL.

    IMPORTANT:
    The URL is generated only once per Streamlit session.

    This prevents a Streamlit rerun from generating a new
    PKCE verifier and invalidating the verifier associated
    with the Google authorization request.
    """

    # --------------------------------------------------------
    # REUSE EXISTING OAUTH URL
    # --------------------------------------------------------

    existing_url = st.session_state.get(
        "google_oauth_url"
    )

    if existing_url:

        return existing_url

    try:

        supabase = get_supabase()

        redirect_url = get_google_redirect_url()

        # ----------------------------------------------------
        # START GOOGLE OAUTH
        # ----------------------------------------------------

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

        google_url = getattr(
            response,
            "url",
            None
        )

        if not google_url:

            raise RuntimeError(
                "Supabase did not return a Google OAuth URL."
            )

        # ----------------------------------------------------
        # SAVE OAUTH URL
        # ----------------------------------------------------

        st.session_state.google_oauth_url = google_url

        return google_url

    except Exception as e:

        print(
            "GOOGLE LOGIN URL ERROR:",
            type(e).__name__,
            repr(e)
        )

        return None


# ============================================================
# CLEAR GOOGLE OAUTH STATE
# ============================================================

def clear_google_oauth_state():

    """
    Remove OAuth-specific temporary state.

    This should be called after the OAuth flow finishes.
    """

    st.session_state.pop(
        "google_oauth_url",
        None
    )

    # Remove the PKCE verifier after the exchange has finished.
    #
    # Supabase normally removes it itself after a successful
    # exchange, but this also cleans it after an unsuccessful
    # attempt.
    st.session_state.pop(
        "_supabase_code-verifier",
        None
    )


# ============================================================
# GOOGLE CALLBACK
# ============================================================

def handle_google_callback(oauth_code):

    if not oauth_code:
        print("GOOGLE CALLBACK ERROR: Missing OAuth code.")
        return None

    try:

        supabase = get_supabase()

        print("=" * 60)
        print("GOOGLE OAUTH CALLBACK")
        print("=" * 60)

        print("Authorization code received:", bool(oauth_code))

        verifier = st.session_state.get(
            "_supabase_code-verifier"
        )

        print(
            "PKCE verifier exists:",
            bool(verifier)
        )

        if verifier:
            print(
                "PKCE verifier length:",
                len(verifier)
            )

        print(
            "Attempting Supabase code exchange..."
        )

        response = supabase.auth.exchange_code_for_session(
            {
                "auth_code": oauth_code
            }
        )

        print(
            "Supabase exchange response:",
            repr(response)
        )

        if not response:
            print(
                "ERROR: Supabase returned no response."
            )
            return None

        user = getattr(
            response,
            "user",
            None
        )

        session = getattr(
            response,
            "session",
            None
        )

        print(
            "User returned:",
            bool(user)
        )

        print(
            "Session returned:",
            bool(session)
        )

        if not user and session:

            user = getattr(
                session,
                "user",
                None
            )

        if not user:

            print(
                "ERROR: No authenticated user returned."
            )

            return None

        user_email = getattr(
            user,
            "email",
            None
        )

        metadata = getattr(
            user,
            "user_metadata",
            None
        )

        full_name = None

        if metadata:

            full_name = (
                metadata.get("full_name")
                or metadata.get("name")
            )

        if not full_name:

            full_name = (
                user_email.split("@")[0]
                if user_email
                else "User"
            )

        print(
            "GOOGLE LOGIN SUCCESS:",
            user_email
        )

        print("=" * 60)

        return {
            "id": user.id,
            "full_name": full_name,
            "email": user_email,
        }

    except Exception as e:

        print("=" * 60)
        print("GOOGLE OAUTH EXCHANGE FAILED")
        print("=" * 60)

        print(
            "ERROR TYPE:",
            type(e).__name__
        )

        print(
            "ERROR:",
            repr(e)
        )

        print(
            "ERROR STRING:",
            str(e)
        )

        print("=" * 60)

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
        # CLEAR GOOGLE OAUTH STATE
        # ----------------------------------------------------

        st.session_state.pop(
            "google_oauth_url",
            None
        )

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