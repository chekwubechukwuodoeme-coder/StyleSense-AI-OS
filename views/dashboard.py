import base64
import re

import streamlit as st

from database.dashboard import (
    count_projects,
    count_designers,
    count_missions,
)

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AVATAR_PATH = PROJECT_ROOT / "assets" / "fashion_avatar.png"

from database.database import get_all_designs
from database.projects import get_projects

# ============================================================
# HELPERS
# ============================================================

def clean_design_title(value):
    """Create a short plain-text title from an AI design description."""

    text = str(value or "AI Fashion Design")

    # Remove markdown headings
    text = re.sub(r"^#{1,6}\s*", "", text)

    # Remove markdown emphasis
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)

    # Remove excessive whitespace
    text = " ".join(text.split())

    if not text:
        text = "AI Fashion Design"

    return text[:90]


def navigate_to(target):
    """Navigate to another StyleSense section."""

    st.session_state.main_navigation = target
    st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def render_dashboard():

    st.markdown(
        """
        <style>

        /* ========================================================
        STYLESENSE — 4 COLOR DASHBOARD BACKGROUND
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
                    rgba(0, 168, 107, 0.30),
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
            min-height: 100vh;
        }


        /* ========================================================
        STREAMLIT CONTENT — KEEP BACKGROUND TRANSPARENT
        ======================================================== */

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            background: transparent !important;
        }


        /* ========================================================
        MAIN HEADER
        ======================================================== */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background:
                linear-gradient(
                    135deg,
                    rgba(0, 107, 69, 0.96),
                    rgba(38, 50, 56, 0.94),
                    rgba(245, 166, 35, 0.88)
                ) !important;

            border: 1px solid rgba(57, 255, 20, 0.25) !important;

            border-radius: 28px !important;

            box-shadow:
                0 20px 60px rgba(0, 0, 0, 0.35),
                0 0 40px rgba(57, 255, 20, 0.08) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            background: transparent !important;
        }


        /* ========================================================
        AI PROMPT
        ======================================================== */

        div[data-baseweb="input"] {
            background: rgba(255, 255, 255, 0.96) !important;
            border: 2px solid rgba(57, 255, 20, 0.35) !important;
            border-radius: 14px !important;
        }

        div[data-baseweb="input"] input {
            color: #263238 !important;
        }

        div[data-baseweb="input"] input::placeholder {
            color: #687277 !important;
        }


        /* ========================================================
        BUTTONS
        ======================================================== */

        div[data-testid="stButton"] button {
            background: rgba(0, 107, 69, 0.75) !important;
            color: white !important;
            border: 1px solid rgba(57, 255, 20, 0.35) !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
        }

        div[data-testid="stButton"] button:hover {
            background: #006B45 !important;
            border-color: #39FF14 !important;
            color: #FFFFFF !important;
        }


        /* ========================================================
        WORKSPACE METRICS
        ======================================================== */

        div[data-testid="stMetric"] {
            background: rgba(38, 50, 56, 0.65) !important;
            border: 1px solid rgba(57, 255, 20, 0.18) !important;
            border-radius: 16px !important;
            padding: 14px !important;
        }

        div[data-testid="stMetricValue"] {
            color: #F5A623 !important;
        }

        div[data-testid="stMetricLabel"] {
            color: rgba(255, 255, 255, 0.82) !important;
        }


        /* ========================================================
        DIVIDERS
        ======================================================== */

        hr {
            border-color: rgba(57, 255, 20, 0.18) !important;
        }


        /* ========================================================
        HEADINGS
        ======================================================== */

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4 {
            color: #FFFFFF !important;
        }


        /* ========================================================
        CAPTIONS
        ======================================================== */

        .stApp .stCaption {
            color: rgba(255, 255, 255, 0.70) !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # SESSION STATE
    # ========================================================

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

    # ========================================================
    # LOAD DATABASE DATA
    # ========================================================

    user_id = st.session_state.get("user_id")

    try:
        
        all_projects = get_projects(
            user_id=user_id
        ) or []
        projects = len(all_projects)
    except Exception:
        all_projects = []
        projects = 0

    try:
        designers = count_designers()
    except Exception:
        designers = 0

    try:
        saved_designs = get_all_designs() or []
    except Exception:
        saved_designs = []

    design_count = len(saved_designs)

    # ========================================================
    # TOP BAR
    # ========================================================

    _, top_right = st.columns(
        [5, 1]
    )

    with top_right:

        notification_col, profile_col, theme_col = st.columns(
            [1, 1, 1]
        )

        # ----------------------------------------------------
        # NOTIFICATIONS
        # ----------------------------------------------------

        with notification_col:

            if st.button(
                "🔔",
                key="dashboard_notifications",
                help="Notifications",
            ):

                navigate_to("Notifications")

        # ----------------------------------------------------
        # PROFILE
        # ----------------------------------------------------

        with profile_col:

            if st.button(
                "👤",
                key="dashboard_profile",
                help="Profile",
            ):

                navigate_to("Settings")

        # ----------------------------------------------------
        # APPEARANCE / DARK MODE
        # ----------------------------------------------------

        with theme_col:

            if st.button(
                "🌙",
                key="dashboard_theme",
                help="Appearance",
            ):

                navigate_to("Settings")

    # ========================================================
    # MAIN DASHBOARD HEADER + AI PROMPT + WORKSPACE
    # ========================================================

    user_name = st.session_state.get("user_name") or "there"

    name_parts = str(user_name).strip().split()
    first_name = name_parts[0] if name_parts else "there"


    # ========================================================
    # ONE RECTANGULAR HEADER CONTAINER
    # ========================================================

    with st.container(border=True):

        # ----------------------------------------------------
        # LEFT CONTENT + RIGHT FASHION AVATAR
        # ----------------------------------------------------

        header_left, header_right = st.columns(
            [3.2, 1.8],
            vertical_alignment="center"
        )

        # ====================================================
        # LEFT SIDE
        # ====================================================

        with header_left:

            # ------------------------------------------------
            # PERSONALIZED GREETING
            # ------------------------------------------------

            st.markdown(
                f"### HELLO, {first_name.upper()}!"
            )

            st.markdown(
                "## What are you creating today?"
            )

            st.caption(
                "Your intelligent fashion workspace for design, "
                "creativity, research and business."
            )

            # ------------------------------------------------
            # AI PROMPT
            # ------------------------------------------------

            st.markdown(
                """
                <style>
                div[data-testid="stButton"] button {
                    white-space: nowrap !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            prompt = st.text_input(
                "StyleSense AI",
                placeholder=(
                    "Ask StyleSense anything about your fashion idea..."
                ),
                label_visibility="collapsed",
                key="dashboard_prompt",
            )

            prompt_col, button_col = st.columns(
                [5, 1],
                vertical_alignment="center"
            )

            with prompt_col:

                st.caption(
                    "✨ Concepts • Designs • Fabrics • Styling • "
                    "Trends • Business"
                )

            with button_col:

                generate = st.button(
                    "⚡ Ask AI",
                    use_container_width=True,
                    key="dashboard_generate",
                )

            # ------------------------------------------------
            # AI PROMPT ACTION
            # ------------------------------------------------

            if generate:

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

                    navigate_to("Design Studio")

            # =================================================
            # YOUR WORKSPACE
            # =================================================


            stats = [
                ("📁", "Projects", projects),
                ("🎨", "Designs", design_count),
                (
                    "✦",
                    "AI Generations",
                    len(st.session_state.messages),
                ),
                ("👥", "Designers", designers),
            ]

            workspace_columns = st.columns(4)

            for i, (icon, label, number) in enumerate(stats):

                with workspace_columns[i]:

                    st.metric(
                        label=f"{icon} {label}",
                        value=number,
                    )

        # ====================================================
        # RIGHT SIDE — FASHION AVATAR
        # ====================================================

        with header_right:

            avatar_path = (
                Path(__file__).resolve().parent.parent
                / "assets"
                / "fashion_avatar.png"
            )

            if avatar_path.exists():

                st.markdown(
                    f"""
                    <div style="
                        width: 100%;
                        height: 560px;
                        overflow: hidden;
                        border-radius: 16px;
                    ">
                        <img
                            src="data:image/png;base64,{base64.b64encode(
                                avatar_path.read_bytes()
                            ).decode()}"
                            style="
                                width: 100%;
                                height: 100%;
                                object-fit: fill;
                                display: block;
                            "
                        >
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:

                st.warning("Fashion avatar image not found.")
    # ========================================================
    # QUICK ACTIONS
    # ========================================================

    st.divider()

    st.subheader("Quick Actions")

    st.caption(
        "Jump directly into your creative workflow"
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

    for i, (
        icon,
        title,
        description,
        target,
    ) in enumerate(actions):

        with columns[i]:

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
                key=f"dashboard_action_{i}",
                use_container_width=True,
            ):

                navigate_to(target)

    # ========================================================
    # AI TEAM
    # ========================================================

    st.divider()

    st.subheader("Your AI Team")

    st.caption(
        "Five specialized AI agents working with you"
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

    for i, (
        icon,
        name,
        role,
    ) in enumerate(agents):

        with columns[i]:

            # Circular-style avatar using Streamlit container
            st.markdown(
                f"""
                <div style="
                    width:70px;
                    height:70px;
                    border-radius:50%;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:#111827;
                    border:2px solid #374151;
                    font-size:28px;
                    margin:auto;
                ">
                    {icon}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write(
                f"**{name}**"
            )

            st.caption(
                role
            )

            if st.button(
                "Open",
                key=f"agent_{i}",
                use_container_width=True,
            ):

                navigate_to("AI Team")

    st.write("")

    agent_col = st.columns([1, 2, 1])[1]

    with agent_col:

        if st.button(
            "View All Agents →",
            use_container_width=True,
            key="view_all_agents",
        ):

            navigate_to("AI Team")

    # ========================================================
    # RECENT PROJECTS
    # ========================================================

    st.divider()

    st.subheader("Recent Projects")

    st.caption(
        "Continue working on your latest fashion projects"
    )

    try:
       recent_projects = all_projects
    except Exception as e:
        recent_projects = []
        st.error(f"Unable to load projects: {e}")


    if not recent_projects:

        st.info(
            "📁 You don't have any projects yet. "
            "Create your first fashion project from Projects."
        )

    else:

        # Show the 3 most recent real projects
        recent_projects = recent_projects[:3]

        columns = st.columns(len(recent_projects))

        for i, project in enumerate(recent_projects):

            project_id = project[0]
            project_user_id = project[1]
            project_title = project[2]
            project_description = project[3]
            project_category = project[4]
            project_cover = project[5]
            project_created = project[6]

            with columns[i]:

                # Project card
                with st.container(border=True):

                    if project_cover:
                        st.image(
                            project_cover,
                            use_container_width=True
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

                        st.session_state.main_navigation = "Workspace"

                        st.rerun()


        st.write("")

        project_col = st.columns([1, 2, 1])[1]

        with project_col:

            if st.button(
                "View All Projects →",
                use_container_width=True,
                key="view_all_projects",
            ):

                navigate_to("Projects")

    # ========================================================
    # RECENT DESIGNS
    # ========================================================

    st.divider()

    st.subheader("Recent Designs")

    st.caption(
        "Your latest AI-generated fashion work"
    )

    if not saved_designs:

        st.info(
            "✨ Your Design Library is waiting.\n\n"
            "Create your first AI fashion concept "
            "and it will appear here automatically."
        )

    else:

        recent_designs = saved_designs[:4]

        columns = st.columns(4)

        for i, design in enumerate(recent_designs):

            with columns[i]:

                image = design.get("image")

                description = design.get(
                    "design",
                    "AI Fashion Design",
                )

                mode = design.get(
                    "mode",
                    "AI Design",
                )

                created_at = design.get(
                    "created_at",
                    "",
                )

                description = clean_design_title(
                    description
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
                    f"**{description}**"
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
                    key=f"recent_design_{i}",
                    use_container_width=True,
                ):

                    navigate_to("Design Library")

    st.write("")

    design_col = st.columns([1, 2, 1])[1]

    with design_col:

        if st.button(
            "View All Designs →",
            use_container_width=True,
            key="view_all_designs",
        ):

            navigate_to("Design Library")

    # ========================================================
    # INTELLIGENCE CENTER
    # ========================================================

    st.divider()

    st.subheader("Intelligence Center")

    st.caption(
        "AI-powered intelligence for your next move"
    )

    intelligence_columns = st.columns(3)

    # ========================================================
    # AI INSIGHTS
    # ========================================================

    with intelligence_columns[0]:

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
            use_container_width=True,
            key="dashboard_ai_insights",
        ):

            navigate_to("Fashion Assistant")

    # ========================================================
    # TRENDING NOW
    # ========================================================

    with intelligence_columns[1]:

        st.markdown(
            "### 📈 Trending Now"
        )

        st.caption(
            "Fashion intelligence"
        )

        trends = [
            (
                "Sheer Elegance",
                "↑ 82%",
            ),
            (
                "Relaxed Luxury",
                "↑ 74%",
            ),
            (
                "Bold Tailoring",
                "↑ 69%",
            ),
            (
                "African Prints",
                "↑ 61%",
            ),
        ]

        for name, value in trends:

            trend_col_1, trend_col_2 = st.columns(
                [3, 1]
            )

            with trend_col_1:

                st.write(
                    f"**{name}**"
                )

            with trend_col_2:

                st.write(
                    value
                )

        if st.button(
            "View Trends →",
            use_container_width=True,
            key="dashboard_trending",
        ):

            navigate_to("AI Fashion Trends")

    # ========================================================
    # MY TASKS
    # ========================================================

    with intelligence_columns[2]:

        st.markdown(
            "### ✓ My Tasks"
        )

        st.caption(
            "Your current workspace tasks"
        )

        completed = 0

        for i, task in enumerate(
            st.session_state.dashboard_tasks
        ):

            checked = st.checkbox(
                task["title"],
                value=task["completed"],
                key=f"dashboard_task_{i}",
            )

            task["completed"] = checked

            if checked:

                completed += 1

            st.caption(
                f'{task["context"]} • '
                f'{task["priority"]}'
            )

        st.write(
            f"**{completed}/"
            f"{len(st.session_state.dashboard_tasks)} "
            f"completed**"
        )

        if st.button(
            "Open Tasks →",
            use_container_width=True,
            key="open_tasks",
        ):

            navigate_to("Projects")

    # ========================================================
    # CONTINUE YOUR JOURNEY
    # ========================================================

    st.divider()

    st.subheader("Continue Your Journey")

    st.caption(
        "Pick up where you left off"
    )

    continue_items = [
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
            "Fashion Assistant",
        ),
    ]

    columns = st.columns(4)

    for i, (
        icon,
        title,
        description,
        target,
    ) in enumerate(continue_items):

        with columns[i]:

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
                key=f"continue_{i}",
                use_container_width=True,
            ):

                navigate_to(target)

    # ========================================================
    # BOTTOM NAVIGATION
    # ========================================================

    st.divider()

    st.caption(
        "StyleSense Workspace"
    )

    nav_columns = st.columns(5)

    bottom_navigation = [
        (
            "🏠",
            "Home",
            "Dashboard",
        ),
        (
            "📦",
            "Product",
            "Marketplace",
        ),
        (
            "＋",
            "Create",
            "Design Studio",
        ),
        (
            "🤖",
            "AI Teams",
            "AI Team",
        ),
        (
            "⋯",
            "More",
            "Settings",
        ),
    ]

    for i, (
        icon,
        label,
        target,
    ) in enumerate(bottom_navigation):

        with nav_columns[i]:

            if st.button(
                f"{icon} {label}",
                key=f"bottom_nav_{i}",
                use_container_width=True,
            ):

                navigate_to(target)