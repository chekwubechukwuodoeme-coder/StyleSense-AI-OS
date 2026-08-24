import streamlit as st


# ============================================================
# STYLESENSE HELP & SUPPORT
# ============================================================

def render_help_support():

    st.title("❓ Help & Support")

    st.caption(
        "Find answers, learn how StyleSense works, "
        "and get help with your fashion workspace."
    )

    st.divider()

    # ========================================================
    # SEARCH
    # ========================================================

    st.markdown("### 🔍 How can we help?")

    search = st.text_input(
        "Search Help",
        placeholder="Try: How do I create a design?",
        key="help_search",
    )

    search_query = search.strip().lower()

    # ========================================================
    # HELP DATABASE
    # ========================================================

    help_articles = [

        {
            "category": "Getting Started",
            "icon": "🚀",
            "title": "Getting Started with StyleSense",
            "keywords": [
                "getting started",
                "start",
                "begin",
                "new",
                "dashboard",
            ],
            "content": """
Start from the Dashboard to access your StyleSense workspace.

You can create projects, generate AI fashion designs,
manage clients, record measurements, create tech packs,
track inventory and manage your fashion business.

Recommended first steps:

1. Complete your Fashion Professional profile.
2. Create your first project.
3. Add your client measurements.
4. Create a design using AI Design Studio.
5. Save your designs to Design Library.
6. Use Production Manager and Tech Packs when you are
   ready to move from design to production.
""",
        },

        {
            "category": "AI Tools",
            "icon": "🤖",
            "title": "Using StyleSense AI",
            "keywords": [
                "ai",
                "artificial intelligence",
                "assistant",
                "ask stylesense",
                "ai tools",
            ],
            "content": """
StyleSense AI is designed to assist with fashion design,
business decisions and production workflows.

You can use:

• Ask StyleSense for fashion questions and guidance.
• AI Co-Founder for strategic business assistance.
• AI Design Studio for generating fashion concepts.
• Outfit Analyzer for analyzing outfits.
• Fabric Advisor for fabric recommendations.
• Color Matcher for color coordination.
• AI Fashion Trends for trend research.
• Fashion Inspiration for discovering ideas.
""",
        },

        {
            "category": "Design Studio",
            "icon": "🎨",
            "title": "Creating an AI Fashion Design",
            "keywords": [
                "design",
                "design studio",
                "generate",
                "fashion design",
                "image",
                "prompt",
            ],
            "content": """
Open Design Studio from the sidebar.

You can enter a fashion concept and describe:

• Garment type
• Silhouette
• Fabric
• Colors
• Occasion
• Fashion style
• Cultural inspiration
• Embroidery
• Model presentation

The AI will turn your concept into a visual fashion design.

You can save successful designs to your Design Library
for future use.
""",
        },

        {
            "category": "Measurements",
            "icon": "📏",
            "title": "Managing Client Measurements",
            "keywords": [
                "measurement",
                "measurements",
                "client",
                "body",
                "arm",
                "armhole",
            ],
            "content": """
Open Measurements from the Production section.

Create a measurement profile for each client.

You can record:

• Height
• Bust / Chest
• Shoulder
• Sleeve
• Neck
• Long Arm
• Short Arm
• Armhole
• Garment Length
• Head
• Waist
• Hip
• Trouser Length
• Inseam
• Thigh
• Knee
• Calf
• Ankle / Hem Opening

You can also attach client photos, fabric photos
and production notes.

Saved profiles can be opened and edited whenever the
client's measurements change.
""",
        },

        {
            "category": "Production",
            "icon": "🏭",
            "title": "Managing Fashion Production",
            "keywords": [
                "production",
                "production manager",
                "inventory",
                "tech pack",
                "manufacturing",
            ],
            "content": """
The Production section contains:

🏭 Production Manager
📦 Inventory
📏 Measurements
📋 Tech Packs

Use Production Manager to organize garments and
production workflows.

Use Inventory to track fabrics, materials and stock.

Use Measurements to maintain client measurement profiles.

Use Tech Packs to document technical garment information
for production.
""",
        },

        {
            "category": "Business",
            "icon": "💼",
            "title": "Managing Your Fashion Business",
            "keywords": [
                "business",
                "client",
                "clients",
                "orders",
                "expenses",
                "pricing",
                "revenue",
                "profit",
            ],
            "content": """
The Business section helps you manage the commercial
side of your fashion operation.

It includes:

👥 Clients
🛒 Orders
💸 Expenses
💰 Pricing
📊 Revenue & Profit

Use Clients to maintain customer records.

Use Orders to track customer orders.

Use Expenses to record business spending.

Use Pricing to calculate garment prices.

Use Revenue & Profit to understand your financial
performance.
""",
        },

        {
            "category": "Design Library",
            "icon": "📚",
            "title": "Managing Your Design Library",
            "keywords": [
                "library",
                "design library",
                "saved design",
                "save",
                "download",
            ],
            "content": """
Design Library is your central collection of saved
fashion designs.

Use it to:

• Browse your designs.
• Search designs.
• Organize design ideas.
• Review previous AI generations.
• Reuse concepts for new projects.

Save important AI-generated designs so they remain
available in your workspace.
""",
        },

        {
            "category": "Account",
            "icon": "👤",
            "title": "Account & Profile",
            "keywords": [
                "account",
                "profile",
                "settings",
                "profession",
                "avatar",
                "logout",
            ],
            "content": """
Your account information can be managed through Settings.

You can manage your:

• Profile
• Fashion profession
• Appearance
• AI preferences
• Fashion preferences
• Notifications
• Projects and data
• Privacy and security
• Regional settings
• Integrations

Use Logout from the sidebar when you want to leave
your StyleSense session.
""",
        },

        {
            "category": "Troubleshooting",
            "icon": "🛠️",
            "title": "Troubleshooting StyleSense",
            "keywords": [
                "error",
                "problem",
                "not working",
                "bug",
                "troubleshoot",
                "loading",
            ],
            "content": """
If something is not working correctly:

1. Refresh the StyleSense application.
2. Check that you are logged in.
3. Check your internet connection if an AI feature
   requires an external AI service.
4. Try the operation again.
5. If the problem continues, record the exact error
   message.

When contacting support, provide:

• What you were trying to do.
• The page where the problem occurred.
• The exact error message.
• What happened before the error appeared.
""",
        },
    ]

    # ========================================================
    # SEARCH RESULTS
    # ========================================================

    if search_query:

        results = []

        for article in help_articles:

            searchable_text = (
                article["title"]
                + " "
                + article["category"]
                + " "
                + " ".join(article["keywords"])
                + " "
                + article["content"]
            ).lower()

            if search_query in searchable_text:

                results.append(article)

        st.divider()

        st.markdown(
            f"### 🔎 Search Results"
        )

        if results:

            st.caption(
                f"{len(results)} result(s) found."
            )

            for article in results:

                with st.expander(
                    f"{article['icon']} {article['title']}"
                ):

                    st.caption(
                        article["category"]
                    )

                    st.markdown(
                        article["content"]
                    )

        else:

            st.warning(
                f'No help articles found for "{search}".'
            )

            st.info(
                "Try searching for terms such as "
                "\"design\", \"measurements\", \"clients\", "
                "\"AI\", \"inventory\" or \"settings\"."
            )

        st.divider()

    # ========================================================
    # HELP CATEGORIES
    # ========================================================

    st.markdown("### 📚 Help Center")

    st.caption(
        "Choose a category to find useful information."
    )

    categories = [

        (
            "🚀",
            "Getting Started",
            "Learn the basics of StyleSense."
        ),

        (
            "🤖",
            "AI Tools",
            "Learn how to use the StyleSense AI tools."
        ),

        (
            "🎨",
            "Design Studio",
            "Create and manage AI fashion designs."
        ),

        (
            "📏",
            "Measurements",
            "Manage detailed client measurements."
        ),

        (
            "🏭",
            "Production",
            "Manage production, inventory and tech packs."
        ),

        (
            "💼",
            "Business",
            "Manage clients, orders and finances."
        ),

        (
            "👤",
            "Account & Settings",
            "Manage your profile and preferences."
        ),

        (
            "🛠️",
            "Troubleshooting",
            "Fix common StyleSense problems."
        ),
    ]

    cols = st.columns(4)

    for index, (
        icon,
        title,
        description,
    ) in enumerate(categories):

        with cols[index % 4]:

            with st.container(border=True):

                st.markdown(
                    f"## {icon}"
                )

                st.markdown(
                    f"**{title}**"
                )

                st.caption(
                    description
                )

                if st.button(
                    "View Help",
                    key=f"help_category_{index}",
                    use_container_width=True,
                ):

                    st.session_state[
                        "help_selected_category"
                    ] = title

                    st.rerun()

    # ========================================================
    # SELECTED CATEGORY
    # ========================================================

    selected_category = st.session_state.get(
        "help_selected_category"
    )

    if selected_category:

        st.divider()

        st.markdown(
            f"### 📖 {selected_category}"
        )

        selected_articles = [

            article
            for article in help_articles
            if article["category"] == selected_category
        ]

        if selected_articles:

            for article in selected_articles:

                with st.expander(
                    f"{article['icon']} {article['title']}",
                    expanded=True,
                ):

                    st.markdown(
                        article["content"]
                    )

        else:

            st.info(
                "More help content for this category "
                "will be added soon."
            )

        if st.button(
            "Clear Category",
            key="clear_help_category",
        ):

            st.session_state[
                "help_selected_category"
            ] = None

            st.rerun()

    # ========================================================
    # FREQUENTLY ASKED QUESTIONS
    # ========================================================

    st.divider()

    st.markdown("### ❓ Frequently Asked Questions")

    faq = [

        (
            "How do I create a fashion design?",
            """
Go to **Design Studio**, describe the garment you want,
configure your design options and generate the design.
"""
        ),

        (
            "Where can I find my saved designs?",
            """
Open **Design Library** from the sidebar. Your saved
fashion concepts and generated designs are organized there.
"""
        ),

        (
            "Can I edit a client's measurements?",
            """
Yes. Open **Measurements**, find the client's profile,
open the profile and use the edit controls to update
the measurements.
"""
        ),

        (
            "Where do I manage my clients?",
            """
Open **Clients** under the Business section of the
sidebar.
"""
        ),

        (
            "Where can I track production?",
            """
Use **Production Manager** under the Production section.
You can also use Inventory, Measurements and Tech Packs
as part of the production workflow.
"""
        ),

        (
            "Where can I see my business performance?",
            """
Open **Revenue & Profit** under the Business section.
"""
        ),

        (
            "Where can I change my profile?",
            """
Open **Settings** or use **Edit Profile** in the sidebar.
"""
        ),

        (
            "What should I do if I encounter an error?",
            """
First refresh the application and try again. If the
problem continues, record the exact error message and
use the support section below.
"""
        ),
    ]

    for question, answer in faq:

        with st.expander(
            f"❓ {question}"
        ):

            st.markdown(
                answer
            )

    # ========================================================
    # QUICK START
    # ========================================================

    st.divider()

    st.markdown("### 🚀 Quick Start")

    quick_start = [

        (
            "1",
            "Complete your profile",
            "Set up your fashion professional information."
        ),

        (
            "2",
            "Create a project",
            "Organize your fashion work inside Projects."
        ),

        (
            "3",
            "Create a design",
            "Use AI Design Studio to develop fashion concepts."
        ),

        (
            "4",
            "Add measurements",
            "Create client measurement profiles."
        ),

        (
            "5",
            "Plan production",
            "Use Production Manager, Inventory and Tech Packs."
        ),

        (
            "6",
            "Manage your business",
            "Track clients, orders, expenses, pricing and profit."
        ),
    ]

    cols = st.columns(3)

    for index, (
        number,
        title,
        description,
    ) in enumerate(quick_start):

        with cols[index % 3]:

            with st.container(border=True):

                st.markdown(
                    f"### {number}. {title}"
                )

                st.caption(
                    description
                )

    # ========================================================
    # CONTACT SUPPORT
    # ========================================================

    st.divider()

    st.markdown("### 💬 Contact Support")

    st.caption(
        "Need help with something that is not covered "
        "in the Help Center?"
    )

    support_col1, support_col2 = st.columns(2)

    with support_col1:

        support_subject = st.text_input(
            "Subject",
            placeholder="What do you need help with?",
            key="support_subject",
        )

        support_category = st.selectbox(
            "Support Category",
            [
                "General Question",
                "AI Tools",
                "Design Studio",
                "Measurements",
                "Production",
                "Business",
                "Account & Settings",
                "Bug Report",
                "Feature Request",
            ],
            key="support_category",
        )

    with support_col2:

        support_message = st.text_area(
            "Describe the issue",
            placeholder=(
                "Tell us what happened and what you "
                "were trying to do..."
            ),
            height=140,
            key="support_message",
        )

    if st.button(
        "📨 Submit Support Request",
        type="primary",
        use_container_width=True,
        key="submit_support_request",
    ):

        if not support_subject.strip():

            st.error(
                "Please enter a support subject."
            )

        elif not support_message.strip():

            st.error(
                "Please describe your issue."
            )

        else:

            st.success(
                "✅ Your support request has been recorded."
            )

            st.info(
                "Support request handling can be connected "
                "to your email, database or support system next."
            )

    # ========================================================
    # FEEDBACK
    # ========================================================

    st.divider()

    st.markdown("### 💡 Help Us Improve StyleSense")

    feedback_type = st.selectbox(
        "Feedback Type",
        [
            "General Feedback",
            "Feature Request",
            "Bug Report",
            "UI / UX Feedback",
            "AI Feedback",
        ],
        key="help_feedback_type",
    )

    feedback = st.text_area(
        "Your Feedback",
        placeholder=(
            "Tell us what you think or what you would "
            "like StyleSense to improve..."
        ),
        key="help_feedback",
    )

    if st.button(
        "💡 Send Feedback",
        use_container_width=True,
        key="send_help_feedback",
    ):

        if not feedback.strip():

            st.warning(
                "Please enter some feedback first."
            )

        else:

            st.success(
                "Thank you for helping improve StyleSense! 💚"
            )