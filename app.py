import streamlit as st
from pathlib import Path

from database.database import init_database

from database.users import (
    get_current_user,
)

from views.auth import render_auth

from views.profiles import render_profiles
from views.fashion_cofounder import render_fashion_cofounder
from views.dashboard import render_dashboard
from views.marketplace import render_marketplace
from views.design_library import render_design_library
from views.settings import render_settings
from views.fashion_trends import render_fashion_trends
from views.fashion_magazine import render_fashion_magazine
from views.fashion_news import render_fashion_news
from views.virtual_stylist import render_virtual_stylist
from views.color_matcher import render_color_matcher
from views.fabric_advisor import render_fabric_advisor
from views.logo_generator import render_logo_generator
from views.fashion_inspiration import render_fashion_inspiration
from views.outfit_analyzer import render_outfit_analyzer
from views.design_editor import render_design_editor
from views.fashion_assistant import render_fashion_assistant
from views.design_studio import render_design_studio
from views.ai_team import render_ai_team
from views.workspace import render_workspace
from views.projects import render_projects


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="StyleSense AI OS",
    page_icon="👗",
    layout="wide",
)


# ============================================================
# DATABASE
# ============================================================

init_database()


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CSS_PATH = (
    BASE_DIR
    / "assets"
    / "css"
    / "style.css"
)


# ============================================================
# CSS
# ============================================================

def load_css():

    if not CSS_PATH.exists():

        print(
            f"CSS file not found: {CSS_PATH}"
        )

        return

    try:

        with open(
            CSS_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )

    except Exception as e:

        print(
            "CSS LOAD ERROR:",
            repr(e)
        )


load_css()


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_SESSION_STATE = {

    "logged_in": False,

    "user_id": None,

    "user_name": None,

    "user_email": None,

    "auth_page": "login",

    "saved_designs": [],

    "saved_inspirations": [],

    "collections": [],

    "messages": [],

    "current_design": "",

    "current_image": None,

    "current_project": None,

    "open_workspace": False,
}


for key, value in DEFAULT_SESSION_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# CHECK EXISTING SUPABASE SESSION
# ============================================================

if not st.session_state.logged_in:

    current_user = get_current_user()

    if current_user:

        st.session_state.logged_in = True

        st.session_state.user_id = (
            current_user["id"]
        )

        st.session_state.user_name = (
            current_user["full_name"]
        )

        st.session_state.user_email = (
            current_user["email"]
        )

        st.rerun()

    else:

        render_auth()

        st.stop()


# ============================================================
# PAGES
# ============================================================

PAGES = {

    "🏠 Dashboard": render_dashboard,

    "📂 Projects": render_projects,

    "🤖 AI Team": render_ai_team,

    "✨ AI Design Studio": render_design_studio,

    "💡 Fashion Inspiration": render_fashion_inspiration,

    "✏ AI Design Editor": render_design_editor,

    "🚀 AI Fashion Co-Founder":
        render_fashion_cofounder,

    "🎨 Logo Generator":
        render_logo_generator,

    "📸 Outfit Analyzer":
        render_outfit_analyzer,

    "🤖 Fashion Assistant":
        render_fashion_assistant,

    "🧵 Fabric Advisor":
        render_fabric_advisor,

    "📚 Design Library":
        render_design_library,

    "🎨 Color Matcher":
        render_color_matcher,

    "📰 Fashion News":
        render_fashion_news,

    "📰 Fashion Magazine":
        render_fashion_magazine,

    "🔥 AI Fashion Trends":
        render_fashion_trends,

    "🛍️ Fashion Marketplace":
        render_marketplace,

    "👗 Fashion Professionals":
        render_profiles,

    "👔 AI Virtual Stylist":
        render_virtual_stylist,

    "⚙ Settings":
        render_settings,
}


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    logo_path = (
        BASE_DIR
        / "assets"
        / "logo.png"
    )

    if logo_path.exists():

        st.image(
            str(logo_path),
            width=80
        )

    st.title(
        "👗 StyleSense AI OS"
    )

    st.caption(
        "Powered by Chekwube Empire"
    )

    st.success(
        "🟢 OpenAI Connected"
    )

    navigation = (
        ["🖥 Workspace"]
        + list(PAGES.keys())
    )

    # --------------------------------------------------------
    # WORKSPACE
    # --------------------------------------------------------

    if st.session_state.get(
        "open_workspace",
        False
    ):

        page = "🖥 Workspace"

        st.session_state.open_workspace = False

    else:

        page = st.radio(
            "Navigation",
            navigation,
            index=1,
            key="main_navigation"
        )


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "🖥 Workspace":

    if st.session_state.get(
        "current_project"
    ) is None:

        st.warning(
            "Open a project first."
        )

        st.info(
            "Go to 📂 Projects and click "
            "🚀 Open Project."
        )

    else:

        render_workspace()

else:

    selected_page = PAGES.get(
        page
    )

    if selected_page:

        selected_page()