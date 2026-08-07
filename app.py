import streamlit as st
from pathlib import Path
from database.database import init_database
init_database()

from views.fashion_cofounder import render_fashion_cofounder
from views.dashboard import render_dashboard
from views.find_designers import render_find_designers
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


PAGES = {
    "🏠 Dashboard": render_dashboard,
    "📂 Projects": render_projects,
    "🤖 AI Team": render_ai_team,
    "✨ AI Design Studio": render_design_studio,
    "💡 Fashion Inspiration": render_fashion_inspiration,
    "✏ AI Design Editor": render_design_editor,
    "🚀 AI Fashion Co-Founder": render_fashion_cofounder,
    "🎨 Logo Generator": render_logo_generator,
    "📸 Outfit Analyzer": render_outfit_analyzer,
    "🤖 Fashion Assistant": render_fashion_assistant,
    "🧵 Fabric Advisor": render_fabric_advisor,
    "📚 Design Library": render_design_library,
    "🎨 Color Matcher": render_color_matcher,
    "📰 Fashion News": render_fashion_news,
    "📰 Fashion Magazine": render_fashion_magazine,
    "🔥 AI Fashion Trends": render_fashion_trends,
    "👗 Find Designers": render_find_designers,
    "👔 AI Virtual Stylist": render_virtual_stylist,
    "⚙ Settings": render_settings,
}

def load_css():

    try:
        with open("assets/css/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        st.warning("CSS file not found.")


st.set_page_config(
    page_title="StyleSense AI OS",
    page_icon="👗",
    layout="wide"
)

load_css()

# ==========================
# SESSION STATE
# ==========================

if "saved_designs" not in st.session_state:
    st.session_state.saved_designs = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_design" not in st.session_state:
    st.session_state.current_design = ""

if "current_image" not in st.session_state:
    st.session_state.current_image = None

if "current_project" not in st.session_state:
    st.session_state.current_project = None

# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    logo_path = Path("assets/logo.png")

    if logo_path.exists():
        st.image(str(logo_path), width=80)

    st.title("👗 StyleSense AI OS")
    st.caption("Powered by Chekwube Empire")
    st.success("🟢 Gemini Connected")
    navigation = ["🖥 Workspace"] + list(PAGES.keys())

    page = st.radio(
        "Navigation",
        navigation
    )

if page == "🖥 Workspace":

    if st.session_state.current_project:

        render_workspace()

    else:

        st.warning("Open a project first.")
else:

    PAGES[page]()