import streamlit as st

from ai.ceo import ceo_agent
from ai.designer import designer_agent
from ai.marketing import marketing_agent
from ai.finance import finance_agent
from ai.production import production_agent
from ai.research import research_agent
from ai.stylist import stylist_agent
from ai.business import business_agent


def agent_card(
    icon,
    title,
    description,
    function,
    key
):

    with st.container(border=True):

        st.subheader(f"{icon} {title}")

        st.caption(description)

        st.success("🟢 Online")

        prompt = st.text_area(
            "Ask your AI",
            key=f"{key}_prompt",
            height=120
        )

        if st.button(
            f"Ask {title}",
            key=f"{key}_button",
            use_container_width=True
        ):

            if prompt.strip() == "":

                st.warning(
                    "Please enter a prompt."
                )

            else:

                with st.spinner(
                    f"{title} is thinking..."
                ):

                    response = function(prompt)

                    st.markdown("### Response")

                    st.write(response)


def render_ai_team():

    st.title("👔 AI Executive Board")

    st.caption(
        "Your intelligent executive team for fashion business."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "AI Agents",
        8
    )

    col2.metric(
        "Online",
        8
    )

    col3.metric(
        "Projects",
        len(
            st.session_state.get(
                "saved_designs",
                []
            )
        )
    )

    col4.metric(
        "Status",
        "Operational"
    )

    st.divider()

    st.info(
        """
Every executive specializes in a different part of your fashion business.

Ask each AI independently for the best results.
"""
    )

    tab1, tab2, tab3, tab4 = st.tabs(

        [
            "Executives",
            "Board Meeting",
            "Dashboard",
            "🚨 War Room"
        ]
    )

    with tab1:

        c1, c2 = st.columns(2)

        with c1:

            agent_card(
                "👑",
                "CEO",
                "Business strategy and growth.",
                ceo_agent,
                "ceo"
            )

            agent_card(
                "🎨",
                "Fashion Designer",
                "Luxury fashion creation.",
                designer_agent,
                "designer"
            )

            agent_card(
                "📈",
                "Marketing Director",
                "Branding and promotion.",
                marketing_agent,
                "marketing"
            )

            agent_card(
                "💰",
                "Finance Manager",
                "Pricing and profitability.",
                finance_agent,
                "finance"
            )

        with c2:

            agent_card(
                "🧵",
                "Production Manager",
                "Manufacturing and production.",
                production_agent,
                "production"
            )

            agent_card(
                "🔬",
                "Research Analyst",
                "Fashion trends and market research.",
                research_agent,
                "research"
            )

            agent_card(
                "👗",
                "Personal Stylist",
                "Outfit recommendations.",
                stylist_agent,
                "stylist"
            )

            agent_card(
                "💼",
                "Business Consultant",
                "Business planning and scaling.",
                business_agent,
                "business"
            )

    with tab2:    

        st.subheader("🚨 AI Executive Board Meeting")

        st.info(
            """
        Present your business idea once.

        Every executive AI will analyse it
        from their own perspective.
        """
        )

        meeting_prompt = st.text_area(
            "Business Proposal",
            placeholder="""
        Example:

        I have ₦500,000.

        I want to launch a luxury
        Ankara fashion brand
        targeting young professionals
        in Lagos.
        """,
            height=180
        )

        if st.button(
            "🚀 Start Executive Meeting",
            use_container_width=True
        ):

            if meeting_prompt.strip() == "":

                st.warning(
                    "Enter your proposal first."
                )

            else:

                executives = [

                    (
                        "👑 CEO",
                        ceo_agent
                    ),

                    (
                        "🎨 Fashion Designer",
                        designer_agent
                    ),

                    (
                        "📈 Marketing Director",
                        marketing_agent
                    ),

                    (
                        "💰 Finance Manager",
                        finance_agent
                    ),

                    (
                        "🧵 Production Manager",
                        production_agent
                    ),

                    (
                        "🔬 Research Analyst",
                        research_agent
                    ),

                    (
                        "👗 Personal Stylist",
                        stylist_agent
                    ),

                    (
                        "💼 Business Consultant",
                        business_agent
                    )

                ]

                progress = st.progress(0)

                for index, executive in enumerate(executives):

                    title = executive[0]

                    function = executive[1]

                    with st.spinner(f"{title} is analysing..."):

                        response = function(
                            meeting_prompt
                        )

                    with st.expander(title, expanded=True):

                        st.write(response)

                    progress.progress(
                        (index + 1) / len(executives)
                    )

                st.success(
                    "Executive meeting completed."
                )

    with tab3:     

        st.subheader("🏢 Executive Intelligence Dashboard")

        st.info(
            """
        The Executive Board continuously monitors your
        fashion business and provides intelligent recommendations.
            """
        )

        st.divider()

        # ===========================
        # COMPANY HEALTH
        # ===========================

        st.subheader("📊 Company Health")

        business = 95
        marketing = 90
        finance = 93
        production = 88
        branding = 97

        overall = int(
            (
                business +
                marketing +
                finance +
                production +
                branding
            ) / 5
        )

        st.metric(
            "Overall Company Score",
            f"{overall}%"
        )

        st.progress(overall / 100)

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Business",
                f"{business}%"
            )

            st.progress(business / 100)

            st.metric(
                "Marketing",
                f"{marketing}%"
            )

            st.progress(marketing / 100)

            st.metric(
                "Finance",
                f"{finance}%"
            )

            st.progress(finance / 100)

        with c2:

            st.metric(
                "Production",
                f"{production}%"
            )

            st.progress(production / 100)

            st.metric(
                "Branding",
                f"{branding}%"
            )

            st.progress(branding / 100)

        st.divider()

        # ===========================
        # DAILY MISSION
        # ===========================

        st.subheader("🎯 Today's Mission")

        missions = [

            "Generate two luxury fashion concepts.",

            "Research current fashion trends.",

            "Create a marketing campaign.",

            "Review production costs.",

            "Contact suppliers.",

            "Prepare Instagram content."

        ]

        completed = 0

        for mission in missions:

            done = st.checkbox(mission)

            if done:

                completed += 1

        progress = completed / len(missions)

        st.progress(progress)

        st.success(
            f"{completed} of {len(missions)} tasks completed."
        )

        st.divider()

        # ===========================
        # AI NOTIFICATIONS
        # ===========================

        st.subheader("🔔 Executive Notifications")

        notifications = [

            (
                "👑 CEO",
                "Your current pricing can be increased by 15%."
            ),

            (
                "📈 Marketing",
                "Luxury fashion performs better on Instagram Reels."
            ),

            (
                "💰 Finance",
                "Reduce production costs by buying fabric wholesale."
            ),

            (
                "🔬 Research",
                "Streetwear demand has increased this month."
            ),

            (
                "👗 Stylist",
                "Neutral colors are trending globally."
            )

        ]

        for sender, message in notifications:

            with st.container(border=True):

                st.markdown(f"### {sender}")

                st.write(message)

        st.divider()

        # ===========================
        # AI ACTIVITY
        # ===========================

        st.subheader("📜 Executive Timeline")

        timeline = [

            "09:00 — CEO reviewed business strategy",

            "09:20 — Designer created luxury sketch",

            "09:40 — Marketing generated campaign",

            "10:10 — Finance calculated pricing",

            "10:35 — Production estimated manufacturing",

            "11:00 — Stylist suggested accessories",

            "11:20 — Research updated trend report"

        ]

        for activity in timeline:

            st.write("•", activity)

        st.divider()

        # ===========================
        # AI STATS
        # ===========================

        st.subheader("📈 Executive Statistics")

        a, b, c, d = st.columns(4)

        with a:
            st.metric(
                "Designs",
                len(st.session_state.get("saved_designs", []))
            )

        with b:
            st.metric(
                "AI Requests",
                127
            )

        with c:
            st.metric(
                "Executives",
                8
            )

        with d:
            st.metric(
                "Projects",
                14
            )

        st.divider()

        st.success(
            """
        🚀 StyleSense Executive Board is fully operational.

        Your AI executives are ready to help you build,
        manage and scale your fashion business.
        """
        )             

    with tab4:

        st.title("🚨 AI War Room")

        st.caption(
            "Your entire executive board working together."
        )

        business_goal = st.text_area(
            "Mission",
            placeholder="""
        Example

        Launch a luxury fashion brand
        in Lagos with ₦1,000,000.
        """
        )

        if st.button(
            "🚀 Launch Strategy",
            use_container_width=True
        ):

            if business_goal == "":

                st.warning(
                    "Enter your mission."
                )

            else:

                executives = [

                    ("👑 CEO", ceo_agent),

                    ("🎨 Designer", designer_agent),

                    ("📈 Marketing", marketing_agent),

                    ("💰 Finance", finance_agent),

                    ("🧵 Production", production_agent),

                    ("🔬 Research", research_agent),

                    ("👗 Stylist", stylist_agent),

                    ("💼 Business", business_agent)

                ]

                progress = st.progress(0)

                for index, executive in enumerate(executives):

                    title = executive[0]

                    agent = executive[1]

                    with st.spinner(
                        f"{title} working..."
                    ):

                        answer = agent(
                            business_goal
                        )

                    st.subheader(title)

                    st.write(answer)

                    progress.progress(
                        (index + 1) /
                        len(executives)
                    )

                st.success(
                    "Mission completed."
                )    