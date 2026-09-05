import re
from pathlib import Path

import streamlit as st

from database.dashboard import count_designers
from database.database import get_all_designs
from database.projects import get_projects


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

AVATAR_PATH = (
    PROJECT_ROOT
    / "assets"
    / "fashion_avatar.png"
)


# ============================================================
# NAVIGATION HELPER
# ============================================================

def navigate_to(page: str):
    """
    Navigate to another StyleSense page.

    Global navigation is owned by app.py.
    This helper is only for dashboard action buttons.
    """

    st.session_state.main_navigation = page
    st.rerun()


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_design_title(value) -> str:
    """Convert an AI-generated design description into a short title."""

    text = str(
        value or "AI Fashion Design"
    )

    # Remove markdown headings
    text = re.sub(
        r"^\s*#{1,6}\s*",
        "",
        text,
    )

    # Remove markdown emphasis
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        text,
    )

    text = re.sub(
        r"__(.*?)__",
        r"\1",
        text,
    )

    text = re.sub(
        r"\*(.*?)\*",
        r"\1",
        text,
    )

    text = re.sub(
        r"_(.*?)_",
        r"\1",
        text,
    )

    # Remove excessive whitespace
    text = " ".join(
        text.split()
    ).strip()

    if not text:
        return "AI Fashion Design"

    if len(text) > 90:
        text = (
            text[:87].rstrip()
            + "..."
        )

    return text


def get_first_name() -> str:
    """Return the logged-in user's first name."""

    name = (
        st.session_state.get(
            "user_name"
        )
        or "there"
    )

    parts = (
        str(name)
        .strip()
        .split()
    )

    return (
        parts[0]
        if parts
        else "there"
    )


# ============================================================
# DASHBOARD STYLING
# ============================================================

