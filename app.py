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
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StyleSense AI OS",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CSS_PATH = BASE_DIR / "assets" / "css" / "style.css"


# ============================================================
# LOAD CSS
# ============================================================

def load_css():
    """Load StyleSense global CSS."""

    if not CSS_PATH.exists():
        print(f"CSS FILE NOT FOUND: {CSS_PATH}")
        return

    try:
        with open(CSS_PATH, "r", encoding="utf-8") as file:
            css = file.read()

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True,
        )

    except Exception as error:
        print("CSS LOAD ERROR:", repr(error))


load_css()


# ============================================================
# DATABASE
# ============================================================

init_database()


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_SESSION_STATE = {
    "logged_in": False,
    "user_id": None,
    "user_name": None,
    "user_email": None,
    "user_profession": "Fashion Designer",
    "user_avatar_url": "",

    "auth_page": "login",

    "main_navigation": "Dashboard",

    # Mobile navigation
    "mobile_menu_open": False,
    "sidebar_open": False,

    # Settings
    "settings_section": "Account",

    # Designs
    "saved_designs": [],
    "saved_inspirations": [],
    "collections": [],
    "messages": [],
    "current_design": "",
    "current_image": None,

    # Background generation
    "design_generation_job_id": None,
    "design_generation_status": None,
    "design_generation_result": None,
    "design_generation_error": None,

    # Projects
    "current_project": None,
    "open_workspace": False,

    # Dashboard
    "dashboard_ai_prompt": "",

    # Fashion news
    "fashion_news_articles": [],
    "fashion_news_generated": False,

    # Design Studio
    "open_design_studio": False,
    "studio_reference_image_url": None,
    "studio_reference_title": "",
    "studio_reference_photographer": "",

    # Dashboard tasks
    "dashboard_tasks": [
        {
            "title": "Finalize Design #12",
            "context": "Summer Collection",
            "priority": "HIGH",
            "completed": False,
        },
        {
            "title": "Select fabrics",
            "context": "Summer Collection",
            "priority": "MEDIUM",
            "completed": False,
        },
        {
            "title": "Review trend report",
            "context": "AI Trend Analyst",
            "priority": "LOW",
            "completed": False,
        },
    ],
}


for key, value in DEFAULT_SESSION_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# AUTHENTICATION
# ============================================================

if not st.session_state.logged_in:

    current_user = get_current_user()

    if current_user:

        st.session_state.logged_in = True

        st.session_state.user_id = current_user["id"]

        st.session_state.user_name = (
            current_user.get("full_name")
            or "Fashion Designer"
        )

        st.session_state.user_email = (
            current_user.get("email")
            or ""
        )

        st.session_state.user_profession = (
            current_user.get(
                "profession",
                "Fashion Designer",
            )
            or "Fashion Designer"
        )

        st.session_state.user_avatar_url = (
            current_user.get(
                "avatar_url",
                "",
            )
            or ""
        )

        st.rerun()

    else:

        render_auth()

        st.stop()


# ============================================================
# PAGE REGISTRY
# ============================================================

PAGES = {

    # WORKSPACE
    "Dashboard": render_dashboard,
    "Projects": render_projects,
    "AI Team": render_ai_team,

    # AI DESIGN
    "Design Studio": render_design_studio,
    "Design Library": render_design_library,
    "Fashion Inspiration": render_fashion_inspiration,
    "AI Design Editor": render_design_editor,
    "AI Co-Founder": render_fashion_cofounder,
    "Logo Generator": render_logo_generator,
    "Outfit Analyzer": render_outfit_analyzer,
    "Ask StyleSense": render_fashion_assistant,
    "Fabric Advisor": render_fabric_advisor,
    "Color Matcher": render_color_matcher,
    "AI Virtual Stylist": render_virtual_stylist,

    # FASHION INTELLIGENCE
    "Fashion News": render_fashion_news,
    "Fashion Magazine": render_fashion_magazine,
    "AI Fashion Trends": render_fashion_trends,

    # PRODUCTION
    "Production Manager": render_production_manager,
    "Inventory": render_inventory,
    "Measurements": render_measurements,
    "Tech Packs": render_tech_packs,

    # BUSINESS
    "Clients": render_clients,
    "Orders": render_orders,
    "Expenses": render_expenses,
    "Pricing": render_pricing,
    "Revenue & Profit": render_revenue_profit,

    # COMMUNITY
    "Fashion Professionals": render_profiles,
    "Marketplace": render_marketplace,

    # SYSTEM
    "Settings": render_settings,
    "Help & Support": render_help_support,
}


