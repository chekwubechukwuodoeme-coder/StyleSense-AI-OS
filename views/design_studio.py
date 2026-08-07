import streamlit as st

from ai import generate_design
from image_generator import generate_image
from pdf_generator import create_pdf


def render_design_studio():

    st.title("✨ AI Design Studio Pro")

    st.caption(
        "Create luxury fashion collections powered by AI."
    )

    st.divider()

    if "saved_designs" not in st.session_state:
        st.session_state.saved_designs = []

    if "current_design" not in st.session_state:
        st.session_state.current_design = ""

    tab1, tab2, tab3 = st.tabs(
        [
            "🎨 Design",
            "⚙ Advanced",
            "📂 Saved"
        ]
    )

    with tab1:

        left, right = st.columns(2)

        with left:

            st.subheader("Designer")

            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Unisex"]
            )

            age = st.slider(
                "Age",
                5,
                80,
                25
            )

            height = st.slider(
                "Height (cm)",
                120,
                220,
                170
            )

            body_shape = st.selectbox(
                "Body Shape",
                [
                    "Slim",
                    "Athletic",
                    "Average",
                    "Curvy",
                    "Plus Size"
                ]
            )

            skin_tone = st.selectbox(
                "Skin Tone",
                [
                    "Fair",
                    "Light Brown",
                    "Brown",
                    "Dark Brown",
                    "Deep Black"
                ]
            )

            st.divider()

            st.subheader("Fashion")

            category = st.selectbox(
                "Category",
                [
                    "Luxury",
                    "Streetwear",
                    "Corporate",
                    "Native Wear",
                    "Wedding",
                    "Evening Wear",
                    "Casual",
                    "Sport Wear"
                ]
            )

            fabric = st.selectbox(
                "Fabric",
                [
                    "Ankara",
                    "Aso Oke",
                    "Lace",
                    "Silk",
                    "Velvet",
                    "Cashmere",
                    "Senator",
                    "Cotton",
                    "Linen",
                    "Leather",
                    "Denim"
                ]
            )

            colors = st.multiselect(
                "Preferred Colors",
                [
                    "Black",
                    "White",
                    "Gold",
                    "Silver",
                    "Royal Blue",
                    "Wine",
                    "Emerald Green",
                    "Purple",
                    "Cream",
                    "Brown",
                    "Red"
                ]
            )

        with right:

            st.subheader("Occasion")

            occasion = st.selectbox(
                "Event",
                [
                    "Wedding",
                    "Traditional Marriage",
                    "Birthday",
                    "Dinner",
                    "Church",
                    "Office",
                    "Graduation",
                    "Date",
                    "Vacation",
                    "Award Ceremony",
                    "Photoshoot"
                ]
            )

            budget = st.select_slider(
                "Budget",
                options=[
                    "₦20,000",
                    "₦50,000",
                    "₦100,000",
                    "₦200,000",
                    "₦500,000",
                    "Unlimited"
                ]
            )

            complexity = st.selectbox(
                "Complexity",
                [
                    "Simple",
                    "Moderate",
                    "Luxury"
                ]
            )

            theme = st.selectbox(
                "Theme",
                [
                    "African Royalty",
                    "Modern Luxury",
                    "Celebrity Fashion",
                    "Traditional Heritage",
                    "Minimalist",
                    "Futuristic"
                ]
            )

            country = st.selectbox(
                "Country",
                [
                    "Nigeria",
                    "Ghana",
                    "Kenya",
                    "South Africa",
                    "United Kingdom",
                    "United States",
                    "France",
                    "Italy"
                ]
            )

            climate = st.selectbox(
                "Climate",
                [
                    "Hot",
                    "Cold",
                    "Rainy",
                    "Dry"
                ]
            )

            embroidery = st.checkbox(
                "Include Embroidery",
                value=True
            )

            accessories = st.checkbox(
                "Recommend Accessories",
                value=True
            )

    with tab2:

        st.subheader("AI Settings")

        ai_creativity = st.slider(
            "AI Creativity",
            1,
            10,
            8
        )

        st.info(
            """
Higher creativity gives more artistic and
experimental fashion concepts.
"""
        )

        st.success(
            "OpenAI Image Generation Enabled"
        )

    with tab3:

        st.subheader("Saved Designs")

        if not st.session_state.saved_designs:

            st.info(
                "No saved designs yet."
            )

        else:

            for design in st.session_state.saved_designs:

                with st.expander("Fashion Design"):

                    st.write(design["design"])

                    if design["image"]:

                        st.image(
                            design["image"],
                            use_container_width=True
                        )

    st.divider()

    if st.button(
        "🚀 Generate Luxury Fashion Design",
        use_container_width=True
    ):

        with st.spinner("🧠 AI is designing your fashion concept..."):

            try:

                result = generate_design(
                    gender,
                    age,
                    height,
                    body_shape,
                    skin_tone,
                    category,
                    fabric,
                    occasion,
                    budget,
                    colors,
                    complexity,
                    theme,
                    embroidery,
                    accessories,
                    ai_creativity,
                    country,
                    climate
                )

                st.session_state.current_design = result

                st.success("✅ Design generated successfully!")

                st.divider()

                st.subheader("📝 AI Fashion Concept")

                st.write(result)

                st.divider()

                image_prompt = f"""
        Professional luxury fashion illustration.

        Gender: {gender}

        Age: {age}

        Height: {height}cm

        Body Shape: {body_shape}

        Skin Tone: {skin_tone}

        Category: {category}

        Fabric: {fabric}

        Occasion: {occasion}

        Theme: {theme}

        Style Complexity: {complexity}

        Country: {country}

        Climate: {climate}

        Preferred Colors:
        {", ".join(colors) if colors else "Designer Choice"}

        Luxury fashion sketch.

        Runway quality.

        Elegant pose.

        Full body.

        White background.

        Highly detailed.

        Professional fashion illustration.

        Fashion concept art.

        4K.

        """

                st.subheader("🎨 AI Fashion Sketch")

                with st.spinner("Generating fashion illustration..."):

                    try:

                        image = generate_image(image_prompt)

                        st.image(
                            image,
                            use_container_width=True
                        )

                    except Exception as e:

                        image = None

                        st.warning(
                            f"Image generation failed.\n\n{e}"
                        )

                st.divider()

                st.subheader("👠 Accessories")

                if accessories:

                    st.success(
                        """
        • Luxury Wrist Watch

        • Premium Leather Bag

        • Sunglasses

        • Gold Jewelry

        • Matching Belt

        • Designer Shoes
        """
                    )

                st.divider()

                st.subheader("🧵 Production Recommendation")

                st.info(
                    f"""
        Recommended Fabric:
        {fabric}

        Recommended Market:
        Luxury Fashion

        Estimated Completion:
        5-10 Days

        Quality Level:
        Premium
        """
                )

                st.divider()

                st.subheader("💰 Suggested Selling Price")

                prices = {
                    "Simple": "₦50,000 - ₦120,000",
                    "Moderate": "₦120,000 - ₦300,000",
                    "Luxury": "₦300,000 - ₦1,000,000+"
                }

                st.success(
                    prices.get(complexity)
                )

                st.divider()

                st.subheader("📣 Marketing Caption")

                caption = f"""
        Introducing our latest {category.lower()} collection.

        Designed for {occasion.lower()}.

        Crafted from premium {fabric.lower()}.

        Luxury.

        Elegance.

        Confidence.

        Powered by StyleSense AI OS.
        """

                st.code(caption)

                pdf = create_pdf(result)

                with open(pdf, "rb") as file:

                    st.download_button(
                        "📄 Download Design Report",
                        file,
                        file_name="StyleSense_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                st.session_state.saved_designs.append(
                    {
                        "design": result,
                        "image": image
                    }
                )

                st.divider()

                st.subheader("✂ Tailoring Instructions")

                tailoring = f"""
        Pattern Type:
        Custom {category}

        Fit:
        {body_shape}

        Fabric:
        {fabric}

        Complexity:
        {complexity}

        Recommended Seam:
        Double stitched

        Recommended Lining:
        Premium lining

        Recommended Thread:
        Matching premium polyester thread

        Estimated Tailoring Time:
        5 - 10 working days
        """

                st.text_area(
                    "Tailor Notes",
                    tailoring,
                    height=220
                )

                st.divider()

                st.subheader("💰 Production Cost Estimate")

                costs = {
                    "Simple": {
                        "Fabric": 25000,
                        "Labour": 15000,
                        "Accessories": 10000
                    },
                    "Moderate": {
                        "Fabric": 50000,
                        "Labour": 30000,
                        "Accessories": 25000
                    },
                    "Luxury": {
                        "Fabric": 120000,
                        "Labour": 90000,
                        "Accessories": 60000
                    }
                }

                estimate = costs[complexity]

                total = (
                    estimate["Fabric"] +
                    estimate["Labour"] +
                    estimate["Accessories"]
                )

                profit = int(total * 0.5)

                selling_price = total + profit

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Production Cost",
                    f"₦{total:,}"
                )

                c2.metric(
                    "Estimated Profit",
                    f"₦{profit:,}"
                )

                c3.metric(
                    "Suggested Price",
                    f"₦{selling_price:,}"
                )

                st.divider()

                st.subheader("📦 Packaging Recommendation")

                st.success(
                    f"""
        • Premium Gift Box

        • Brand Sticker

        • Thank You Card

        • Care Instruction Card

        • Luxury Shopping Bag

        Suitable for a {complexity.lower()} collection.
        """
                )

                st.divider()

                st.subheader("📸 Photoshoot Ideas")

                st.info(
                    f"""
        Location:
        Luxury hotel or studio.

        Theme:
        {theme}

        Lighting:
        Soft luxury lighting.

        Recommended Pose:
        Editorial fashion pose.

        Background:
        Minimal white or premium marble.
        """
                )

                st.divider()

                st.subheader("📱 Instagram Advertisement")

                advert = f"""
        ✨ NEW COLLECTION ✨

        Introducing our exclusive {category} collection.

        ✔ Premium {fabric}

        ✔ {theme}

        ✔ Designed for {occasion}

        Available now.

        #Fashion
        #Luxury
        #StyleSense
        #Designer
        """

                st.code(advert)

                st.divider()

                st.subheader("🏷 AI Brand Name Suggestions")

                names = [
                    "Royal Threads",
                    "Elite Couture",
                    "Imperial Stitch",
                    "Luxora Fashion",
                    "Heritage Wear",
                    "StyleSense Signature"
                ]

                cols = st.columns(2)

                for i, name in enumerate(names):

                    with cols[i % 2]:

                        st.success(name)

                st.divider()

                st.subheader("📈 AI Fashion Insights")

                insight1, insight2 = st.columns(2)

                with insight1:

                    st.info(f"""
                ### 🎯 Target Audience

                • Age: {age}

                • Gender: {gender}

                • Region: {country}

                • Fashion Category:
                {category}

                • Income:
                Middle to High Class

                • Fashion Taste:
                Premium Luxury
                """)

                with insight2:

                    st.success(f"""
                ### 🔥 Market Opportunity

                Demand:
                ★★★★★

                Competition:
                ★★★☆☆

                Luxury Appeal:
                ★★★★★

                Commercial Potential:
                ★★★★★

                Brand Value:
                Excellent
                """)

                st.divider()

                st.subheader("🎨 Recommended Color Palette")

                palette = st.columns(6)

                recommended = colors

                if len(recommended) == 0:

                    recommended = [
                        "Black",
                        "Gold",
                        "White",
                        "Wine",
                        "Royal Blue",
                        "Cream"
                    ]

                for colour in recommended[:6]:

                    palette[recommended.index(colour)].success(colour)

                st.divider()

                st.subheader("✅ Fashion Production Checklist")

                st.checkbox(
                    "Design Completed",
                    value=True,
                    disabled=True
                )

                st.checkbox(
                    "Fabric Selected",
                    value=True,
                    disabled=True
                )

                st.checkbox(
                    "Accessories Recommended",
                    value=accessories,
                    disabled=True
                )

                st.checkbox(
                    "AI Sketch Generated",
                    value=image is not None,
                    disabled=True
                )

                st.checkbox(
                    "PDF Generated",
                    value=True,
                    disabled=True
                )

                st.divider()

                st.subheader("📂 Export")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.download_button(
                        "📄 Export Report",
                        data=open(pdf, "rb"),
                        file_name="Fashion_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                with col2:

                    st.button(
                        "💾 Save To Library",
                        use_container_width=True
                    )

                with col3:

                    st.button(
                        "🚀 Send To Workspace",
                        use_container_width=True
                    )

                    st.divider()

                    st.subheader("🤖 AI Recommendations")

                    recommendations = [

                        "Increase embroidery for premium appeal.",

                        "Use luxury photography for marketing.",

                        "Offer limited edition releases.",

                        "Target Instagram and TikTok first.",

                        "Bundle matching accessories."

                    ]

                    for recommendation in recommendations:

                        st.success(recommendation)

            except Exception as e:

                st.error(e)

    