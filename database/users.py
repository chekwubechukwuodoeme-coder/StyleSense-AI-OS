import streamlit as st

from supabase import create_client
from supabase.client import ClientOptions


# ============================================================
# SUPABASE CONFIGURATION
# ============================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

AVATAR_BUCKET = "avatars"


# ============================================================
# STREAMLIT STORAGE
# ============================================================

class StreamlitStorage:
    """
    Storage adapter used by Supabase Auth.
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
                        "full_name": full_name,
                        "profession": "Fashion Designer",
                        "avatar_url": "",
                    }
                }
            }
        )

        if not response.user:
            return False, "Unable to create account."

        if response.session is None:

            return (
                True,
                "Account created successfully. "
                "Please check your email and verify your account "
                "before logging in."
            )

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
        return None, "Please enter your email and password."

    try:

        supabase = get_supabase()

        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        if not response.user:

            return None, "Unable to authenticate this account."

        user = response.user

        user_email = user.email

        metadata = user.user_metadata or {}

        full_name = (
            metadata.get("full_name")
            or metadata.get("name")
        )

        profession = (
            metadata.get("profession")
            or "Fashion Designer"
        )

        avatar_url = (
            metadata.get("avatar_url")
            or ""
        )

        if not full_name:

            full_name = (
                user_email.split("@")[0]
                if user_email
                else "User"
            )

        return (
            {
                "id": user.id,
                "full_name": full_name,
                "email": user_email,
                "profession": profession,
                "avatar_url": avatar_url,
            },
            None
        )

    except Exception as e:

        error = str(e)
        lower = error.lower()

        print(
            "EMAIL LOGIN ERROR:",
            repr(e)
        )

        if (
            "email_not_confirmed" in lower
            or "email not confirmed" in lower
        ):

            return (
                None,
                "Your email has not been verified yet. "
                "Please check your inbox and click the "
                "Supabase confirmation link."
            )

        if (
            "invalid login credentials" in lower
            or "invalid credentials" in lower
        ):

            return (
                None,
                "Incorrect email or password."
            )

        if (
            "rate limit" in lower
            or "too many requests" in lower
        ):

            return (
                None,
                "Too many login attempts. "
                "Please wait a moment and try again."
            )

        return (
            None,
            f"Login error: {error}"
        )


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

        metadata = getattr(
            user,
            "user_metadata",
            None
        ) or {}

        full_name = (
            metadata.get("full_name")
            or metadata.get("name")
        )

        profession = (
            metadata.get("profession")
            or "Fashion Designer"
        )

        avatar_url = (
            metadata.get("avatar_url")
            or ""
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
            "profession": profession,
            "avatar_url": avatar_url,
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

        return user

    except Exception as e:

        print(
            "GET USER ERROR:",
            repr(e)
        )

        return None


# ============================================================
# UPLOAD PROFILE PICTURE
# ============================================================

def upload_profile_avatar(uploaded_file):

    if uploaded_file is None:
        return None, "No image selected."

    try:

        supabase = get_supabase()

        user = get_current_user()

        if not user:
            return None, "Unable to identify the current user."

        user_id = str(user["id"])

        # ----------------------------------------------------
        # GET FILE INFORMATION
        # ----------------------------------------------------

        file_bytes = uploaded_file.getvalue()

        content_type = (
            uploaded_file.type
            or "image/jpeg"
        )

        original_name = (
            uploaded_file.name
            or "profile.jpg"
        )

        extension = original_name.rsplit(
            ".",
            1
        )[-1].lower()

        allowed_extensions = {
            "jpg",
            "jpeg",
            "png",
            "webp",
        }

        if extension not in allowed_extensions:

            return (
                None,
                "Please upload a JPG, JPEG, PNG or WEBP image."
            )

        # ----------------------------------------------------
        # CREATE UNIQUE FILE PATH
        # ----------------------------------------------------

        file_path = (
            f"{user_id}/profile.{extension}"
        )

        # ----------------------------------------------------
        # UPLOAD TO SUPABASE STORAGE
        # ----------------------------------------------------

        supabase.storage \
            .from_(AVATAR_BUCKET) \
            .upload(
                file_path,
                file_bytes,
                {
                    "content-type": content_type,
                    "upsert": "true",
                }
            )

        # ----------------------------------------------------
        # GET PUBLIC URL
        # ----------------------------------------------------

        public_url = (
            supabase.storage
            .from_(AVATAR_BUCKET)
            .get_public_url(file_path)
        )

        # Some versions return a string while others may
        # return an object/dictionary.

        if isinstance(public_url, str):

            avatar_url = public_url

        elif isinstance(public_url, dict):

            avatar_url = (
                public_url.get("publicUrl")
                or public_url.get("public_url")
            )

        else:

            avatar_url = getattr(
                public_url,
                "public_url",
                None
            )

        if not avatar_url:

            return (
                None,
                "Image uploaded, but the public URL could not be created."
            )

        return avatar_url, None

    except Exception as e:

        print(
            "UPLOAD PROFILE AVATAR ERROR:",
            repr(e)
        )

        return (
            None,
            f"Profile image upload failed: {e}"
        )


# ============================================================
# UPLOAD PROFILE IMAGE
# ============================================================

def upload_profile_image(uploaded_file):

    if uploaded_file is None:

        return (
            False,
            "",
            "No image selected."
        )

    try:

        supabase = get_supabase()

        user = get_current_user()

        if not user:

            return (
                False,
                "",
                "You must be logged in."
            )

        user_id = str(user["id"])

        file_extension = (
            uploaded_file.name
            .split(".")[-1]
            .lower()
        )

        # ----------------------------------------------------
        # CREATE FILE PATH
        # ----------------------------------------------------

        file_path = (
            f"{user_id}/profile.{file_extension}"
        )

        file_bytes = uploaded_file.getvalue()

        # ----------------------------------------------------
        # DELETE OLD PROFILE IMAGE(S)
        # ----------------------------------------------------

        old_files = (
            supabase.storage
            .from_("profile-images")
            .list(user_id)
        )

        if old_files:

            files_to_remove = []

            for file in old_files:

                file_name = file.get(
                    "name"
                )

                if file_name:

                    files_to_remove.append(
                        f"{user_id}/{file_name}"
                    )

            if files_to_remove:

                supabase.storage \
                    .from_("profile-images") \
                    .remove(
                        files_to_remove
                    )

        # ----------------------------------------------------
        # UPLOAD NEW PROFILE IMAGE
        # ----------------------------------------------------

        supabase.storage \
            .from_("profile-images") \
            .upload(
                file_path,
                file_bytes,
                {
                    "content-type": uploaded_file.type
                }
            )

        # ----------------------------------------------------
        # GET PUBLIC URL
        # ----------------------------------------------------

        public_url = (
            supabase.storage
            .from_("profile-images")
            .get_public_url(
                file_path
            )
        )

        # ----------------------------------------------------
        # SAVE AVATAR URL TO SUPABASE AUTH
        # ----------------------------------------------------

        response = supabase.auth.update_user(
            {
                "data": {
                    "avatar_url": public_url
                }
            }
        )

        if not response.user:

            return (
                False,
                "",
                "Profile image could not be saved."
            )

        # ----------------------------------------------------
        # UPDATE STREAMLIT SESSION
        # ----------------------------------------------------

        st.session_state.user_avatar_url = (
            public_url
        )

        return (
            True,
            public_url,
            "Profile picture updated successfully."
        )

    except Exception as e:

        print(
            "UPLOAD PROFILE IMAGE ERROR:",
            repr(e)
        )

        return (
            False,
            "",
            str(e)
        )


# ============================================================
# UPDATE PROFILE
# ============================================================

def update_user_profile(
    full_name,
    profession,
    avatar_url=""
):

    full_name = (full_name or "").strip()
    profession = (profession or "").strip()
    avatar_url = (avatar_url or "").strip()

    if not full_name:

        return False, "Please enter your full name."

    if not profession:

        return False, "Please enter your profession."

    try:

        supabase = get_supabase()

        response = supabase.auth.update_user(
            {
                "data": {
                    "full_name": full_name,
                    "profession": profession,
                    "avatar_url": avatar_url,
                }
            }
        )

        if not response.user:

            return (
                False,
                "Unable to update your profile."
            )

        # ----------------------------------------------------
        # UPDATE STREAMLIT SESSION
        # ----------------------------------------------------

        st.session_state.user_name = full_name

        st.session_state.user_profession = profession

        st.session_state.user_avatar_url = avatar_url

        return True, "Profile updated successfully."

    except Exception as e:

        print(
            "UPDATE PROFILE ERROR:",
            repr(e)
        )

        return False, str(e)


# ============================================================
# LOGOUT
# ============================================================

def logout_user():

    try:

        supabase = get_supabase()

        supabase.auth.sign_out()

        st.session_state.pop(
            "supabase_client",
            None
        )

        for key in list(
            st.session_state.keys()
        ):

            if key.startswith(
                "_supabase_"
            ):

                del st.session_state[key]

        st.session_state.logged_in = False

        st.session_state.user_id = None

        st.session_state.user_name = None

        st.session_state.user_email = None

        st.session_state.user_profession = None

        st.session_state.user_avatar_url = None

        st.session_state.auth_page = "login"

        return True

    except Exception as e:

        print(
            "LOGOUT ERROR:",
            repr(e)
        )

        return False