# ============================================================
# NAVIGATION FUNCTIONS
#
# IMPORTANT:
# These functions are used as Streamlit callbacks.
# DO NOT call st.rerun() inside them.
#
# Streamlit automatically reruns the application after
# an on_click callback finishes.
# ============================================================

def navigate_to(page):
    """Navigate to a StyleSense page."""

    st.session_state.main_navigation = page

    st.session_state.mobile_menu_open = False
    st.session_state.sidebar_open = False


def open_settings(section):
    """Open a specific StyleSense Settings section."""

    st.session_state.main_navigation = "Settings"

    st.session_state.settings_section = section

    st.session_state.mobile_menu_open = False
    st.session_state.sidebar_open = False


def open_notifications():
    """Open Settings → Notifications."""

    st.session_state.main_navigation = "Settings"

    st.session_state.settings_section = "Notifications"

    st.session_state.mobile_menu_open = False
    st.session_state.sidebar_open = False


def open_profile():
    """Open Settings → Account."""

    st.session_state.main_navigation = "Settings"

    st.session_state.settings_section = "Account"

    st.session_state.mobile_menu_open = False
    st.session_state.sidebar_open = False


def open_appearance():
    """Open Settings → Appearance."""

    st.session_state.main_navigation = "Settings"

    st.session_state.settings_section = "Appearance"

    st.session_state.mobile_menu_open = False
    st.session_state.sidebar_open = False


def toggle_sidebar():
    """Toggle the mobile sidebar."""

    current_state = st.session_state.get(
        "mobile_menu_open",
        False,
    )

    new_state = not current_state

    st.session_state.mobile_menu_open = new_state
    st.session_state.sidebar_open = new_state


def close_mobile_sidebar():
    """Close the mobile sidebar."""

    st.session_state.mobile_menu_open = False
    st.session_state.sidebar_open = False


def perform_logout():
    """Log the current user out."""

    try:

        logout_user()

    except Exception:

        pass


    st.session_state.logged_in = False

    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_email = None

    st.session_state.user_profession = "Fashion Designer"

    st.session_state.user_avatar_url = ""

    st.session_state.sidebar_open = False
    st.session_state.mobile_menu_open = False

    st.session_state.settings_section = "Account"


# ============================================================
# MOBILE SIDEBAR VISIBILITY
# ============================================================

if st.session_state.get("mobile_menu_open", False):

    st.markdown(
        """
        <style>
        @media (max-width: 768px) {

            section[data-testid="stSidebar"] {
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
                transform: translateX(0) !important;
            }

        }
        </style>
        """,
        unsafe_allow_html=True,
    )

