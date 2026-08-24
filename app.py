import streamlit as st
from pathlib import Path

from database.database import init_database
from background_tasks import get_job_status

from database.users import (
    get_current_user,
    logout_user,
)

from views.auth import render_auth
from views.inventory import render_inventory
from views.production_manager import render_production_manager
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
# STYLESENSE GLOBAL APP + SIDEBAR COLORS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL STYLESENSE BACKGROUND
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 8% 8%,
                rgba(245, 166, 35, 0.32),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 12%,
                rgba(57, 255, 20, 0.18),
                transparent 25%
            ),
            radial-gradient(
                circle at 15% 85%,
                rgba(0, 107, 69, 0.30),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 85%,
                rgba(57, 255, 20, 0.12),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #263238 0%,
                #263238 30%,
                #006B45 55%,
                #263238 75%,
                #F5A623 100%
            ) !important;

        background-attachment: fixed !important;
        min-height: 100vh !important;
    }


    /* ========================================================
       MAIN CONTENT
       ======================================================== */

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background: transparent !important;
    }


    /* ========================================================
       SIDEBAR
       DEEP SLATE CHARCOAL + ELECTRIC LIME GREEN
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #263238 0%,
                #263238 70%,
                #1F292D 100%
            ) !important;

        border-right: 2px solid #39FF14 !important;
    }


    /* Sidebar inner area */

    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }


    /* ========================================================
       SIDEBAR TEXT
       ======================================================== */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }


    /* ========================================================
       SIDEBAR BUTTONS
       ======================================================== */

    section[data-testid="stSidebar"]
    div[data-testid="stButton"] button {
        background: rgba(57, 255, 20, 0.06) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(57, 255, 20, 0.15) !important;
        border-radius: 12px !important;
    }


    /* ========================================================
       SIDEBAR BUTTON HOVER
       ======================================================== */

    section[data-testid="stSidebar"]
    div[data-testid="stButton"] button:hover {
        background: #39FF14 !important;
        color: #263238 !important;
        border-color: #39FF14 !important;
        box-shadow:
            0 0 15px rgba(57, 255, 20, 0.30) !important;
    }


    /* ========================================================
       SIDEBAR DIVIDERS
       ======================================================== */

    section[data-testid="stSidebar"] hr {
        border-color: rgba(57, 255, 20, 0.20) !important;
    }


    /* ========================================================
       SIDEBAR LINKS
       ======================================================== */

    section[data-testid="stSidebar"] a {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] a:hover {
        color: #39FF14 !important;
    }


    </style>
    """,
    unsafe_allow_html=True,
)

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
# LOAD CSS
# ============================================================

def load_css():

    if not CSS_PATH.exists():
        print(f"CSS file not found: {CSS_PATH}")
        return

    try:

        with open(
            CSS_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            css = f.read()

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
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

    "user_profession": "None",

    "user_avatar_url": "None",

    "auth_page": "login",
    
    "main_navigation": "Dashboard",

    "open_profile_settings": False,

    "saved_designs": [],

    "saved_inspirations": [],

    "collections": [],

    "messages": [],

    "current_design": "",

    "current_image": None,

    "design_generation_job_id": None,

    "design_generation_status": None,

    "design_generation_result": None,

    "design_generation_error": None,

    "current_project": None,

    "open_workspace": False,

    "dashboard_ai_prompt": "",

    "fashion_news_articles": [],

    "fashion_news_generated": False,

    # Fashion Inspiration → Design Studio

    "open_design_studio": False,

    "studio_reference_image_url": None,

    "studio_reference_title": "",

    "studio_reference_photographer": "",
}


for key, value in DEFAULT_SESSION_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# CHECK EXISTING USER SESSION
# ============================================================

if not st.session_state.logged_in:

    current_user = get_current_user()

    if current_user:

        st.session_state.logged_in = True

        st.session_state.user_id = current_user["id"]

        st.session_state.user_name = current_user["full_name"]

        st.session_state.user_email = current_user["email"]

        st.session_state.user_profession = (
            current_user.get(
                "profession",
                "Fashion Designer"
            )
            or "Fashion Designer"
        )

        st.session_state.user_avatar_url = (
            current_user.get(
                "avatar_url",
                ""
            )
            or ""
        )

        st.rerun()

    else:

        render_auth()

        st.stop()


# ============================================================
# BACKGROUND DESIGN GENERATION
# ============================================================

design_job_id = st.session_state.get(
    "design_generation_job_id"
)


if design_job_id:

    job_status = get_job_status(
        design_job_id
    )

    status = job_status.get(
        "status"
    )

    # --------------------------------------------------------
    # GENERATING
    # --------------------------------------------------------

    if status == "generating":

        st.info(
            "🎨 Your AI fashion design is being generated..."
        )

    # --------------------------------------------------------
    # COMPLETED
    # --------------------------------------------------------

    elif status == "completed":

        result = job_status.get(
            "result"
        )

        if result:

            st.session_state.design_generation_result = (
                result
            )

            st.session_state.current_image = (
                result
            )

            st.session_state.design_generation_status = (
                "completed"
            )

            st.success(
                "✨ Your AI design is ready!"
            )

            st.subheader(
                "🎨 Your AI Fashion Design"
            )

            st.image(
                result,
                use_container_width=True
            )

        else:

            st.warning(
                "The design finished generating, "
                "but no image was returned."
            )

        st.session_state.design_generation_job_id = None

    # --------------------------------------------------------
    # FAILED
    # --------------------------------------------------------

    elif status == "failed":

        error = job_status.get(
            "error"
        )

        st.session_state.design_generation_status = (
            "failed"
        )

        st.session_state.design_generation_error = (
            error
        )

        st.error(
            "❌ AI design generation failed."
        )

        if error:

            st.caption(
                str(error)
            )

        st.session_state.design_generation_job_id = None


# ============================================================
# PAGE DEFINITIONS
# ============================================================

PAGES = {

    "Dashboard":
        render_dashboard,

    "Projects":
        render_projects,

    "AI Team":
        render_ai_team,

    "Design Studio":
        render_design_studio,

    "Fashion Inspiration":
        render_fashion_inspiration,

    "AI Design Editor":
        render_design_editor,

    "AI Co-Founder":
        render_fashion_cofounder,

    "Logo Generator":
        render_logo_generator,

    "Outfit Analyzer":
        render_outfit_analyzer,

    "Ask StyleSense":
        render_fashion_assistant,

    "Fabric Advisor":
        render_fabric_advisor,

    "Design Library":
        render_design_library,

    "Color Matcher":
        render_color_matcher,

    "Fashion News":
        render_fashion_news,

    "Fashion Magazine":
        render_fashion_magazine,

    "AI Fashion Trends":
        render_fashion_trends,

    "Production Manager":
        render_production_manager,

    "Marketplace":
        render_marketplace,

    "Fashion Professionals":
        render_profiles,

    "AI Virtual Stylist":
        render_virtual_stylist,

    "Settings":
        render_settings,
}


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    # ========================================================
    # BRAND
    # ========================================================

    st.title("✦ StyleSense")

    st.caption(
        "AI Fashion Operating System"
    )

    # ========================================================
    # USER PROFILE
    # ========================================================

    user_name = (
        st.session_state.get(
            "user_name"
        )
        or "StyleSense User"
    )

    user_profession = (
        st.session_state.get(
            "user_profession"
        )
        or "Fashion Designer"
    )

    avatar_url = (
        st.session_state.get(
            "user_avatar_url"
        )
        or ""
    )

    first_letter = (
        str(user_name)[0].upper()
        if user_name
        else "U"
    )

    # --------------------------------------------------------
    # PROFILE CONTAINER
    # --------------------------------------------------------

    profile_col1, profile_col2 = st.columns(
        [1, 2.5],
        vertical_alignment="center"
    )

    # --------------------------------------------------------
    # PROFILE IMAGE
    # --------------------------------------------------------

    with profile_col1:

        if avatar_url:

            st.image(
                avatar_url,
                width=58
            )

        else:

            st.markdown(
                f"""
                <div style="
                    width:58px;
                    height:58px;
                    border-radius:50%;
                    background:linear-gradient(
                        135deg,
                        #7c3aed,
                        #ec4899
                    );
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                    font-size:24px;
                    font-weight:700;
                ">
                    {first_letter}
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # NAME + PROFESSION
    # --------------------------------------------------------

    with profile_col2:

        st.markdown(
            f"**{user_name}**"
        )

        st.caption(
            user_profession
        )

    # --------------------------------------------------------
    # EDIT PROFILE
    # --------------------------------------------------------

    if st.button(
        "Edit Profile →",
        key="sidebar_edit_profile",
        use_container_width=True,
    ):

        st.session_state.main_navigation = "Settings"

        st.session_state.open_profile_settings = True

        st.rerun()

    # ========================================================
    # MAIN NAVIGATION
    # ========================================================

    st.caption("WORKSPACE")

    main_navigation = [

        ("🏠", "Dashboard"),

        ("🤖", "AI Team"),

        ("✨", "Design Studio"),

        ("📚", "Design Library"),

        ("📸", "Outfit Analyzer"),

        ("🧵", "Fabric Advisor"),

        ("🎨", "Color Matcher"),

        ("💡", "Fashion Inspiration"),

        ("📈", "AI Fashion Trends"),

        ("📰", "Fashion News"),

        ("📰", "Fashion Magazine"),

        ("👔", "Fashion Professionals"),

        ("🛍️", "Marketplace"),
    ]

    current_page = st.session_state.get(
        "main_navigation",
        "Dashboard"
    )

    for icon, label in main_navigation:

        is_active = (
            current_page == label
        )

        if is_active:

            button_text = (
                f"● {icon} {label}"
            )

        else:

            button_text = (
                f"{icon} {label}"
            )

        if st.button(
            button_text,
            key=f"main_nav_{label}",
            use_container_width=True,
        ):

            st.session_state.main_navigation = (
                label
            )

            st.rerun()

    # ========================================================
    # AI SHORTCUT
    # ========================================================

    st.divider()

    st.caption(
        "AI SHORTCUT"
    )

    # --------------------------------------------------------
    # ASK STYLESENSE
    # --------------------------------------------------------

    if st.button(
        "✦ Ask StyleSense",
        key="shortcut_ask_stylesense",
        use_container_width=True,
    ):

        st.session_state.main_navigation = (
            "Ask StyleSense"
        )

        st.rerun()

    # --------------------------------------------------------
    # AI CO-FOUNDER
    # --------------------------------------------------------

    if st.button(
        "🚀 AI Co-Founder",
        key="shortcut_ai_cofounder",
        use_container_width=True,
    ):

        st.session_state.main_navigation = (
            "AI Co-Founder"
        )

        st.rerun()

    # --------------------------------------------------------
    # MY TASKS
    # --------------------------------------------------------

    if st.button(
        "✓ My Tasks",
        key="shortcut_my_tasks",
        use_container_width=True,
    ):

        st.session_state.main_navigation = (
            "My Tasks"
        )

        st.rerun()

    # --------------------------------------------------------
    # NOTIFICATIONS
    # --------------------------------------------------------

    if st.button(
        "🔔 Notifications",
        key="shortcut_notifications",
        use_container_width=True,
    ):

        st.session_state.main_navigation = (
            "Notifications"
        )

        st.rerun()

    # ========================================================
    # SETTINGS
    # ========================================================

    st.divider()

    st.caption(
        "SETTINGS"
    )

    # --------------------------------------------------------
    # SETTINGS
    # --------------------------------------------------------

    if st.button(
        "⚙ Settings",
        key="sidebar_settings",
        use_container_width=True,
    ):

        st.session_state.main_navigation = (
            "Settings"
        )

        st.rerun()

    # --------------------------------------------------------
    # HELP & SUPPORT
    # --------------------------------------------------------

    if st.button(
        "❓ Help & Support",
        key="sidebar_help_support",
        use_container_width=True,
    ):

        st.session_state.main_navigation = (
            "Help & Support"
        )

        st.rerun()

    # --------------------------------------------------------
    # LOGOUT
    # --------------------------------------------------------

    if st.button(
        "↪ Logout",
        key="sidebar_logout",
        use_container_width=True,
    ):

        st.session_state.logged_in = False

        st.session_state.user_id = None

        st.session_state.user_name = None

        st.session_state.user_email = None

        st.rerun()

    # ========================================================
    # UPGRADE TO PRO
    # ========================================================

    st.divider()

    st.info(
        "✨ UPGRADE TO PRO\n\n"
        "Unlock advanced AI tools, "
        "more generations and "
        "professional fashion workflows."
    )

    if st.button(
        "Upgrade to Pro →",
        key="upgrade_to_pro",
        use_container_width=True,
        type="primary",
    ):

        st.session_state.main_navigation = (
            "Settings"
        )

        st.rerun()


