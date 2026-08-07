import streamlit as st

from ai.designer import fashion_chat
from image_generator import generate_image


def render_logo_generator():

    st.header("🎨 AI Brand Identity Studio")

    st.caption(
        "Create luxury logos and complete brand identities powered by AI."
    )

    col1, col2 = st.columns(2)

    with col1:

        brand = st.text_input(
            "🏷 Brand Name"
        )

        description = st.text_area(
            "📝 Brand Description",
            placeholder="""
    Example:

    Luxury African fashion brand
    for high-end weddings,
    corporate executives
    and celebrities.
    """
        )

        industry = st.selectbox(

            "Industry",

            [
                "Luxury Fashion",
                "Streetwear",
                "Corporate Fashion",
                "Beauty",
                "Shoes",
                "Jewelry",
                "Perfume",
                "Accessories"
            ]
        )

        style = st.selectbox(

            "Logo Style",

            [
                "Luxury",
                "Modern",
                "Minimalist",
                "Streetwear",
                "Vintage",
                "Futuristic",
                "Elegant"
            ]
        )

    with col2:

        colors = st.multiselect(

            "Preferred Colors",

            [

                "Black",

                "White",

                "Gold",

                "Silver",

                "Wine",

                "Royal Blue",

                "Emerald Green",

                "Brown",

                "Cream",

                "Purple",

                "Red"

            ]

        )

        icon = st.text_input(

            "Preferred Symbol",

            placeholder="Lion, Crown, Eagle, Needle..."

        )

        typography = st.selectbox(

            "Typography",

            [

                "Luxury Serif",

                "Modern Sans Serif",

                "Bold",

                "Minimal",

                "Elegant Script"

            ]

        )

        vibe = st.selectbox(

            "Brand Personality",

            [

                "Premium",

                "Luxury",

                "Creative",

                "Bold",

                "Elegant",

                "Royal",

                "Minimal"

            ]

        )

    if st.button("🚀 Generate Brand Identity", use_container_width=True):

        if not brand.strip():

            st.warning("Please enter your brand name.")

            st.stop()

        prompt = f"""
    You are one of the world's best luxury brand identity designers.

    Create a complete premium fashion brand identity.

    Brand Name:
    {brand}

    Brand Description:
    {description}

    Industry:
    {industry}

    Logo Style:
    {style}

    Preferred Colors:
    {", ".join(colors)}

    Preferred Symbol:
    {icon}

    Typography:
    {typography}

    Brand Personality:
    {vibe}

    Generate a professional logo with:

    - Clean vector style
    - White background
    - Minimal luxury look
    - Premium branding
    - Fashion industry quality
    - High resolution
    """

        with st.spinner("Designing your luxury brand..."):

            try:

                image = generate_image(prompt)

                st.success("🎉 Brand Identity Generated!")

                st.image(
                    image,
                    caption=f"{brand} Brand Logo",
                    use_container_width=True
                )

                st.download_button(
                    "📥 Download Logo",
                    data=image,
                    file_name=f"{brand.replace(' ','_')}_Logo.png",
                    mime="image/png",
                    use_container_width=True
                )

                st.divider()

                st.subheader("📖 AI Brand Identity Report")

                brand_prompt = f"""
                You are a world-class luxury branding expert.

                Create a complete brand identity for this fashion brand.

                Brand Name:
                {brand}

                Brand Description:
                {description}

                Industry:
                {industry}

                Brand Style:
                {style}

                Brand Personality:
                {vibe}

                Preferred Colors:
                {", ".join(colors)}

                Preferred Symbol:
                {icon}

                Typography:
                {typography}

                Return your answer in beautiful Markdown.

                Include:

                # 🏷 Brand Story

                # 🎯 Mission

                # 🌍 Vision

                # 👥 Target Audience

                # 🎨 Color Palette Meaning

                # 🔤 Typography Recommendation

                # 💬 Brand Voice

                # ✨ Brand Slogan (Give 5)

                # 📦 Packaging Concept

                # 📱 Social Media Theme

                # 💼 Luxury Positioning

                # 🚀 Future Expansion Ideas
                """

                with st.spinner("Building complete brand identity..."):

                    report = fashion_chat(brand_prompt)

                st.markdown(report)

                st.download_button(
                    "📄 Download Brand Report",
                    data=report,
                    file_name=f"{brand.replace(' ','_')}_Brand_Report.md",
                    mime="text/markdown",
                    use_container_width=True
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button("🔄 Generate Another", use_container_width=True):
                        st.rerun()

                with col2:

                    st.button(
                        "💾 Save Brand",
                        use_container_width=True
                    )

                st.divider()

                st.subheader("🎁 AI Brand Assets")

                asset = st.selectbox(

                    "Generate Brand Asset",

                    [

                        "Business Card",

                        "Shopping Bag",

                        "Clothing Label",

                        "Luxury Box",

                        "Store Sign",

                        "Instagram Profile",

                        "Billboard",

                        "Fashion Hang Tag"

                    ]

                )

                if st.button(
                    "✨ Generate Asset",
                    use_container_width=True
                ):

                    asset_prompt = f"""
                Create a professional mockup.

                Brand Name:
                {brand}

                Brand Description:
                {description}

                Logo Style:
                {style}

                Brand Personality:
                {vibe}

                Asset:
                {asset}

                Luxury fashion branding.

                Premium realistic mockup.

                White background.

                Ultra realistic.

                4K.

                Professional lighting.
                """

                    with st.spinner("Generating Brand Asset..."):

                        asset_image = generate_image(asset_prompt)

                    st.image(
                        asset_image,
                        caption=asset,
                        use_container_width=True
                    )

                    st.download_button(

                        "📥 Download Asset",

                        data=asset_image,

                        file_name=f"{brand}_{asset.replace(' ','_')}.png",

                        mime="image/png",

                        use_container_width=True

                    )

            except Exception as e:

                st.error(f"Logo generation failed:\n{e}")