else:

    st.markdown(
        """
        <style>
        @media (max-width: 768px) {

            section[data-testid="stSidebar"] {
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                transform: translateX(-100%) !important;
            }

        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# TOP HEADER
# ============================================================

topbar = st.container(
    key="stylesense_topbar"
)


with topbar:

    # ========================================================
    # TOP ROW
    # ========================================================

    top_row = st.container(
        key="stylesense_top_row"
    )


    with top_row:

        (
            menu_column,
            brand_column,
            spacer_column,
            notification_column,
            profile_column,
            appearance_column,
        ) = st.columns(
            [
                0.55,
                2.2,
                4.2,
                1.25,
                1.0,
                1.15,
            ],
            vertical_alignment="center",
        )


        # ====================================================
        # HAMBURGER
        # ====================================================

        with menu_column:

            st.button(
                "☰",
                key="top_menu_button",
                help="Open navigation",
                use_container_width=True,
                on_click=toggle_sidebar,
            )


        # ====================================================
        # BRAND
        # ====================================================

        with brand_column:

            st.markdown(
                "✦ StyleSense"
            )


        # ====================================================
        # NOTIFICATIONS
        # ====================================================

        with notification_column:

            st.button(
                "🔔",
                key="top_notifications",
                help="Notifications",
                use_container_width=True,
                on_click=open_notifications,
            )


        # ====================================================
        # PROFILE
        # ====================================================

        with profile_column:

            st.button(
                "👤",
                key="top_profile",
                help="Account",
                use_container_width=True,
                on_click=open_profile,
            )


        # ====================================================
        # APPEARANCE
        # ====================================================

        with appearance_column:

            st.button(
                "◐",
                key="top_appearance",
                help="Appearance",
                use_container_width=True,
                on_click=open_appearance,
            )


    # ========================================================
    # QUICK NAVIGATION
    # ========================================================

    navigation_row = st.container(
        key="stylesense_navigation_row"
    )


    with navigation_row:

        (
            nav_home,
            nav_product,
            nav_create,
            nav_ai,
        ) = st.columns(
            [
                1.3,
                1.3,
                1.3,
                1.3,
            ],
            vertical_alignment="center",
        )


        with nav_home:

            st.button(
                "🏠  Home",
                key="top_nav_home",
                use_container_width=True,
                on_click=navigate_to,
                args=("Dashboard",),
            )


        with nav_product:

            st.button(
                "📦  Product",
                key="top_nav_product",
                use_container_width=True,
                on_click=navigate_to,
                args=("Production Manager",),
            )


        with nav_create:

            st.button(
                "✨  Create",
                key="top_nav_create",
                use_container_width=True,
                on_click=navigate_to,
                args=("Design Studio",),
            )


        with nav_ai:

            st.button(
                "🤖  AI Teams",
                key="top_nav_ai",
                use_container_width=True,
                on_click=navigate_to,
                args=("AI Team",),
            )


# ============================================================
# NATIVE STYLESENSE SIDEBAR
# ============================================================

with st.sidebar:

    (
        sidebar_brand_column,
        sidebar_close_column,
    ) = st.columns(
        [4, 1],
        vertical_alignment="center",
    )


    # ========================================================
    # SIDEBAR BRAND
    # ========================================================

    with sidebar_brand_column:

        st.markdown(
            "✦ StyleSense"
        )

        st.caption(
            "AI Fashion Operating System"
        )


    # ========================================================
    # SIDEBAR CLOSE
    # ========================================================

    with sidebar_close_column:

        st.button(
            "✕",
            key="sidebar_close_button",
            help="Close sidebar",
            on_click=close_mobile_sidebar,
        )


    # ========================================================
    # USER PROFILE
    # ========================================================

    user_name = (
        st.session_state.get(
            "user_name",
            "Fashion Designer",
        )
        or "Fashion Designer"
    )

    user_email = (
        st.session_state.get(
            "user_email",
            "",
        )
        or ""
    )

    user_profession = (
        st.session_state.get(
            "user_profession",
            "Fashion Designer",
        )
        or "Fashion Designer"
    )

    user_avatar_url = (
        st.session_state.get(
            "user_avatar_url",
            "",
        )
        or ""
    )


    (
        avatar_column,
        profile_info_column,
    ) = st.columns(
        [0.8, 2.8],
        vertical_alignment="center",
    )


    with avatar_column:

        if user_avatar_url:

            st.image(
                user_avatar_url,
                width=52,
            )

        else:

            first_letter = (
                user_name.strip()[0].upper()
                if user_name.strip()
                else "F"
            )

            st.markdown(
                f"### {first_letter}"
            )


    with profile_info_column:

        st.markdown(
            f"**{user_name}**"
        )

        st.caption(
            user_profession
        )

        if user_email:

            st.caption(
                user_email
            )


    st.divider()


    # ========================================================
    # WORKSPACE
    # ========================================================

    st.caption("WORKSPACE")


    st.button(
        "🏠  Dashboard",
        key="side_dashboard",
        use_container_width=True,
        on_click=navigate_to,
        args=("Dashboard",),
    )


    st.button(
        "📁  Projects",
        key="side_projects",
        use_container_width=True,
        on_click=navigate_to,
        args=("Projects",),
    )


    st.button(
        "🤖  AI Team",
        key="side_ai_team",
        use_container_width=True,
        on_click=navigate_to,
        args=("AI Team",),
    )


    # ========================================================
    # AI DESIGN
    # ========================================================

    st.caption("🎨 AI DESIGN")


    ai_design_navigation = [
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


    for index, (icon, label) in enumerate(
        ai_design_navigation
    ):

        st.button(
            f"{icon}  {label}",
            key=f"side_ai_design_{index}",
            use_container_width=True,
            on_click=navigate_to,
            args=(label,),
        )


    # ========================================================
    # FASHION INTELLIGENCE
    # ========================================================

    st.caption("🧠 FASHION INTELLIGENCE")


    intelligence_navigation = [
        ("📈", "AI Fashion Trends"),
        ("📰", "Fashion News"),
        ("📰", "Fashion Magazine"),
    ]


    for index, (icon, label) in enumerate(
        intelligence_navigation
    ):

        st.button(
            f"{icon}  {label}",
            key=f"side_intelligence_{index}",
            use_container_width=True,
            on_click=navigate_to,
            args=(label,),
        )


    # ========================================================
    # PRODUCTION
    # ========================================================

    st.caption("🏭 PRODUCTION")


    production_navigation = [
        ("🏭", "Production Manager"),
        ("📦", "Inventory"),
        ("📏", "Measurements"),
        ("📋", "Tech Packs"),
    ]


    for index, (icon, label) in enumerate(
        production_navigation
    ):

        st.button(
            f"{icon}  {label}",
            key=f"side_production_{index}",
            use_container_width=True,
            on_click=navigate_to,
            args=(label,),
        )


    # ========================================================
    # BUSINESS
    # ========================================================

    st.caption("💼 BUSINESS")


    business_navigation = [
        ("👥", "Clients"),
        ("🛒", "Orders"),
        ("💸", "Expenses"),
        ("💰", "Pricing"),
        ("📊", "Revenue & Profit"),
    ]


    for index, (icon, label) in enumerate(
        business_navigation
    ):

        st.button(
            f"{icon}  {label}",
            key=f"side_business_{index}",
            use_container_width=True,
            on_click=navigate_to,
            args=(label,),
        )


    # ========================================================
    # FASHION PROFESSIONAL
    # ========================================================

    st.caption("👥 FASHION PROFESSIONAL")


    professional_navigation = [
        ("👔", "Fashion Professionals"),
        ("🛍️", "Marketplace"),
    ]


    for index, (icon, label) in enumerate(
        professional_navigation
    ):

        st.button(
            f"{icon}  {label}",
            key=f"side_professional_{index}",
            use_container_width=True,
            on_click=navigate_to,
            args=(label,),
        )


    # ========================================================
    # AI SHORTCUTS
    # ========================================================

    st.caption("⚡ AI SHORTCUTS")


    st.button(
        "✦  Ask StyleSense",
        key="side_ask_stylesense",
        use_container_width=True,
        on_click=navigate_to,
        args=("Ask StyleSense",),
    )


    st.button(
        "🚀  AI Co-Founder",
        key="side_ai_cofounder",
        use_container_width=True,
        on_click=navigate_to,
        args=("AI Co-Founder",),
    )


    st.button(
        "✓  My Tasks",
        key="side_tasks",
        use_container_width=True,
        on_click=navigate_to,
        args=("My Tasks",),
    )


    st.button(
        "🔔  Notifications",
        key="side_notifications",
        use_container_width=True,
        on_click=open_notifications,
    )


    # ========================================================
    # SYSTEM
    # ========================================================

    st.caption("⚙️ SYSTEM")


    st.button(
        "⚙  Settings",
        key="side_settings",
        use_container_width=True,
        on_click=navigate_to,
        args=("Settings",),
    )


    st.button(
        "❓  Help & Support",
        key="side_help",
        use_container_width=True,
        on_click=navigate_to,
        args=("Help & Support",),
    )


    st.button(
        "↪  Logout",
        key="side_logout",
        use_container_width=True,
        on_click=perform_logout,
    )


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

    status = job_status.get("status")


    if status == "generating":

        st.info(
            "🎨 Your AI fashion design is being generated..."
        )


    elif status == "completed":

        result = job_status.get("result")


        if result:

            st.session_state.design_generation_result = result

            st.session_state.current_image = result

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
                use_container_width=True,
            )


        else:

            st.warning(
                "The design finished generating, "
                "but no image was returned."
            )


        st.session_state.design_generation_job_id = None


    elif status == "failed":

        error = job_status.get("error")


        st.session_state.design_generation_status = (
            "failed"
        )

        st.session_state.design_generation_error = error


        st.error(
            "❌ AI design generation failed."
        )


        if error:

            st.caption(
                str(error)
            )


        st.session_state.design_generation_job_id = None


# ============================================================
# CURRENT PAGE
# ============================================================

current_page = st.session_state.get(
    "main_navigation",
    "Dashboard",
)


# ============================================================
# SPECIAL PAGES
# ============================================================

if current_page == "Notifications":

    st.title(
        "🔔 Notifications"
    )

    st.caption(
        "Stay updated with your StyleSense workspace."
    )

    st.info(
        "Your notifications will appear here."
    )


elif current_page == "My Tasks":

    st.title(
        "✓ My Tasks"
    )

    st.caption(
        "Your fashion workflow and AI tasks."
    )

    tasks = st.session_state.get(
        "dashboard_tasks",
        [],
    )


    if not tasks:

        st.info(
            "You currently have no tasks."
        )


    else:

        for index, task in enumerate(tasks):

            checked = st.checkbox(
                task["title"],
                value=task.get(
                    "completed",
                    False,
                ),
                key=f"my_tasks_{index}",
            )

            task["completed"] = checked

            st.caption(
                f'{task["context"]} • '
                f'{task["priority"]}'
            )


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
# NORMAL PAGES
# ============================================================

else:

    selected_page = PAGES.get(
        current_page
    )


    if selected_page:

        selected_page()


    else:

        st.error(
            f"Page not found: {current_page}"
        )