# ============================================================
# PAGE ROUTING
# ============================================================

current_page = st.session_state.get(
    "main_navigation",
    "Dashboard"
)


# ============================================================
# SPECIAL PAGES
# ============================================================

if current_page == "My Tasks":

    st.title("✓ My Tasks")

    st.caption(
        "Your fashion workflow and AI tasks."
    )

    st.info(
        "Task management is coming next."
    )


elif current_page == "Notifications":

    st.title("🔔 Notifications")

    st.caption(
        "Stay updated with your StyleSense workspace."
    )

    st.info(
        "Notifications will appear here."
    )


elif current_page == "Help & Support":

    st.title("❓ Help & Support")

    st.caption(
        "Get help using StyleSense AI OS."
    )

    st.info(
        "Help and support tools will be added here."
    )


# ============================================================
# WORKSPACE
# ============================================================

elif current_page == "Workspace":

    if (
        st.session_state.get(
            "current_project"
        ) is None
    ):

        st.warning(
            "Open a project first."
        )

        st.info(
            "Go to Projects and click "
            "Open Project."
        )

    else:

        render_workspace()


# ============================================================
# PRODUCTION SECTION
# ============================================================

st.divider()

st.caption("🏭 PRODUCTION")

if st.button(
    "🏭 Production Manager",
    key="nav_production_manager",
    use_container_width=True,
):

    st.session_state.main_navigation = (
        "Production Manager"
    )

    st.rerun()

# ============================================================
# NORMAL PAGE ROUTING
# ============================================================

else:

    selected_page = PAGES.get(
        current_page
    )

    if selected_page is not None:

        selected_page()

    else:

        st.error(
            f"Page not found: {current_page}"
        )