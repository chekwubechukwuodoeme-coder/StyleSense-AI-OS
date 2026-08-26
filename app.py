import streamlit as st
from pathlib import Path

from database.database import init_database
from background_tasks import get_job_status

from database.users import (
    get_current_user,
    logout_user,
)

from views.auth import render_auth

from views.production_manager import render_production_manager
from views.inventory import render_inventory
from views.measurements import render_measurements
from views.tech_packs import render_tech_packs

from views.clients import render_clients
from views.orders import render_orders
from views.expenses import render_expenses
from views.pricing import render_pricing
from views.revenue_profit import render_revenue_profit

from views.help_support import render_help_support
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
    initial_sidebar_state="collapsed",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL RESET
       ======================================================== */

    html,
    body {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }

    * {
        box-sizing: border-box;
    }


    /* ========================================================
       REMOVE STREAMLIT DEFAULT SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        display: none !important;
    }


    /* ========================================================
       REMOVE STREAMLIT SIDEBAR TOGGLE
       ======================================================== */

    button[kind="headerNoPadding"] {
        display: none !important;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }


    /* ========================================================
       MAIN APP
       ======================================================== */

    [data-testid="stAppViewContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        background: transparent !important;
    }

    [data-testid="stMain"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        background: transparent !important;
    }

    [data-testid="stMainBlockContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }


    /* ========================================================
       BACKGROUND
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
       IMAGES
       ======================================================== */

    img {
        max-width: 100% !important;
        height: auto !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton {
        max-width: 100% !important;
    }

    .stButton > button {
        max-width: 100% !important;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    input,
    textarea,
    select {
        font-size: 16px !important;
    }


    /* ========================================================
       MOBILE TOP NAVIGATION
       ======================================================== */

    .stylesense-mobile-topbar {

        position: fixed !important;

        top: 0 !important;
        left: 0 !important;

        width: 100% !important;

        height: 58px !important;

        z-index: 999999 !important;

        display: flex !important;

        align-items: center !important;

        background:
            rgba(31, 41, 45, 0.98) !important;

        border-bottom:
            1px solid
            rgba(57, 255, 20, 0.25) !important;

        box-shadow:
            0 4px 20px
            rgba(0, 0, 0, 0.30) !important;

        backdrop-filter:
            blur(15px) !important;

        -webkit-backdrop-filter:
            blur(15px) !important;

        padding:
            5px 6px !important;
    }


    /* ========================================================
       TOPBAR ROW
       ======================================================== */

    .stylesense-mobile-topbar
    [data-testid="stHorizontalBlock"] {

        display: flex !important;

        flex-direction: row !important;

        flex-wrap: nowrap !important;

        align-items: center !important;

        justify-content: space-between !important;

        width: 100% !important;

        gap: 2px !important;

        margin: 0 !important;
    }


    /* ========================================================
       TOPBAR COLUMNS
       ======================================================== */

    .stylesense-mobile-topbar
    [data-testid="stColumn"] {

        min-width: 0 !important;

        padding: 0 !important;

        flex: 1 1 0 !important;

        display: flex !important;

        align-items: center !important;

        justify-content: center !important;
    }


    /* ========================================================
       TOPBAR BUTTON CONTAINER
       ======================================================== */

    .stylesense-mobile-topbar
    .stButton {

        width: 100% !important;

        margin: 0 !important;

        padding: 0 !important;
    }


    /* ========================================================
       TOPBAR BUTTON
       ======================================================== */

    .stylesense-mobile-topbar
    .stButton > button {

        width: 100% !important;

        height: 46px !important;

        min-height: 46px !important;

        padding: 0 !important;

        margin: 0 !important;

        background:
            transparent !important;

        border:
            none !important;

        border-radius:
            10px !important;

        color:
            #FFFFFF !important;

        font-size:
            20px !important;

        line-height:
            1 !important;

        box-shadow:
            none !important;
    }


    .stylesense-mobile-topbar
    .stButton > button:hover {

        background:
            rgba(57, 255, 20, 0.10) !important;

        color:
            #39FF14 !important;
    }


    .stylesense-mobile-topbar
    .stButton > button:focus {

        background:
            rgba(57, 255, 20, 0.12) !important;

        color:
            #39FF14 !important;

        outline:
            none !important;

        box-shadow:
            none !important;
    }


    /* ========================================================
       PAGE TOP SPACE
       ======================================================== */

    .stylesense-page-wrapper {

        width: 100% !important;

        padding-top: 0 !important;
    }


    /* ========================================================
       LEFT DRAWER
       ======================================================== */

    .stylesense-mobile-drawer {

        position: fixed !important;

        top: 0 !important;

        left: 0 !important;

        width: 300px !important;

        max-width: 82vw !important;

        height: 100vh !important;

        height: 100dvh !important;

        z-index: 1000001 !important;

        overflow-y: auto !important;

        overflow-x: hidden !important;

        padding:
            20px
            16px
            35px
            16px !important;

        background:
            linear-gradient(
                180deg,
                #263238 0%,
                #263238 70%,
                #1F292D 100%
            ) !important;

        border-right:
            2px solid
            #39FF14 !important;

        box-shadow:
            8px 0 35px
            rgba(0, 0, 0, 0.55) !important;

        transform:
            translateX(0) !important;
    }


    /* ========================================================
       DRAWER SCROLLBAR
       ======================================================== */

    .stylesense-mobile-drawer::-webkit-scrollbar {
        width: 5px;
    }

    .stylesense-mobile-drawer::-webkit-scrollbar-track {
        background: transparent;
    }

    .stylesense-mobile-drawer::-webkit-scrollbar-thumb {
        background: rgba(57, 255, 20, 0.30);
        border-radius: 10px;
    }


    /* ========================================================
       DRAWER CONTENT
       ======================================================== */

    .stylesense-mobile-drawer-content {

        width: 100% !important;

        min-height: 100% !important;

        position: relative !important;
    }


    /* ========================================================
       DRAWER BRAND
       ======================================================== */

    .stylesense-mobile-drawer
    .stylesense-brand {

        font-size: 25px;

        font-weight: 800;

        letter-spacing: -0.5px;

        margin-bottom: 0;
    }


    .stylesense-mobile-drawer
    .stylesense-brand-accent {

        color: #39FF14;
    }


    .stylesense-mobile-drawer
    .stylesense-tagline {

        color: #AAB7BB !important;

        font-size: 11px;

        margin-top: -4px;

        margin-bottom: 14px;
    }


    /* ========================================================
       DRAWER BUTTONS
       ======================================================== */

    .stylesense-mobile-drawer
    .stButton {

        width: 100% !important;

        margin: 0 !important;

        padding: 0 !important;
    }


    .stylesense-mobile-drawer
    .stButton > button {

        width: 100% !important;

        min-height: 44px !important;

        margin-bottom: 5px !important;

        text-align: left !important;

        padding:
            8px 12px !important;

        background:
            rgba(57, 255, 20, 0.05) !important;

        color:
            #FFFFFF !important;

        border:
            1px solid
            rgba(57, 255, 20, 0.08) !important;

        border-radius:
            10px !important;

        box-shadow:
            none !important;
    }


    .stylesense-mobile-drawer
    .stButton > button:hover {

        background:
            rgba(57, 255, 20, 0.14) !important;

        border-color:
            rgba(57, 255, 20, 0.30) !important;

        color:
            #39FF14 !important;
    }


    /* ========================================================
       DRAWER HEADINGS
       ======================================================== */

    .stylesense-sidebar-section {

        margin-top: 16px;

        margin-bottom: 7px;

        padding:
            6px 5px;

        color:
            #8DFF70 !important;

        font-size:
            11px;

        font-weight:
            800;

        letter-spacing:
            1.2px;

        text-transform:
            uppercase;
    }


    /* ========================================================
       DRAWER CLOSE BUTTON
       ======================================================== */

    .stylesense-mobile-drawer
    .stylesense-close-button
    .stButton > button {

        background:
            rgba(255, 255, 255, 0.05) !important;

        border:
            1px solid
            rgba(255, 255, 255, 0.08) !important;

        text-align:
            center !important;

        color:
            #FFFFFF !important;

        margin-bottom:
            12px !important;
    }


    /* ========================================================
       OVERLAY
       ======================================================== */

    .stylesense-mobile-overlay {

        position: fixed !important;

        top: 0 !important;

        left: 0 !important;

        width: 100vw !important;

        height: 100vh !important;

        height: 100dvh !important;

        z-index: 1000000 !important;

        background:
            rgba(0, 0, 0, 0.50) !important;
    }


    /* ========================================================
       MOBILE CONTENT
       ======================================================== */

    @media (max-width: 600px) {

        header[data-testid="stHeader"] {
            display: none !important;
        }

        [data-testid="stMainBlockContainer"] {

            width: 100% !important;

            max-width: 100% !important;

            padding:
                76px
                14px
                30px
                14px !important;
        }

        h1 {
            font-size: 28px !important;
            line-height: 1.15 !important;
        }

        h2 {
            font-size: 23px !important;
            line-height: 1.2 !important;
        }

        h3 {
            font-size: 19px !important;
            line-height: 1.25 !important;
        }

        .stButton > button {

            min-height:
                46px !important;

            border-radius:
                12px !important;
        }

        [data-testid="stHorizontalBlock"] {

            width: 100% !important;

            max-width: 100% !important;

            min-width: 0 !important;
        }

        [data-testid="stColumn"] {

            min-width: 0 !important;

            max-width: 100% !important;
        }

        [data-testid="stDataFrame"] {

            max-width: 100% !important;

            overflow-x: auto !important;
        }

        [data-testid="stFileUploader"] {

            max-width: 100% !important;
        }

        [data-testid="stAlert"] {

            max-width: 100% !important;
        }
    }


    /* ========================================================
       DESKTOP
       ======================================================== */

    @media (min-width: 601px) {

        .stylesense-mobile-topbar {
            display: none !important;
        }

        .stylesense-mobile-drawer {
            display: none !important;
        }

        .stylesense-mobile-overlay {
            display: none !important;
        }

        [data-testid="stMainBlockContainer"] {

            width: 100% !important;

            max-width: 100% !important;

            padding:
                32px
                40px
                40px
                40px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
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

    "mobile_menu_open": False,

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

        st.session_state.user_id = (
            current_user["id"]
        )

        st.session_state.user_name = (
            current_user["full_name"]
        )

        st.session_state.user_email = (
            current_user["email"]
        )

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


    if status == "generating":

        st.info(
            "🎨 Your AI fashion design is being generated..."
        )


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

    "Design Library":
        render_design_library,

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

    "Color Matcher":
        render_color_matcher,

    "Fashion News":
        render_fashion_news,

    "Fashion Magazine":
        render_fashion_magazine,

    "AI Fashion Trends":
        render_fashion_trends,

    "AI Virtual Stylist":
        render_virtual_stylist,

    "Production Manager":
        render_production_manager,

    "Inventory":
        render_inventory,

    "Measurements":
        render_measurements,

    "Tech Packs":
        render_tech_packs,

    "Clients":
        render_clients,

    "Orders":
        render_orders,

    "Expenses":
        render_expenses,

    "Pricing":
        render_pricing,

    "Revenue & Profit":
        render_revenue_profit,

    "Fashion Professionals":
        render_profiles,

    "Marketplace":
        render_marketplace,

    "Settings":
        render_settings,

    "Help & Support":
        render_help_support,
}


# ============================================================
# NAVIGATION HELPER
# ============================================================

def navigate_to(page):

    st.session_state.main_navigation = page

    st.session_state.mobile_menu_open = False

    st.rerun()


# ============================================================
# MOBILE TOP BAR
#
# THIS IS ALWAYS FIXED AT THE TOP.
#
# ☰   🏠   🎨   🤖   📚   ⚙️
# ============================================================

st.markdown(
    '<div class="stylesense-mobile-topbar">',
    unsafe_allow_html=True
)


(
    mobile_menu_col,
    mobile_home_col,
    mobile_design_col,
    mobile_ai_col,
    mobile_library_col,
    mobile_settings_col,
) = st.columns(
    [0.85, 1, 1, 1, 1, 1]
)


# ============================================================
# MENU
# ============================================================

with mobile_menu_col:

    if st.button(
        "☰",
        key="mobile_menu_button",
        use_container_width=True,
    ):

        st.session_state.mobile_menu_open = not (
            st.session_state.get(
                "mobile_menu_open",
                False
            )
        )

        st.rerun()


# ============================================================
# HOME
# ============================================================

with mobile_home_col:

    if st.button(
        "🏠",
        key="mobile_home_button",
        use_container_width=True,
    ):

        navigate_to(
            "Dashboard"
        )


# ============================================================
# DESIGN
# ============================================================

with mobile_design_col:

    if st.button(
        "🎨",
        key="mobile_design_button",
        use_container_width=True,
    ):

        navigate_to(
            "Design Studio"
        )


# ============================================================
# AI TEAM
# ============================================================

with mobile_ai_col:

    if st.button(
        "🤖",
        key="mobile_ai_button",
        use_container_width=True,
    ):

        navigate_to(
            "AI Team"
        )


# ============================================================
# LIBRARY
# ============================================================

with mobile_library_col:

    if st.button(
        "📚",
        key="mobile_library_button",
        use_container_width=True,
    ):

        navigate_to(
            "Design Library"
        )


# ============================================================
# SETTINGS
# ============================================================

with mobile_settings_col:

    if st.button(
        "⚙️",
        key="mobile_settings_button",
        use_container_width=True,
    ):

        navigate_to(
            "Settings"
        )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# MOBILE LEFT DRAWER
# ============================================================

if st.session_state.get(
    "mobile_menu_open",
    False
):

    # ========================================================
    # DARK OVERLAY
    # ========================================================

    st.markdown(
        '<div class="stylesense-mobile-overlay"></div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # LEFT DRAWER
    # ========================================================

    st.markdown(
        '<div class="stylesense-mobile-drawer">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="stylesense-mobile-drawer-content">',
        unsafe_allow_html=True
    )


    # ========================================================
    # BRAND
    # ========================================================

    st.markdown(
        """
        <div class="stylesense-brand">
            ✦ Style<span class="stylesense-brand-accent">
            Sense
            </span>
        </div>

        <div class="stylesense-tagline">
            AI Fashion Operating System
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CLOSE
    # ========================================================

    st.markdown(
        '<div class="stylesense-close-button">',
        unsafe_allow_html=True
    )

    if st.button(
        "✕  Close Menu",
        key="mobile_drawer_close",
        use_container_width=True,
    ):

        st.session_state.mobile_menu_open = False

        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # WORKSPACE
    # ========================================================

    st.markdown(
        '<div class="stylesense-sidebar-section">'
        'WORKSPACE'
        '</div>',
        unsafe_allow_html=True
    )


    mobile_workspace_navigation = [

        ("🏠", "Dashboard"),

        ("📁", "Projects"),

        ("🤖", "AI Team"),

    ]


    for icon, label in mobile_workspace_navigation:

        if st.button(
            f"{icon}  {label}",
            key=f"mobile_drawer_workspace_{label}",
            use_container_width=True,
        ):

            navigate_to(
                label
            )


    # ========================================================
    # AI DESIGN
    # ========================================================

    st.markdown(
        '<div class="stylesense-sidebar-section">'
        '🎨 AI DESIGN'
        '</div>',
        unsafe_allow_html=True
    )


    mobile_ai_navigation = [

        ("✨", "Design Studio"),

        ("📚", "Design Library"),

        ("✏️", "AI Design Editor"),

        ("💡", "Fashion Inspiration"),

        ("🎨", "Color Matcher"),

        ("🧵", "Fabric Advisor"),

        ("📸", "Outfit Analyzer"),

        ("👗", "AI Virtual Stylist"),

        ("🎨", "Logo Generator"),

    ]


    for icon, label in mobile_ai_navigation:

        if st.button(
            f"{icon}  {label}",
            key=f"mobile_drawer_ai_{label}",
            use_container_width=True,
        ):

            navigate_to(
                label
            )


    # ========================================================
    # FASHION INTELLIGENCE
    # ========================================================

    st.markdown(
        '<div class="stylesense-sidebar-section">'
        '🧠 FASHION INTELLIGENCE'
        '</div>',
        unsafe_allow_html=True
    )


    mobile_intelligence_navigation = [

        ("📈", "AI Fashion Trends"),

        ("📰", "Fashion News"),

        ("📰", "Fashion Magazine"),

    ]


    for icon, label in mobile_intelligence_navigation:

        if st.button(
            f"{icon}  {label}",
            key=f"mobile_drawer_intelligence_{label}",
            use_container_width=True,
        ):

            navigate_to(
                label
            )


    # ========================================================
    # PRODUCTION
    # ========================================================

    st.markdown(
        '<div class="stylesense-sidebar-section">'
        '🏭 PRODUCTION'
        '</div>',
        unsafe_allow_html=True
    )


    mobile_production_navigation = [

        ("🏭", "Production Manager"),

        ("📦", "Inventory"),

        ("📏", "Measurements"),

        ("📋", "Tech Packs"),

    ]


    for icon, label in mobile_production_navigation:

        if st.button(
            f"{icon}  {label}",
            key=f"mobile_drawer_production_{label}",
            use_container_width=True,
        ):

            navigate_to(
                label
            )


    # ========================================================
    # BUSINESS
    # ========================================================

    st.markdown(
        '<div class="stylesense-sidebar-section">'
        '💼 BUSINESS'
        '</div>',
        unsafe_allow_html=True
    )


    mobile_business_navigation = [

        ("👥", "Clients"),

        ("🛒", "Orders"),

        ("💸", "Expenses"),

        ("💰", "Pricing"),

        ("📊", "Revenue & Profit"),

    ]


    for icon, label in mobile_business_navigation:

        if st.button(
            f"{icon}  {label}",
            key=f"mobile_drawer_business_{label}",
            use_container_width=True,
        ):

            navigate_to(
                label
            )


    # ========================================================
    # FASHION PROFESSIONAL
    # ========================================================

    st.markdown(
        '<div class="stylesense-sidebar-section">'
        '👥 FASHION PROFESSIONAL'
        '</div>',
        unsafe_allow_html=True
    )


    mobile_professional_navigation = [

        ("👔", "Fashion Professionals"),

        ("🛍️", "Marketplace"),

    ]


    for icon, label in mobile_professional_navigation:

        if st.button(
            f"{icon}  {label}",
            key=f"mobile_drawer_professional_{label}",
            use_container_width=True,
        ):

            navigate_to(
                label
            )


    # ========================================================
    # AI SHORTCUTS
    # ========================================================

    st.markdown(
        '<div class="stylesense-sidebar-section">'
        '⚡ AI SHORTCUTS'
        '</div>',
        unsafe_allow_html=True
    )


    if st.button(
        "✦  Ask StyleSense",
        key="mobile_drawer_ask_stylesense",
        use_container_width=True,
    ):

        navigate_to(
            "Ask StyleSense"
        )


    if st.button(
        "🚀  AI Co-Founder",
        key="mobile_drawer_ai_cofounder",
        use_container_width=True,
    ):

        navigate_to(
            "AI Co-Founder"
        )


    if st.button(
        "✓  My Tasks",
        key="mobile_drawer_tasks",
        use_container_width=True,
    ):

        navigate_to(
            "My Tasks"
        )


    if st.button(
        "🔔  Notifications",
        key="mobile_drawer_notifications",
        use_container_width=True,
    ):

        navigate_to(
            "Notifications"
        )


    # ========================================================
    # SYSTEM
    # ========================================================

    st.markdown(
        '<div class="stylesense-sidebar-section">'
        '⚙️ SYSTEM'
        '</div>',
        unsafe_allow_html=True
    )


    if st.button(
        "⚙  Settings",
        key="mobile_drawer_settings",
        use_container_width=True,
    ):

        navigate_to(
            "Settings"
        )


    if st.button(
        "❓  Help & Support",
        key="mobile_drawer_help",
        use_container_width=True,
    ):

        navigate_to(
            "Help & Support"
        )


    if st.button(
        "↪  Logout",
        key="mobile_drawer_logout",
        use_container_width=True,
    ):

        try:

            logout_user()

        except Exception:

            pass

        st.session_state.logged_in = False

        st.session_state.user_id = None

        st.session_state.user_name = None

        st.session_state.user_email = None

        st.session_state.mobile_menu_open = False

        st.rerun()


    # ========================================================
    # CLOSE DRAWER WRAPPERS
    # ========================================================

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# PAGE ROUTING
# ============================================================

current_page = st.session_state.get(
    "main_navigation",
    "Dashboard"
)


# ============================================================
# SPECIAL PAGE — MY TASKS
# ============================================================

if current_page == "My Tasks":

    st.title(
        "✓ My Tasks"
    )

    st.caption(
        "Your fashion workflow and AI tasks."
    )

    st.info(
        "Task management is coming next."
    )


# ============================================================
# SPECIAL PAGE — NOTIFICATIONS
# ============================================================

elif current_page == "Notifications":

    st.title(
        "🔔 Notifications"
    )

    st.caption(
        "Stay updated with your StyleSense workspace."
    )

    st.info(
        "Notifications will appear here."
    )


# ============================================================
# WORKSPACE
# ============================================================

elif current_page == "Workspace":

    current_project = st.session_state.get(
        "current_project"
    )

    if current_project is None:

        st.warning(
            "Open a project first."
        )

        st.info(
            "Go to Projects and click Open Project."
        )

    else:

        render_workspace()


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