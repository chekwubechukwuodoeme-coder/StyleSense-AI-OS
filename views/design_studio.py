import io
from datetime import datetime

import streamlit as st

from ai import generate_design

from image_generator import (
    generate_image,
    generate_image_from_reference,
)

from pdf_generator import create_pdf


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {

    "saved_designs": [],

    "current_design": "",

    "advanced_prompt": "",

    "advanced_enhanced_prompt": "",

    "advanced_image": None,

    "reference_image_result": None,

    # Pexels → Design Studio
    "studio_reference_image_url": None,

    "studio_reference_title": "",

    "studio_reference_photographer": "",

    "open_design_studio": False,
}


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# PEXELS REFERENCE DOWNLOAD
# ============================================================

def load_reference_from_url(url):

    """
    Download the original Pexels image into memory.

    The resulting BytesIO object can be passed to the
    reference-image generator.
    """

    if not url:

        return None

    try:

        import urllib.request

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            image_bytes = response.read()

        image_file = io.BytesIO(
            image_bytes
        )

        image_file.name = "pexels_reference.jpg"

        return image_file

    except Exception as e:

        st.error(
            f"Unable to load reference image: {e}"
        )

        return None


# ============================================================
# DESIGN STUDIO
# ============================================================

def render_design_studio():

    st.title(
        "✨ AI Design Studio Pro"
    )

    st.caption(
        "Create luxury fashion designs powered by StyleSense AI."
    )

    st.divider()

    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "🎨 Design",
            "⚙️ Advanced",
            "📂 Saved"
        ]
    )

    # ========================================================
    # DESIGN TAB
    # ========================================================

    with tab1:

        left, right = st.columns(2)

        # ====================================================
        # DESIGNER
        # ====================================================

        with left:

            st.subheader(
                "👤 Designer"
            )

            gender = st.selectbox(
                "Gender",
                [
                    "Male",
                    "Female",
                    "Unisex"
                ],
                key="studio_gender"
            )

            age = st.slider(
                "Age",
                5,
                80,
                25,
                key="studio_age"
            )

            height = st.slider(
                "Height (cm)",
                120,
                220,
                170,
                key="studio_height"
            )

            body_shape = st.selectbox(
                "Body Shape",
                [
                    "Slim",
                    "Athletic",
                    "Average",
                    "Curvy",
                    "Plus Size"
                ],
                key="studio_body_shape"
            )

            skin_tone = st.selectbox(
                "Skin Tone",
                [
                    "Fair",
                    "Light Brown",
                    "Brown",
                    "Dark Brown",
                    "Deep Black"
                ],
                key="studio_skin_tone"
            )

            st.divider()

            st.subheader(
                "👗 Fashion"
            )

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
                ],
                key="studio_category"
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
                ],
                key="studio_fabric"
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
                ],
                key="studio_colors"
            )

        # ====================================================
        # OCCASION
        # ====================================================

        with right:

            st.subheader(
                "🎯 Occasion"
            )

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
                ],
                key="studio_occasion"
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
                ],
                key="studio_budget"
            )

            complexity = st.selectbox(
                "Complexity",
                [
                    "Simple",
                    "Moderate",
                    "Luxury"
                ],
                key="studio_complexity"
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
                ],
                key="studio_theme"
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
                ],
                key="studio_country"
            )

            climate = st.selectbox(
                "Climate",
                [
                    "Hot",
                    "Cold",
                    "Rainy",
                    "Dry"
                ],
                key="studio_climate"
            )

            embroidery = st.checkbox(
                "Include Embroidery",
                value=True,
                key="studio_embroidery"
            )

            accessories = st.checkbox(
                "Recommend Accessories",
                value=True,
                key="studio_accessories"
            )

    # ============================================================
    # ADVANCED
    # ============================================================

    with tab2:

        st.subheader(
            "⚙️ Advanced AI Design"
        )

        st.caption(
            "Use natural language to create a professional fashion design."
        )

        # ========================================================
        # PEXELS REFERENCE FROM FASHION INSPIRATION
        # ========================================================

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

        if studio_reference_url:

            st.success(
                "✨ Fashion Inspiration loaded from Fashion Inspiration."
            )

            st.image(
                studio_reference_url,
                caption=studio_reference_title,
                use_container_width=True
            )

            st.caption(
                f"📸 Original inspiration by "
                f"{studio_reference_photographer}"
            )

            st.info(
                "This is the original Pexels inspiration. "
                "Describe exactly how you want StyleSense AI "
                "to transform it below."
            )

            if st.button(
                "✕ Remove Inspiration",
                key="remove_pexels_studio_reference",
                use_container_width=True
            ):

                st.session_state.studio_reference_image_url = None

                st.session_state.studio_reference_title = ""

                st.session_state.studio_reference_photographer = ""

                st.rerun()

            st.divider()

        # ========================================================
        # AI SETTINGS
        # ========================================================

        st.subheader(
            "🧠 AI Settings"
        )

        ai_creativity = st.slider(
            "AI Creativity",
            1,
            10,
            8,
            key="advanced_ai_creativity"
        )

        st.caption(
            "Higher creativity produces more artistic and experimental concepts."
        )

        st.success(
            "🟢 OpenAI Image Generation Enabled"
        )

        st.divider()

        # ========================================================
        # PROMPT TO DESIGN
        # ========================================================

        st.subheader(
            "🚀 Prompt-to-Design"
        )

        st.write(
            "Describe exactly what you want to create."
        )

        prompt_examples = [

            "Create a luxurious emerald green evening gown with an asymmetric neckline, sculptural sleeves, subtle gold embroidery and a fitted silhouette.",

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

                st.session_state.advanced_prompt = (
                    example_choice
                )

                st.rerun()

        prompt = st.text_area(
            "Describe Your Fashion Design",
            value=st.session_state.advanced_prompt,
            height=180,
            placeholder=(
                "Example: Create a luxury floor-length emerald "
                "green evening gown..."
            ),
            key="advanced_prompt_input"
        )

        st.divider()

        # ========================================================
        # OPTIONAL DESIGN CONTROLS
        # ========================================================

        st.subheader(
            "🎯 Optional Design Controls"
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

        st.divider()

        # ========================================================
        # PROMPT ENHANCEMENT
        # ========================================================

        st.subheader(
            "✨ AI Prompt Enhancement"
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
- Cultural details
- Overall aesthetic
- Luxury fashion quality
- Professional presentation

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

            st.subheader(
                "📝 Enhanced Fashion Prompt"
            )

            st.text_area(
                "AI Enhanced Prompt",
                value=st.session_state.advanced_enhanced_prompt,
                height=260,
                disabled=True,
                key="display_enhanced_prompt"
            )

        st.divider()

        # ========================================================
        # GENERATE PROMPT DESIGN
        # ========================================================

        if st.button(
            "🎨 Generate Design From Prompt",
            use_container_width=True,
            type="primary",
            key="generate_advanced_design"
        ):

            if not prompt.strip():

                st.warning(
                    "Please describe the fashion design you want."
                )

            else:

                final_prompt = (
                    st.session_state.advanced_enhanced_prompt
                    if st.session_state.advanced_enhanced_prompt
                    else prompt
                )

                image_prompt = f"""
Create a professional luxury fashion design.

Creative Direction:
{final_prompt}

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

Embroidery:
{"Include sophisticated embroidery." if advanced_embroidery else "Use embellishment only when appropriate."}

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
- Premium editorial quality
- Highly detailed
- 4K quality

The garment must remain the primary focus.
"""

                with st.spinner(
                    "🧠 StyleSense AI is creating your design..."
                ):

                    try:

                        image = generate_image(
                            image_prompt
                        )

                        st.session_state.advanced_image = image

                        st.session_state.current_design = prompt

                        st.success(
                            "✅ Fashion design generated successfully!"
                        )

                        st.image(
                            image,
                            use_container_width=True
                        )

                        st.subheader(
                            "📝 Design Concept"
                        )

                        st.write(prompt)

                        # ----------------------------------------
                        # SAVE
                        # ----------------------------------------

                        st.session_state.saved_designs.append(
                            {
                                "design": prompt,
                                "image": image,

                                "mode":
                                    "Advanced Prompt-to-Design",

                                "style":
                                    advanced_style,

                                "fabric":
                                    advanced_fabric,

                                "colour":
                                    advanced_colour,

                                "occasion":
                                    advanced_occasion,

                                "market":
                                    advanced_market,

                                "culture":
                                    advanced_culture,

                                "created_at":
                                    datetime.now().strftime(
                                        "%Y-%m-%d %H:%M"
                                    )
                            }
                        )

                        st.success(
                            "💾 Design automatically saved to Design Library."
                        )

                        # ----------------------------------------
                        # DOWNLOAD
                        # ----------------------------------------

                        if isinstance(image, bytes):

                            st.download_button(
                                "📥 Download Design",
                                data=image,
                                file_name="StyleSense_AI_Design.png",
                                mime="image/png",
                                use_container_width=True,
                                key="advanced_download_image"
                            )

                    except Exception as e:

                        st.error(
                            f"Advanced design generation failed:\n\n{e}"
                        )

        # ========================================================
        # REFERENCE IMAGE → DESIGN
        # ========================================================

        st.divider()

        st.subheader(
            "🖼️ Reference Image → Design"
        )

        st.caption(
            "Upload your own reference image OR use a Pexels inspiration "
            "from Fashion Inspiration."
        )

        # ========================================================
        # PEXELS REFERENCE
        # ========================================================

        studio_reference_url = st.session_state.get(
            "studio_reference_image_url"
        )

        reference_source = None

        if studio_reference_url:

            st.success(
                "✨ Using Pexels Fashion Inspiration as reference."
            )

            st.image(
                studio_reference_url,
                use_container_width=True
            )

            reference_source = load_reference_from_url(
                studio_reference_url
            )

        # ========================================================
        # UPLOAD YOUR OWN IMAGE
        # ========================================================

        uploaded_reference = st.file_uploader(
            "Or Upload Your Own Reference Image",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp"
            ],
            key="advanced_reference_image"
        )

        if uploaded_reference:

            st.image(
                uploaded_reference,
                caption="Uploaded Reference",
                use_container_width=True
            )

            reference_source = uploaded_reference

        # ========================================================
        # TRANSFORMATION
        # ========================================================

        if studio_reference_url or uploaded_reference:

            reference_prompt = st.text_area(
                "✍️ What do you want StyleSense AI to do?",
                height=160,
                placeholder=(
                    "Example: Keep the silhouette but transform "
                    "this into a luxury Nigerian evening gown. "
                    "Use emerald green velvet with gold embroidery."
                ),
                key="reference_design_prompt"
            )

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

            if st.button(
                "🎨 Generate From Reference Image",
                use_container_width=True,
                type="primary",
                key="generate_reference_design"
            ):

                if not reference_prompt.strip():

                    st.warning(
                        "Please describe what you want StyleSense AI to create."
                    )

                elif reference_source is None:

                    st.error(
                        "Reference image could not be loaded."
                    )

                else:

                    transformation_instructions = f"""
You are an expert fashion designer and fashion visual director.

Use the uploaded reference image as the visual foundation.

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

Preserve important details:
{"YES" if preserve_details else "NO"}

The reference image is inspiration, not a restriction.

Follow the user's transformation request carefully.

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

Do not simply apply an image filter.
Create a professional fashion concept.
"""

                    with st.spinner(
                        "🧠 StyleSense AI is transforming your reference..."
                    ):

                        try:

                            reference_result = (
                                generate_image_from_reference(
                                    reference_source,
                                    transformation_instructions
                                )
                            )

                            st.session_state.reference_image_result = (
                                reference_result
                            )

                            st.success(
                                "✅ New fashion design created!"
                            )

                            st.image(
                                reference_result,
                                use_container_width=True
                            )

                            st.subheader(
                                "📝 Transformation Request"
                            )

                            st.write(
                                reference_prompt
                            )

                            # ------------------------------------
                            # SAVE
                            # ------------------------------------

                            st.session_state.saved_designs.append(
                                {
                                    "design":
                                        reference_prompt,

                                    "image":
                                        reference_result,

                                    "mode":
                                        "Reference Image → Design",

                                    "category":
                                        "Reference Design",

                                    "reference_source":
                                        "Pexels"
                                        if studio_reference_url
                                        else "Uploaded Image",

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
                                "💾 Design saved to Design Library."
                            )

                            # ------------------------------------
                            # DOWNLOAD
                            # ------------------------------------

                            if isinstance(
                                reference_result,
                                bytes
                            ):

                                st.download_button(
                                    "📥 Download Generated Design",
                                    data=reference_result,
                                    file_name=(
                                        "StyleSense_"
                                        "Reference_Design.png"
                                    ),
                                    mime="image/png",
                                    use_container_width=True,
                                    key="download_reference_design"
                                )

                        except Exception as e:

                            st.error(
                                f"Reference image generation failed:\n\n{e}"
                            )

    # ========================================================
    # SAVED TAB
    # ========================================================

    with tab3:

        st.subheader(
            "📂 Saved Designs"
        )

        if not st.session_state.saved_designs:

            st.info(
                "No saved designs yet."
            )

        else:

            for i, design in enumerate(
                reversed(
                    st.session_state.saved_designs
                ),
                start=1
            ):

                mode = design.get(
                    "mode",
                    "Fashion Design"
                )

                with st.expander(
                    f"🎨 Design {i} • {mode}"
                ):

                    st.write(
                        design.get(
                            "design",
                            ""
                        )
                    )

                    image = design.get(
                        "image"
                    )

                    if image:

                        st.image(
                            image,
                            use_container_width=True
                        )

                        if isinstance(
                            image,
                            bytes
                        ):

                            st.download_button(
                                "📥 Download Image",
                                data=image,
                                file_name=(
                                    f"StyleSense_Design_{i}.png"
                                ),
                                mime="image/png",
                                use_container_width=True,
                                key=f"saved_download_{i}"
                            )

                    st.caption(
                        f"Created: "
                        f"{design.get('created_at', '')}"
                    )