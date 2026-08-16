import io
import urllib.request

import streamlit as st

from datetime import datetime
from ai import generate_design
from image_generator import (
    generate_image,
    generate_image_from_reference
)
from pdf_generator import create_pdf


def render_design_studio():

    st.title("✨ AI Design Studio Pro")

    st.caption(
        "Create luxury fashion collections powered by AI."
    )

    st.divider()

    # ============================================================
    # SESSION STATE
    # ============================================================

    if "saved_designs" not in st.session_state:
        st.session_state.saved_designs = []

    if "current_design" not in st.session_state:
        st.session_state.current_design = ""

    if "advanced_prompt" not in st.session_state:
        st.session_state.advanced_prompt = ""

    if "advanced_enhanced_prompt" not in st.session_state:
        st.session_state.advanced_enhanced_prompt = ""

    if "advanced_image" not in st.session_state:
        st.session_state.advanced_image = None

    if "reference_image_result" not in st.session_state:
        st.session_state.reference_image_result = None

    # ============================================================
    # REFERENCE IMAGE FROM FASHION INSPIRATION
    # ============================================================

    studio_reference_url = st.session_state.get(
        "studio_reference_image_url"
    )

    studio_reference_title = st.session_state.get(
        "studio_reference_title",
        "Fashion Inspiration"
    )

    studio_reference_photographer = st.session_state.get(
        "studio_reference_photographer",
        "Pexels"
    )

    # ============================================================
    # TABS
    # ============================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "🎨 Design",
            "⚙ Advanced",
            "📂 Design Library"
        ]
    )

    # ============================================================
    # DESIGN TAB
    # ============================================================

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

    # ============================================================
    # ADVANCED TAB
    # ============================================================

    with tab2:

        st.subheader("⚙ Advanced AI Design")

        st.caption(
            "Create fashion concepts using natural language, "
            "advanced controls and visual references."
        )

        # ========================================================
        # AI SETTINGS
        # ========================================================

        st.divider()

        st.subheader("🧠 AI Settings")

        ai_creativity = st.slider(
            "AI Creativity",
            1,
            10,
            8,
            key="advanced_ai_creativity"
        )

        st.info(
            """
Higher creativity produces more artistic,
experimental and unconventional fashion concepts.
"""
        )

        st.success(
            "OpenAI Image Generation Enabled"
        )

        # ========================================================
        # PROMPT-TO-DESIGN
        # ========================================================

        st.divider()

        st.subheader("🚀 Prompt-to-Design")

        st.write(
            "Describe the fashion design you want in your own words. "
            "You do not need to complete the Design tab."
        )

        prompt_examples = [
            "Create a luxurious emerald green evening gown with an asymmetric neckline, sculptural sleeves, subtle gold embroidery and a fitted silhouette. Make it elegant and sophisticated.",
            "Design a modern Nigerian agbada for a young entrepreneur using deep wine velvet, gold embroidery and a clean luxury silhouette.",
            "Create a futuristic streetwear outfit inspired by African architecture, using black technical fabric with silver details and an oversized silhouette.",
            "Design an elegant Aso Oke bridal outfit combining traditional Nigerian heritage with modern haute couture."
        ]

        example_choice = st.selectbox(
            "💡 Example Prompts",
            [
                "Choose an example...",
                *prompt_examples
            ],
            key="advanced_example_prompt"
        )

        if example_choice != "Choose an example...":

            if st.button(
                "Use Example Prompt",
                key="use_example_prompt"
            ):

                st.session_state.advanced_prompt = example_choice

                st.rerun()

        prompt = st.text_area(
            "Describe Your Fashion Design",
            value=st.session_state.advanced_prompt,
            height=180,
            placeholder=(
                "Example: Create a luxury floor-length emerald green "
                "evening gown for a sophisticated young woman attending "
                "a high-end wedding..."
            ),
            key="advanced_prompt_input"
        )

        st.caption(
            "Describe the garment, fabric, colour, silhouette, "
            "occasion, cultural inspiration, mood, details and target customer."
        )

        # ========================================================
        # OPTIONAL DESIGN CONTROLS
        # ========================================================

        st.divider()

        st.subheader("🎯 Optional Design Controls")

        st.caption(
            "These controls are optional. Your prompt remains the main instruction."
        )

        advanced_col1, advanced_col2 = st.columns(2)

        with advanced_col1:

            advanced_style = st.selectbox(
                "Design Style",
                [
                    "AI Choice",
                    "Luxury",
                    "Haute Couture",
                    "African Luxury",
                    "Streetwear",
                    "Minimalist",
                    "Futuristic",
                    "Traditional",
                    "Editorial",
                    "Celebrity"
                ],
                key="advanced_style"
            )

            advanced_fabric = st.selectbox(
                "Preferred Fabric",
                [
                    "AI Choice",
                    "Ankara",
                    "Aso Oke",
                    "Lace",
                    "Silk",
                    "Velvet",
                    "Cashmere",
                    "Cotton",
                    "Linen",
                    "Leather",
                    "Denim"
                ],
                key="advanced_fabric"
            )

            advanced_colour = st.selectbox(
                "Preferred Colour",
                [
                    "AI Choice",
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
                ],
                key="advanced_colour"
            )

        with advanced_col2:

            advanced_occasion = st.selectbox(
                "Occasion",
                [
                    "AI Choice",
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
                    "Photoshoot",
                    "Runway"
                ],
                key="advanced_occasion"
            )

            advanced_market = st.selectbox(
                "Target Market",
                [
                    "AI Choice",
                    "Mass Market",
                    "Premium",
                    "Luxury",
                    "Haute Couture",
                    "Celebrity"
                ],
                key="advanced_market"
            )

            advanced_culture = st.selectbox(
                "Cultural Inspiration",
                [
                    "AI Choice",
                    "Nigerian",
                    "West African",
                    "East African",
                    "South African",
                    "European",
                    "Asian",
                    "Global"
                ],
                key="advanced_culture"
            )

        advanced_embroidery = st.checkbox(
            "✨ Include Embroidery / Embellishment",
            value=False,
            key="advanced_embroidery"
        )

        advanced_full_body = st.checkbox(
            "👤 Full Body Fashion Presentation",
            value=True,
            key="advanced_full_body"
        )

        # ========================================================
        # AI PROMPT ENHANCEMENT
        # ========================================================

        st.divider()

        st.subheader("✨ AI Prompt Enhancement")

        st.caption(
            "Turn a simple idea into a detailed professional fashion prompt."
        )

        if st.button(
            "✨ Enhance Prompt",
            use_container_width=True,
            key="enhance_advanced_prompt"
        ):

            if not prompt.strip():

                st.warning(
                    "Please describe your fashion idea first."
                )

            else:

                enhanced_prompt = f"""
Transform the following fashion idea into a detailed professional
fashion design generation prompt.

Original idea:
{prompt}

Optional design direction:

Design Style:
{advanced_style}

Fabric:
{advanced_fabric}

Colour:
{advanced_colour}

Occasion:
{advanced_occasion}

Target Market:
{advanced_market}

Cultural Inspiration:
{advanced_culture}

Embroidery:
{"Yes" if advanced_embroidery else "Designer choice"}

The final concept should clearly describe:

- Garment type
- Silhouette
- Construction
- Fabric
- Colour
- Texture
- Neckline
- Sleeves
- Length
- Embellishment
- Cultural details where appropriate
- Overall aesthetic
- Luxury and fashion quality
- Professional fashion presentation

Do not change the user's core idea.
Improve it while preserving the original creative direction.
"""

                st.session_state.advanced_enhanced_prompt = (
                    enhanced_prompt
                )

                st.success(
                    "✨ Prompt enhanced successfully!"
                )

        if st.session_state.advanced_enhanced_prompt:

            st.text_area(
                "📝 Enhanced Fashion Prompt",
                value=st.session_state.advanced_enhanced_prompt,
                height=260,
                key="display_enhanced_prompt"
            )

        # ========================================================
        # GENERATE PROMPT DESIGN
        # ========================================================

        st.divider()

        if st.button(
            "🎨 Generate Design",
            use_container_width=True,
            type="primary",
            key="generate_advanced_design"
        ):

            if not prompt.strip():

                st.warning(
                    "Please describe the fashion design you want to create."
                )

            else:

                final_prompt = (
                    st.session_state.advanced_enhanced_prompt
                    if st.session_state.advanced_enhanced_prompt
                    else prompt
                )

                image_prompt = f"""
Create a professional luxury fashion design based on this creative direction:

{final_prompt}

Additional Style Direction:

Design Style:
{advanced_style}

Preferred Fabric:
{advanced_fabric}

Preferred Colour:
{advanced_colour}

Occasion:
{advanced_occasion}

Target Market:
{advanced_market}

Cultural Inspiration:
{advanced_culture}

Embroidery / Embellishment:
{"Include sophisticated embroidery or embellishment." if advanced_embroidery else "Use embellishment only if appropriate."}

Presentation:
{"Full body fashion presentation." if advanced_full_body else "Professional fashion presentation."}

Requirements:

- Professional fashion design
- High-end fashion illustration
- Strong garment construction
- Accurate silhouette
- Sophisticated proportions
- Detailed fabric texture
- Realistic garment details
- Elegant styling
- Professional fashion pose
- Clean composition
- Premium fashion editorial quality
- Highly detailed
- 4K quality

The garment must remain the primary focus.
"""

                with st.spinner(
                    "🧠 StyleSense AI is creating your fashion design..."
                ):

                    try:

                        image = generate_image(
                            image_prompt
                        )

                        st.session_state.advanced_image = image

                        st.session_state.current_design = prompt

                        # Save generated design to library data
                        st.session_state.saved_designs.append(
                            {
                                "design": prompt,
                                "image": image,
                                "mode": "Advanced Prompt-to-Design",

                                "style": advanced_style,
                                "fabric": advanced_fabric,
                                "colour": advanced_colour,
                                "occasion": advanced_occasion,
                                "market": advanced_market,
                                "culture": advanced_culture,

                                "created_at": datetime.now().strftime(
                                    "%Y-%m-%d %H:%M"
                                )
                            }
                        )

                        st.success(
                            "✅ Design generated successfully!"
                        )

                        st.image(
                            image,
                            use_container_width=True
                        )

                        st.info(
                            "💾 Your design is now available in 📂 Design Library."
                        )

                    except Exception as e:

                        st.error(
                            f"Advanced design generation failed.\n\n{e}"
                        )

        # ============================================================
        # REFERENCE IMAGE → DESIGN
        # ============================================================

        st.divider()

        st.subheader(
            "🖼️ Reference Image → Design"
        )

        st.caption(
            "Transform a fashion inspiration, sketch, garment photo "
            "or your own reference image into a new AI fashion design."
        )


        # ============================================================
        # PEXELS IMAGE FROM FASHION INSPIRATION
        # ============================================================

        studio_reference_url = (
            st.session_state.get(
                "studio_reference_image_url"
            )
        )

        if studio_reference_url:

            st.success(
                "✨ Fashion Inspiration loaded from Fashion Inspiration."
            )

            st.image(
                studio_reference_url,
                caption=st.session_state.get(
                    "studio_reference_title",
                    "Fashion Inspiration"
                ),
                use_container_width=True
            )

            st.caption(
                "📸 Original inspiration by "
                + st.session_state.get(
                    "studio_reference_photographer",
                    "Pexels"
                )
            )

            if st.button(
                "✕ Remove Inspiration",
                key="remove_pexels_studio_reference"
            ):

                st.session_state.studio_reference_image_url = None

                st.session_state.studio_reference_title = ""

                st.session_state.studio_reference_photographer = ""

                st.rerun()


        # ============================================================
        # OWN UPLOADED IMAGE
        # ============================================================

        reference_image = st.file_uploader(
            "Or Upload Your Own Reference Image",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp"
            ],
            key="advanced_reference_image"
        )


        if reference_image:

            st.success(
                "✅ Your reference image is ready."
            )

            st.image(
                reference_image,
                caption="Your Uploaded Reference",
                use_container_width=True
            )


        # ============================================================
        # TRANSFORMATION INSTRUCTION
        # ============================================================

        st.divider()

        st.subheader(
            "✍️ What should StyleSense do with it?"
        )

        reference_prompt = st.text_area(
            "Describe the transformation",
            height=160,
            placeholder=(
                "Example: Keep the silhouette of this dress "
                "but transform it into a luxury Nigerian evening gown. "
                "Use emerald green velvet, subtle gold embroidery, "
                "structured shoulders and a sophisticated couture finish."
            ),
            key="reference_design_prompt"
        )

        st.caption(
            "You can ask StyleSense to preserve the silhouette, "
            "change the fabric, change colours, add details, "
            "change cultural inspiration or completely redesign it."
        )


        # ============================================================
        # TRANSFORMATION CONTROLS
        # ============================================================

        st.divider()

        st.subheader(
            "🎯 Reference Transformation"
        )

        ref_col1, ref_col2 = st.columns(2)

        with ref_col1:

            preserve_silhouette = st.checkbox(
                "Preserve Original Silhouette",
                value=True,
                key="preserve_reference_silhouette"
            )

            change_fabric = st.checkbox(
                "Allow Fabric Transformation",
                value=True,
                key="reference_change_fabric"
            )

            change_colour = st.checkbox(
                "Allow Colour Transformation",
                value=True,
                key="reference_change_colour"
            )


        with ref_col2:

            change_style = st.checkbox(
                "Allow Style Transformation",
                value=True,
                key="reference_change_style"
            )

            preserve_details = st.checkbox(
                "Preserve Important Details",
                value=True,
                key="reference_preserve_details"
            )

            professional_presentation = st.checkbox(
                "Professional Fashion Presentation",
                value=True,
                key="reference_professional_presentation"
            )


        # ============================================================
        # PREPARE REFERENCE
        # ============================================================

        reference_source = reference_image

        if (
            reference_source is None
            and studio_reference_url
        ):

            try:

                request = urllib.request.Request(
                    studio_reference_url,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

                with urllib.request.urlopen(
                    request,
                    timeout=30
                ) as response:

                    image_bytes = response.read()

                reference_source = io.BytesIO(
                    image_bytes
                )

                reference_source.name = (
                    "pexels_reference.jpg"
                )

            except Exception as e:

                st.error(
                    "Unable to load the Pexels reference image."
                )

                st.caption(
                    str(e)
                )

                reference_source = None


        # ============================================================
        # GENERATE
        # ============================================================

        st.divider()

        if st.button(
            "🎨 Generate From Reference Image",
            use_container_width=True,
            type="primary",
            key="generate_reference_design"
        ):

            if reference_source is None:

                st.warning(
                    "Please upload a reference image "
                    "or select a Pexels inspiration."
                )

            elif not reference_prompt.strip():

                st.warning(
                    "Please describe what you want "
                    "StyleSense to create."
                )

            else:

                transformation_instructions = f"""
        You are an expert fashion designer
        and fashion visual director.

        Use the uploaded reference image
        as the visual foundation.

        USER'S TRANSFORMATION REQUEST:

        {reference_prompt}


        DESIGN RULES:

        Preserve original silhouette:

        {"YES" if preserve_silhouette else "NO"}


        Allow fabric transformation:

        {"YES" if change_fabric else "NO"}


        Allow colour transformation:

        {"YES" if change_colour else "NO"}


        Allow style transformation:

        {"YES" if change_style else "NO"}


        Preserve important original details:

        {"YES" if preserve_details else "NO"}


        Professional fashion presentation:

        {"YES" if professional_presentation else "NO"}


        IMPORTANT:

        The uploaded image is a reference,
        not a restriction.

        Follow the user's transformation
        request carefully.

        If the user requests a new fabric,
        colour, cultural influence,
        embellishment or styling,
        apply those changes while maintaining
        visual coherence.

        The result should look like a
        professionally designed fashion concept
        rather than a simple image filter.

        Create:

        - High-end fashion design
        - Accurate garment construction
        - Elegant proportions
        - Detailed fabric texture
        - Professional styling
        - Sophisticated fashion presentation
        - Luxury editorial quality
        - Full garment visibility
        - Clean composition
        - Highly detailed result

        Do not simply copy the reference.

        Create a new fashion concept
        based on the user's requested transformation.
        """

                with st.spinner(
                    "🧠 StyleSense AI is transforming your reference design..."
                ):

                    try:

                        reference_result = (
                            generate_image_from_reference(
                                reference_source,
                                transformation_instructions
                            )
                        )

                        st.success(
                            "✅ New fashion design created!"
                        )

                        st.divider()

                        st.subheader(
                            "🎨 StyleSense Redesigned Concept"
                        )

                        st.image(
                            reference_result,
                            use_container_width=True
                        )

                        st.divider()

                        st.subheader(
                            "📝 Transformation Request"
                        )

                        st.write(
                            reference_prompt
                        )

                        st.divider()

                        st.subheader(
                            "⚙️ Transformation Summary"
                        )

                        summary_col1, summary_col2 = st.columns(2)

                        with summary_col1:

                            st.info(
                                f"""
        **Silhouette Preserved:**
        {"Yes" if preserve_silhouette else "No"}

        **Fabric Transformation:**
        {"Yes" if change_fabric else "No"}

        **Colour Transformation:**
        {"Yes" if change_colour else "No"}
        """
                            )

                        with summary_col2:

                            st.info(
                                f"""
        **Style Transformation:**
        {"Yes" if change_style else "No"}

        **Important Details Preserved:**
        {"Yes" if preserve_details else "No"}

        **Professional Presentation:**
        {"Yes" if professional_presentation else "No"}
        """
                            )


                        # ====================================================
                        # DOWNLOAD GENERATED DESIGN
                        # ====================================================

                        st.divider()

                        st.subheader(
                            "📥 Export Design"
                        )

                        if isinstance(
                            reference_result,
                            bytes
                        ):

                            st.download_button(
                                "⬇️ Download Generated Design",
                                data=reference_result,
                                file_name=(
                                    "StyleSense_Reference_Design.png"
                                ),
                                mime="image/png",
                                use_container_width=True,
                                key="download_reference_design"
                            )


                        # ====================================================
                        # SAVE TO DESIGN LIBRARY
                        # ====================================================

                        st.session_state.saved_designs.append(
                            {
                                "design": reference_prompt,

                                "image": reference_result,

                                "mode": (
                                    "Reference Image → Design"
                                ),

                                "reference_image": True,

                                "reference_source": (
                                    "Pexels"
                                    if studio_reference_url
                                    else "Uploaded Image"
                                ),

                                "preserve_silhouette":
                                    preserve_silhouette,

                                "change_fabric":
                                    change_fabric,

                                "change_colour":
                                    change_colour,

                                "change_style":
                                    change_style,

                                "preserve_details":
                                    preserve_details,

                                "created_at":
                                    datetime.now().strftime(
                                        "%Y-%m-%d %H:%M"
                                    )
                            }
                        )

                        st.success(
                            "💾 Design saved to your Design Library."
                        )


                        # ====================================================
                        # CLEAR PEXELS REFERENCE AFTER GENERATION
                        # ====================================================

                        st.session_state.studio_reference_image_url = None

                        st.session_state.studio_reference_title = ""

                        st.session_state.studio_reference_photographer = ""


                    except Exception as e:

                        st.error(
                            "Reference image generation failed."
                        )

                        st.exception(e)

            # ----------------------------------------------------
            # REFERENCE CONTROLS
            # ----------------------------------------------------

            ref_col1, ref_col2 = st.columns(2)

            with ref_col1:

                preserve_silhouette = st.checkbox(
                    "Preserve Original Silhouette",
                    value=True,
                    key="preserve_reference_silhouette"
                )

                change_fabric = st.checkbox(
                    "Allow Fabric Transformation",
                    value=True,
                    key="reference_change_fabric"
                )

                change_colour = st.checkbox(
                    "Allow Colour Transformation",
                    value=True,
                    key="reference_change_colour"
                )

            with ref_col2:

                change_style = st.checkbox(
                    "Allow Style Transformation",
                    value=True,
                    key="reference_change_style"
                )

                preserve_details = st.checkbox(
                    "Preserve Important Details",
                    value=True,
                    key="reference_preserve_details"
                )

                professional_presentation = st.checkbox(
                    "Professional Fashion Presentation",
                    value=True,
                    key="reference_professional_presentation"
                )

            st.divider()

            if st.button(
                "🎨 Generate Outcome",
                use_container_width=True,
                type="primary",
                key="generate_reference_design"
            ):

                if not reference_prompt.strip():

                    st.warning(
                        "Please tell StyleSense what you want it to create."
                    )

                else:

                    transformation_instructions = f"""
You are an expert fashion designer and fashion visual director.

Use the uploaded reference image as the visual foundation.

USER REQUEST:
{reference_prompt}

DESIGN RULES:

Preserve original silhouette:
{"YES" if preserve_silhouette else "NO"}

Allow fabric transformation:
{"YES" if change_fabric else "NO"}

Allow colour transformation:
{"YES" if change_colour else "NO"}

Allow style transformation:
{"YES" if change_style else "NO"}

Preserve important details:
{"YES" if preserve_details else "NO"}

Professional fashion presentation:
{"YES" if professional_presentation else "NO"}

Follow the user's request carefully.

The reference image is a visual starting point.

Create a professional fashion design with:

- Accurate garment construction
- Elegant proportions
- Detailed fabric texture
- Professional styling
- Sophisticated fashion presentation
- Luxury editorial quality
- Full garment visibility
- Clean composition
- Highly detailed result
"""

                    with st.spinner(
                        "🧠 StyleSense AI is creating your new design..."
                    ):

                        try:

                            reference_result = (
                                generate_image_from_reference(
                                    reference_image,
                                    transformation_instructions
                                )
                            )

                            st.session_state.reference_image_result = (
                                reference_result
                            )

                            # Save to library
                            st.session_state.saved_designs.append(
                                {
                                    "design": reference_prompt,
                                    "image": reference_result,

                                    "mode":
                                        "Reference Image → Design",

                                    "preserve_silhouette":
                                        preserve_silhouette,

                                    "change_fabric":
                                        change_fabric,

                                    "change_colour":
                                        change_colour,

                                    "change_style":
                                        change_style,

                                    "preserve_details":
                                        preserve_details,

                                    "created_at":
                                        datetime.now().strftime(
                                            "%Y-%m-%d %H:%M"
                                        )
                                }
                            )

                            st.success(
                                "✅ New design generated successfully!"
                            )

                            st.image(
                                reference_result,
                                use_container_width=True
                            )

                            st.info(
                                "💾 Your design is now available in 📂 Design Library."
                            )

                        except Exception as e:

                            st.error(
                                f"Reference image generation failed.\n\n{e}"
                            )

    # ============================================================
    # DESIGN LIBRARY
    # ============================================================

    with tab3:

        st.subheader("📂 Design Library")

        st.caption(
            "View, download and manage your AI-generated fashion designs."
        )

        st.divider()

        if not st.session_state.saved_designs:

            st.info(
                "No designs in your library yet. "
                "Create a design from the Design or Advanced tab."
            )

        else:

            for i, design in enumerate(
                reversed(st.session_state.saved_designs),
                start=1
            ):

                mode = design.get(
                    "mode",
                    "Guided Design"
                )

                created_at = design.get(
                    "created_at",
                    ""
                )

                with st.expander(
                    f"🎨 Design {i} • {mode} • {created_at}"
                ):

                    # ------------------------------------------------
                    # IMAGE
                    # ------------------------------------------------

                    if design.get("image"):

                        st.image(
                            design["image"],
                            use_container_width=True
                        )

                        st.download_button(
                            "⬇️ Download Design Image",
                            data=design["image"],
                            file_name=(
                                f"StyleSense_Design_{i}.png"
                            ),
                            mime="image/png",
                            use_container_width=True,
                            key=f"download_image_{i}"
                        )

                    st.divider()

                    # ------------------------------------------------
                    # DESIGN DESCRIPTION
                    # ------------------------------------------------

                    st.subheader("📝 Design Description")

                    st.write(
                        design.get(
                            "design",
                            "No description available."
                        )
                    )

                    # ------------------------------------------------
                    # ADVANCED DESIGN DETAILS
                    # ------------------------------------------------

                    if mode == "Advanced Prompt-to-Design":

                        st.divider()

                        st.subheader(
                            "⚙️ Design Details"
                        )

                        library_col1, library_col2 = st.columns(2)

                        with library_col1:

                            st.write(
                                f"**Style:** "
                                f"{design.get('style', 'AI Choice')}"
                            )

                            st.write(
                                f"**Fabric:** "
                                f"{design.get('fabric', 'AI Choice')}"
                            )

                            st.write(
                                f"**Colour:** "
                                f"{design.get('colour', 'AI Choice')}"
                            )

                        with library_col2:

                            st.write(
                                f"**Occasion:** "
                                f"{design.get('occasion', 'AI Choice')}"
                            )

                            st.write(
                                f"**Target Market:** "
                                f"{design.get('market', 'AI Choice')}"
                            )

                            st.write(
                                f"**Culture:** "
                                f"{design.get('culture', 'AI Choice')}"
                            )

                    # ------------------------------------------------
                    # REFERENCE DESIGN DETAILS
                    # ------------------------------------------------

                    if mode == "Reference Image → Design":

                        st.divider()

                        st.subheader(
                            "🖼️ Reference Transformation"
                        )

                        ref_library_col1, ref_library_col2 = (
                            st.columns(2)
                        )

                        with ref_library_col1:

                            st.write(
                                "**Silhouette Preserved:** "
                                + (
                                    "Yes"
                                    if design.get(
                                        "preserve_silhouette"
                                    )
                                    else "No"
                                )
                            )

                            st.write(
                                "**Fabric Transformation:** "
                                + (
                                    "Yes"
                                    if design.get(
                                        "change_fabric"
                                    )
                                    else "No"
                                )
                            )

                            st.write(
                                "**Colour Transformation:** "
                                + (
                                    "Yes"
                                    if design.get(
                                        "change_colour"
                                    )
                                    else "No"
                                )
                            )

                        with ref_library_col2:

                            st.write(
                                "**Style Transformation:** "
                                + (
                                    "Yes"
                                    if design.get(
                                        "change_style"
                                    )
                                    else "No"
                                )
                            )

                            st.write(
                                "**Important Details Preserved:** "
                                + (
                                    "Yes"
                                    if design.get(
                                        "preserve_details"
                                    )
                                    else "No"
                                )
                            )

                    # ------------------------------------------------
                    # PDF REPORT
                    # ------------------------------------------------

                    st.divider()

                    st.subheader(
                        "📄 Export"
                    )

                    report_text = f"""
StyleSense AI Fashion Design

Design Type:
{mode}

Created:
{created_at}

Design Description:
{design.get("design", "")}
"""

                    try:

                        library_pdf = create_pdf(
                            report_text
                        )

                        with open(
                            library_pdf,
                            "rb"
                        ) as pdf_file:

                            st.download_button(
                                "📄 Download Design Report",
                                data=pdf_file.read(),
                                file_name=(
                                    f"StyleSense_Design_Report_{i}.pdf"
                                ),
                                mime="application/pdf",
                                use_container_width=True,
                                key=f"download_pdf_{i}"
                            )

                    except Exception as e:

                        st.warning(
                            f"PDF export unavailable: {e}"
                        )

    # ============================================================
    # EXISTING GUIDED GENERATION
    # ============================================================

    st.divider()

    if st.button(
        "🚀 Generate Luxury Fashion Design",
        use_container_width=True
    ):

        with st.spinner(
            "🧠 AI is designing your fashion concept..."
        ):

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

                st.success(
                    "✅ Design generated successfully!"
                )

                st.divider()

                st.subheader(
                    "📝 AI Fashion Concept"
                )

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

                st.subheader(
                    "🎨 AI Fashion Sketch"
                )

                with st.spinner(
                    "Generating fashion illustration..."
                ):

                    try:

                        image = generate_image(
                            image_prompt
                        )

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

                st.subheader(
                    "👠 Accessories"
                )

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

                st.subheader(
                    "🧵 Production Recommendation"
                )

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

                st.subheader(
                    "💰 Suggested Selling Price"
                )

                prices = {
                    "Simple": "₦50,000 - ₦120,000",
                    "Moderate": "₦120,000 - ₦300,000",
                    "Luxury": "₦300,000 - ₦1,000,000+"
                }

                st.success(
                    prices.get(complexity)
                )

                st.divider()

                st.subheader(
                    "📣 Marketing Caption"
                )

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

                st.divider()

                # ------------------------------------------------
                # SAVE GUIDED DESIGN TO LIBRARY
                # ------------------------------------------------

                st.session_state.saved_designs.append(
                    {
                        "design": result,
                        "image": image,

                        "mode": "Guided Design",

                        "gender": gender,
                        "age": age,
                        "height": height,
                        "body_shape": body_shape,
                        "skin_tone": skin_tone,

                        "category": category,
                        "fabric": fabric,
                        "colors": colors,

                        "occasion": occasion,
                        "budget": budget,
                        "complexity": complexity,
                        "theme": theme,

                        "country": country,
                        "climate": climate,

                        "embroidery": embroidery,
                        "accessories": accessories,

                        "created_at": datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    }
                )

                st.success(
                    "💾 Design saved to your Design Library."
                )

                # ------------------------------------------------
                # REMAINING EXISTING OUTPUT
                # ------------------------------------------------

                st.divider()

                st.subheader(
                    "✂ Tailoring Instructions"
                )

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

                st.subheader(
                    "💰 Production Cost Estimate"
                )

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

                st.subheader(
                    "📦 Packaging Recommendation"
                )

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

                st.subheader(
                    "📸 Photoshoot Ideas"
                )

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

                st.subheader(
                    "📱 Instagram Advertisement"
                )

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

                st.subheader(
                    "🏷 AI Brand Name Suggestions"
                )

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

                st.subheader(
                    "📈 AI Fashion Insights"
                )

                insight1, insight2 = st.columns(2)

                with insight1:

                    st.info(
                        f"""
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
"""
                    )

                with insight2:

                    st.success(
                        """
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
"""
                    )

                st.divider()

                st.subheader(
                    "🎨 Recommended Color Palette"
                )

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

                for i, colour in enumerate(
                    recommended[:6]
                ):

                    palette[i].success(
                        colour
                    )

                st.divider()

                st.subheader(
                    "✅ Fashion Production Checklist"
                )

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

                st.divider()

                st.subheader(
                    "🤖 AI Recommendations"
                )

                recommendations = [

                    "Increase embroidery for premium appeal.",

                    "Use luxury photography for marketing.",

                    "Offer limited edition releases.",

                    "Target Instagram and TikTok first.",

                    "Bundle matching accessories."

                ]

                for recommendation in recommendations:

                    st.success(
                        recommendation
                    )

            except Exception as e:

                st.error(e)