def render_dashboard_styles():
    """
    Dashboard-specific visual styling.

    Global navigation and sidebar styling belong to app.py
    and assets/css/style.css.
    """

    st.markdown(
        """
        <style>

        .stApp {
            background:
                radial-gradient(
                    circle at 8% 8%,
                    rgba(245, 166, 35, 0.28),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 92% 12%,
                    rgba(57, 255, 20, 0.14),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 15% 85%,
                    rgba(0, 168, 107, 0.25),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 85%,
                    rgba(57, 255, 20, 0.10),
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
            min-height: 100vh;
        }


        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            background: transparent !important;
        }


        div[data-testid="stVerticalBlockBorderWrapper"] {
            background:
                linear-gradient(
                    135deg,
                    rgba(0, 107, 69, 0.92),
                    rgba(38, 50, 56, 0.94)
                ) !important;

            border:
                1px solid
                rgba(57, 255, 20, 0.18) !important;

            border-radius: 24px !important;

            box-shadow:
                0 18px 50px
                rgba(0, 0, 0, 0.24) !important;
        }


        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            background: transparent !important;
        }


        div[data-baseweb="input"] {
            background:
                rgba(255, 255, 255, 0.96) !important;

            border:
                2px solid
                rgba(57, 255, 20, 0.25) !important;

            border-radius: 14px !important;
        }


        div[data-baseweb="input"] input {
            color: #263238 !important;
        }


        div[data-baseweb="input"] input::placeholder {
            color: #687277 !important;
        }


        div[data-testid="stButton"] button {
            background:
                rgba(0, 107, 69, 0.78) !important;

            color: #ffffff !important;

            border:
                1px solid
                rgba(57, 255, 20, 0.28) !important;

            border-radius: 12px !important;

            font-weight: 600 !important;

            transition:
                all 0.18s ease !important;
        }


        div[data-testid="stButton"] button:hover {
            background:
                #006B45 !important;

            border-color:
                #39FF14 !important;

            transform:
                translateY(-1px);
        }


        div[data-testid="stMetric"] {
            background:
                rgba(38, 50, 56, 0.65) !important;

            border:
                1px solid
                rgba(57, 255, 20, 0.16) !important;

            border-radius: 16px !important;

            padding: 14px !important;
        }


        div[data-testid="stMetricValue"] {
            color:
                #F5A623 !important;
        }


        div[data-testid="stMetricLabel"] {
            color:
                rgba(255, 255, 255, 0.82) !important;
        }


        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4 {
            color:
                #ffffff !important;
        }


        .stApp .stCaption {
            color:
                rgba(255, 255, 255, 0.72) !important;
        }


        hr {
            border-color:
                rgba(57, 255, 20, 0.16) !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SESSION STATE
# ============================================================

def initialize_dashboard_state():

    if "saved_designs" not in st.session_state:
        st.session_state.saved_designs = []

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "dashboard_tasks" not in st.session_state:

        st.session_state.dashboard_tasks = [
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
        ]


# ============================================================
# DATABASE
# ============================================================

def load_dashboard_data():

    user_id = st.session_state.get(
        "user_id"
    )

    # --------------------------------------------------------
    # PROJECTS
    # --------------------------------------------------------

    try:

        projects = (
            get_projects(
                user_id=user_id
            )
            or []
        )

    except Exception:

        projects = []

    # --------------------------------------------------------
    # DESIGNERS
    # --------------------------------------------------------

    try:

        designers = count_designers()

    except Exception:

        designers = 0

    # --------------------------------------------------------
    # DESIGNS
    # --------------------------------------------------------

    try:

        designs = (
            get_all_designs()
            or []
        )

    except Exception:

        designs = []

    return {
        "projects": projects,
        "designers": designers,
        "designs": designs,
    }


# ============================================================
# HERO / WELCOME SECTION
# ============================================================

def render_welcome_section(data):

    first_name = get_first_name()

    with st.container(border=True):

        left, right = st.columns(
            [3.2, 1.8],
            vertical_alignment="center",
        )

        # ====================================================
        # LEFT
        # ====================================================

        with left:

            st.markdown(
                f"### HELLO, {first_name.upper()}!"
            )

            st.markdown(
                "## What are you creating today?"
            )

            st.caption(
                "Your intelligent fashion workspace for "
                "design, creativity, research and business."
            )

            st.write("")

            # ------------------------------------------------
            # AI PROMPT
            # ------------------------------------------------

            prompt = st.text_input(
                "StyleSense AI",
                placeholder=(
                    "Ask StyleSense anything about your fashion idea..."
                ),
                label_visibility="collapsed",
                key="dashboard_prompt",
            )

            prompt_info, prompt_action = st.columns(
                [5, 1],
                vertical_alignment="center",
            )

            with prompt_info:

                st.caption(
                    "✨ Concepts • Designs • Fabrics • Styling • "
                    "Trends • Business"
                )

            with prompt_action:

                ask_ai = st.button(
                    "⚡ Ask AI",
                    use_container_width=True,
                    key="dashboard_generate",
                )

            if ask_ai:

                if not prompt.strip():

                    st.warning(
                        "Describe what you want to create first."
                    )

                else:

                    st.session_state.messages.append(
                        {
                            "role": "user",
                            "content": prompt.strip(),
                        }
                    )

                    st.session_state.dashboard_ai_prompt = (
                        prompt.strip()
                    )

                    navigate_to(
                        "Design Studio"
                    )

            # ------------------------------------------------
            # WORKSPACE STATISTICS
            # ------------------------------------------------

            st.write("")

            stats = [
                (
                    "📁",
                    "Projects",
                    len(data["projects"]),
                ),
                (
                    "🎨",
                    "Designs",
                    len(data["designs"]),
                ),
                (
                    "✦",
                    "AI Generations",
                    len(st.session_state.messages),
                ),
                (
                    "👥",
                    "Designers",
                    data["designers"],
                ),
            ]

            metric_columns = st.columns(4)

            for index, (
                icon,
                label,
                value,
            ) in enumerate(stats):

                with metric_columns[index]:

                    st.metric(
                        label=f"{icon} {label}",
                        value=value,
                    )

        # ====================================================
        # RIGHT — FASHION AVATAR
        # ====================================================

        with right:

            if AVATAR_PATH.exists():

                st.image(
                    AVATAR_PATH,
                    use_container_width=True,
                )

            else:

                st.markdown(
                    "## 👗"
                )

                st.caption(
                    "StyleSense Fashion Avatar"
                )


# ============================================================
# QUICK ACTIONS
# ============================================================

def render_quick_actions():

    st.divider()

    st.subheader(
        "Quick Actions"
    )

    st.caption(
        "Jump directly into your creative workflow."
    )

    actions = [
        (
            "✨",
            "Create Design",
            "AI-powered fashion design generation",
            "Design Studio",
        ),
        (
            "📁",
            "New Project",
            "Start a new fashion collection",
            "Projects",
        ),
        (
            "📸",
            "Outfit Analyzer",
            "Analyze an outfit with AI",
            "Outfit Analyzer",
        ),
        (
            "🧵",
            "Fabric Advisor",
            "Find the perfect fabric",
            "Fabric Advisor",
        ),
        (
            "📈",
            "Explore Trends",
            "Discover what's trending",
            "AI Fashion Trends",
        ),
    ]

    columns = st.columns(5)

    for index, (
        icon,
        title,
        description,
        target,
    ) in enumerate(actions):

        with columns[index]:

            st.markdown(
                f"### {icon}"
            )

            st.write(
                f"**{title}**"
            )

            st.caption(
                description
            )

            if st.button(
                f"Open {title}",
                key=f"dashboard_action_{index}",
                use_container_width=True,
            ):

                navigate_to(
                    target
                )


# ============================================================
# AI TEAM
# ============================================================

def render_ai_team():

    st.divider()

    st.subheader(
        "Your AI Team"
    )

    st.caption(
        "Five specialized AI agents working with you."
    )

    agents = [
        (
            "👩‍🎨",
            "Creative Director",
            "Creative Intelligence",
        ),
        (
            "👗",
            "Fashion Designer",
            "Design Intelligence",
        ),
        (
            "🧵",
            "Fabric Advisor",
            "Material Intelligence",
        ),
        (
            "📊",
            "Trend Analyst",
            "Trend Intelligence",
        ),
        (
            "🤖",
            "AI Co-Founder",
            "Business Intelligence",
        ),
    ]

    columns = st.columns(5)

    for index, (
        icon,
        name,
        role,
    ) in enumerate(agents):

        with columns[index]:

            st.markdown(
                f"### {icon}"
            )

            st.write(
                f"**{name}**"
            )

            st.caption(
                role
            )

            if st.button(
                "Open",
                key=f"dashboard_agent_{index}",
                use_container_width=True,
            ):

                navigate_to(
                    "AI Team"
                )

    st.write("")

    center = st.columns(
        [1, 2, 1]
    )[1]

    with center:

        if st.button(
            "View All Agents →",
            key="view_all_agents",
            use_container_width=True,
        ):

            navigate_to(
                "AI Team"
            )


# ============================================================
# RECENT PROJECTS
# ============================================================

def render_recent_projects(projects):

    st.divider()

    st.subheader(
        "Recent Projects"
    )

    st.caption(
        "Continue working on your latest fashion projects."
    )

    if not projects:

        st.info(
            "📁 You don't have any projects yet. "
            "Create your first fashion project from Projects."
        )

        return

    recent_projects = projects[:3]

    columns = st.columns(
        len(recent_projects)
    )

    for index, project in enumerate(
        recent_projects
    ):

        with columns[index]:

            try:

                project_id = project[0]
                project_title = project[2]
                project_description = project[3]
                project_category = project[4]
                project_cover = project[5]
                project_created = project[6]

            except (
                IndexError,
                TypeError,
            ):

                continue

            with st.container(border=True):

                if project_cover:

                    st.image(
                        project_cover,
                        use_container_width=True,
                    )

                else:

                    st.markdown(
                        "### 📁"
                    )

                st.write(
                    f"**{project_title}**"
                )

                if project_description:

                    st.caption(
                        project_description
                    )

                else:

                    st.caption(
                        "No description provided."
                    )

                if project_category:

                    st.caption(
                        f"Category: {project_category}"
                    )

                if project_created:

                    st.caption(
                        f"Created: {project_created}"
                    )

                if st.button(
                    "Open Project",
                    key=f"dashboard_recent_project_{project_id}",
                    use_container_width=True,
                ):

                    st.session_state.current_project = {
                        "id": project_id,
                        "title": project_title,
                        "description": project_description,
                        "category": project_category,
                        "created_at": project_created,
                    }

                    st.session_state.open_workspace = True

                    st.session_state.main_navigation = (
                        "Workspace"
                    )

                    st.rerun()

    st.write("")

    center = st.columns(
        [1, 2, 1]
    )[1]

    with center:

        if st.button(
            "View All Projects →",
            key="view_all_projects",
            use_container_width=True,
        ):

            navigate_to(
                "Projects"
            )


# ============================================================
# RECENT DESIGNS
# ============================================================

def render_recent_designs(designs):

    st.divider()

    st.subheader(
        "Recent Designs"
    )

    st.caption(
        "Your latest AI-generated fashion work."
    )

    if not designs:

        st.info(
            "✨ Your Design Library is waiting.\n\n"
            "Create your first AI fashion concept "
            "and it will appear here automatically."
        )

        return

    recent_designs = designs[:4]

    columns = st.columns(4)

    for index, design in enumerate(
        recent_designs
    ):

        with columns[index]:

            image = design.get(
                "image"
            )

            title = clean_design_title(
                design.get(
                    "design",
                    "AI Fashion Design",
                )
            )

            mode = design.get(
                "mode",
                "AI Design",
            )

            created_at = design.get(
                "created_at",
                "",
            )

            if image:

                st.image(
                    image,
                    use_container_width=True,
                )

            else:

                st.info(
                    "🎨 AI Design"
                )

            st.write(
                f"**{title}**"
            )

            st.caption(
                f"✦ {mode}"
            )

            if created_at:

                st.caption(
                    f"📅 {created_at}"
                )

            if st.button(
                "Open Design",
                key=f"recent_design_{index}",
                use_container_width=True,
            ):

                navigate_to(
                    "Design Library"
                )

    st.write("")

    center = st.columns(
        [1, 2, 1]
    )[1]

    with center:

        if st.button(
            "View All Designs →",
            key="view_all_designs",
            use_container_width=True,
        ):

            navigate_to(
                "Design Library"
            )


# ============================================================
# INTELLIGENCE CENTER
# ============================================================

def render_intelligence_center():

    st.divider()

    st.subheader(
        "Intelligence Center"
    )

    st.caption(
        "AI-powered intelligence for your next move."
    )

    columns = st.columns(3)

    # ========================================================
    # AI INSIGHTS
    # ========================================================

    with columns[0]:

        st.markdown(
            "### ✦ AI Insights"
        )

        st.caption(
            "Powered by StyleSense AI"
        )

        st.info(
            "Your AI workspace is ready. "
            "Generate designs, explore trends and "
            "build your next collection."
        )

        if st.button(
            "Explore Insights →",
            key="dashboard_ai_insights",
            use_container_width=True,
        ):

            navigate_to(
                "Ask StyleSense"
            )

    # ========================================================
    # TRENDING NOW
    # ========================================================

    with columns[1]:

        st.markdown(
            "### 📈 Trending Now"
        )

        st.caption(
            "Fashion intelligence"
        )

        trends = [
            ("Sheer Elegance", "↑ 82%"),
            ("Relaxed Luxury", "↑ 74%"),
            ("Bold Tailoring", "↑ 69%"),
            ("African Prints", "↑ 61%"),
        ]

        for name, value in trends:

            trend_left, trend_right = st.columns(
                [3, 1]
            )

            with trend_left:

                st.write(
                    f"**{name}**"
                )

            with trend_right:

                st.write(
                    value
                )

        if st.button(
            "View Trends →",
            key="dashboard_trending",
            use_container_width=True,
        ):

            navigate_to(
                "AI Fashion Trends"
            )

    # ========================================================
    # TASKS
    # ========================================================

    with columns[2]:

        st.markdown(
            "### ✓ My Tasks"
        )

        st.caption(
            "Your current workspace tasks"
        )

        completed = 0

        tasks = st.session_state.dashboard_tasks

        for index, task in enumerate(tasks):

            checked = st.checkbox(
                task["title"],
                value=task["completed"],
                key=f"dashboard_task_{index}",
            )

            task["completed"] = checked

            if checked:
                completed += 1

            st.caption(
                f'{task["context"]} • '
                f'{task["priority"]}'
            )

        st.write(
            f"**{completed}/{len(tasks)} completed**"
        )

        if st.button(
            "Open Tasks →",
            key="open_tasks",
            use_container_width=True,
        ):

            navigate_to(
                "My Tasks"
            )


# ============================================================
# CONTINUE YOUR JOURNEY
# ============================================================

def render_continue_section():

    st.divider()

    st.subheader(
        "Continue Your Journey"
    )

    st.caption(
        "Pick up where you left off."
    )

    items = [
        (
            "🎨",
            "Design Studio",
            "Create new designs with AI",
            "Design Studio",
        ),
        (
            "📸",
            "Outfit Analyzer",
            "Analyze an outfit for insights",
            "Outfit Analyzer",
        ),
        (
            "🧵",
            "Fabric Advisor",
            "Find the perfect fabric match",
            "Fabric Advisor",
        ),
        (
            "🤖",
            "AI Chat",
            "Chat with your AI fashion team",
            "Ask StyleSense",
        ),
    ]

    columns = st.columns(4)

    for index, (
        icon,
        title,
        description,
        target,
    ) in enumerate(items):

        with columns[index]:

            st.markdown(
                f"### {icon}"
            )

            st.write(
                f"**{title}**"
            )

            st.caption(
                description
            )

            if st.button(
                "Continue →",
                key=f"continue_{index}",
                use_container_width=True,
            ):

                navigate_to(
                    target
                )


# ============================================================
# MAIN DASHBOARD RENDERER
# ============================================================

def render_dashboard():

    # --------------------------------------------------------
    # Dashboard setup
    # --------------------------------------------------------

    render_dashboard_styles()

    initialize_dashboard_state()

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    data = load_dashboard_data()

    # --------------------------------------------------------
    # Dashboard content ONLY
    #
    # app.py owns:
    #
    # ☰ StyleSense
    # 🔔 Profile Appearance
    # Home | Product | Create | AI Teams
    # Sidebar
    #
    # --------------------------------------------------------

    render_welcome_section(
        data
    )

    render_quick_actions()

    render_ai_team()

    render_recent_projects(
        data["projects"]
    )

    render_recent_designs(
        data["designs"]
    )

    render_intelligence_center()

    render_continue_section()