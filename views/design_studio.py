import io
import urllib.request
import uuid
import threading
from datetime import datetime

import streamlit as st

from ai import generate_design

from image_generator import (
    generate_image,
    generate_image_from_reference
)

from database.database import (
    save_design_to_database,
    create_design_job,
    get_design_job,
    update_design_job
)

from utilis.image_utilis import (
    image_to_bytes
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_image_bytes(image):
    """
    Convert any supported image object into bytes.

    This is used for:
    - Downloading generated images
    - Saving images to SQLite
    """

    if image is None:

        return None

    try:

        return image_to_bytes(
            image
        )

    except Exception:

        pass

    # --------------------------------------------------------
    # Raw bytes
    # --------------------------------------------------------

    if isinstance(
        image,
        bytes
    ):

        return image

    # --------------------------------------------------------
    # BytesIO
    # --------------------------------------------------------

    if isinstance(
        image,
        io.BytesIO
    ):

        try:

            image.seek(0)

            return image.read()

        except Exception:

            return None

    # --------------------------------------------------------
    # File-like objects
    # --------------------------------------------------------

    if hasattr(
        image,
        "read"
    ):

        try:

            position = None

            if hasattr(
                image,
                "tell"
            ):

                position = image.tell()

            data = image.read()

            if position is not None:

                try:

                    image.seek(
                        position
                    )

                except Exception:

                    pass

            return data

        except Exception:

            return None

    # --------------------------------------------------------
    # PIL images
    # --------------------------------------------------------

    try:

        from PIL import Image

        if isinstance(
            image,
            Image.Image
        ):

            buffer = io.BytesIO()

            image.save(
                buffer,
                format="PNG"
            )

            buffer.seek(0)

            return buffer.read()

    except Exception:

        pass

    return None


# ============================================================
# SAFE SAVE
# ============================================================

def save_design(design_data):
    """
    Save a design to the permanent SQLite database
    and the current Streamlit session.
    """

    if "saved_designs" not in st.session_state:

        st.session_state.saved_designs = []

    # --------------------------------------------------------
    # Make a copy
    # --------------------------------------------------------

    database_design = dict(
        design_data
    )

    # --------------------------------------------------------
    # Convert image to bytes
    # --------------------------------------------------------

    image = database_design.get(
        "image"
    )

    image_bytes = get_image_bytes(
        image
    )

    database_design["image_data"] = (
        image_bytes
    )

    # --------------------------------------------------------
    # Save to database
    # --------------------------------------------------------

    design_id = save_design_to_database(
        database_design
    )

    # --------------------------------------------------------
    # Session copy
    # --------------------------------------------------------

    session_design = dict(
        design_data
    )

    session_design["id"] = (
        design_id
    )

    st.session_state.saved_designs.append(
        session_design
    )

    return design_id

# ============================================================
# BACKGROUND DESIGN GENERATION
# ============================================================

def generate_design_job(
    job_id,
    user_id,
    image_prompt
):
    """
    Generate an AI fashion design and update the
    persistent design job when finished.
    """

    try:

        # ----------------------------------------------------
        # MARK JOB AS RUNNING
        # ----------------------------------------------------

        update_design_job(
            job_id,
            "running"
        )

        # ----------------------------------------------------
        # GENERATE IMAGE
        # ----------------------------------------------------

        image = generate_image(
            image_prompt
        )

        # ----------------------------------------------------
        # CONVERT IMAGE TO BYTES
        # ----------------------------------------------------

        image_bytes = get_image_bytes(
            image
        )

        if not image_bytes:

            raise Exception(
                "AI generated an image but no image data was returned."
            )

        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        update_design_job(
            job_id,
            "completed",
            image_data=image_bytes
        )

    except Exception as e:

        # ----------------------------------------------------
        # SAVE ERROR
        # ----------------------------------------------------

        update_design_job(
            job_id,
            "failed",
            error=str(e)
        )

    # ========================================================
    # BACKGROUND DESIGN JOB
    # ========================================================

    active_job_id = st.session_state.get(
        "active_design_job"
    )

    if active_job_id:

        job = get_design_job(
            active_job_id
        )

        if job:

            status = job.get(
                "status"
            )

            # ------------------------------------------------
            # COMPLETED
            # ------------------------------------------------

            if status == "completed":

                st.success(
                    "🎉 Your AI fashion design is ready!"
                )

                image_data = job.get(
                    "image_data"
                )

                if image_data:

                    st.subheader(
                        "🎨 Generated Design"
                    )

                    image_bytes = bytes(
                        image_data
                    )

                    st.image(
                        image_bytes,
                        use_container_width=True
                    )

                    st.download_button(
                        "⬇️ Download Design",
                        data=image_bytes,
                        file_name="StyleSense_AI_Design.png",
                        mime="image/png",
                        use_container_width=True,
                        key=f"completed_download_{active_job_id}"
                    )

                else:

                    st.error(
                        "The AI finished, but the generated image was not saved."
                    )

            # ------------------------------------------------
            # RUNNING
            # ------------------------------------------------

            elif status == "running":

                st.info(
                    "🧠 StyleSense AI is still generating your design..."
                )

            # ------------------------------------------------
            # PENDING
            # ------------------------------------------------

            elif status == "pending":

                st.info(
                    "⏳ Your design is waiting to start..."
                )

            # ------------------------------------------------
            # FAILED
            # ------------------------------------------------

            elif status == "failed":

                st.error(
                    "❌ Design generation failed."
                )

                if job.get("error"):

                    st.caption(
                        job["error"]
                    )

# ============================================================
# MAIN DESIGN STUDIO
# ============================================================

def render_design_studio():

    active_job_id = st.session_state.get(
        "active_design_job"
    )

    if active_job_id:

        job = get_design_job(
            active_job_id
        )

        if job:

            if job["status"] == "completed":

                st.success(
                    "🎉 Your AI fashion design is ready!"
                )

                image_data = job.get(
                    "image_data"
                )

                if image_data:

                    st.success(
                        f"✅ Image data found: {len(image_data):,} bytes"
                    )

                    st.image(
                        bytes(image_data),
                        use_container_width=True
                    )

                else:

                    st.error(
                        "❌ Job completed, but image_data is empty."
                    )

            elif job["status"] == "running":

                st.info(
                    "🧠 StyleSense AI is still generating your design..."
                )

            elif job["status"] == "failed":

                st.error(
                    "❌ Design generation failed."
                )

    st.title(
        "✨ AI Design Studio"
    )

    st.caption(
        "Your intelligent fashion workspace for creating, "
        "transforming and managing AI-powered fashion designs."
    )

    st.divider()

    # ========================================================
    # SESSION STATE
    # ========================================================

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

    if "advanced_ai_creativity" not in st.session_state:

        st.session_state.advanced_ai_creativity = 8

    # ========================================================
    # BACKGROUND DESIGN GENERATION
    # ========================================================

    if "design_generation_job_id" not in st.session_state:

        st.session_state.design_generation_job_id = None

    if "design_generation_type" not in st.session_state:

        st.session_state.design_generation_type = None

    if "design_generation_prompt" not in st.session_state:

        st.session_state.design_generation_prompt = None

    # ========================================================
    # FASHION INSPIRATION
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

    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "🎨 Create",
            "✨ Prompt Studio",
            "🖼 Reference"
        ]
    )

    # ========================================================
    # TAB 1 — GUIDED DESIGN
    # ========================================================

    with tab1:

        st.subheader(
            "🎨 Guided AI Fashion Designer"
        )

        st.caption(
            "Tell StyleSense who the design is for, what they are "
            "wearing, where they are going and how you want it to look."
        )

        left, right = st.columns(2)

        # ====================================================
        # DESIGNER PROFILE
        # ====================================================

        with left:

            st.subheader(
                "👤 Designer Profile"
            )

            gender = st.selectbox(
                "Gender",
                [
                    "Male",
                    "Female",
                    "Unisex"
                ],
                key="guided_gender"
            )

            age = st.slider(
                "Age",
                5,
                80,
                25,
                key="guided_age"
            )

            height = st.slider(
                "Height (cm)",
                120,
                220,
                170,
                key="guided_height"
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
                key="guided_body_shape"
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
                key="guided_skin_tone"
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
                key="guided_category"
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
                key="guided_fabric"
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
                key="guided_colors"
            )

        # ====================================================
        # OCCASION
        # ====================================================

        with right:

            st.subheader(
                "🎯 Occasion & Direction"
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
                key="guided_occasion"
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
                key="guided_budget"
            )

            complexity = st.selectbox(
                "Complexity",
                [
                    "Simple",
                    "Moderate",
                    "Luxury"
                ],
                key="guided_complexity"
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
                key="guided_theme"
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
                key="guided_country"
            )

            climate = st.selectbox(
                "Climate",
                [
                    "Hot",
                    "Cold",
                    "Rainy",
                    "Dry"
                ],
                key="guided_climate"
            )

            embroidery = st.checkbox(
                "✨ Include Embroidery",
                value=True,
                key="guided_embroidery"
            )

            accessories = st.checkbox(
                "👜 Recommend Accessories",
                value=True,
                key="guided_accessories"
            )

        # ====================================================
        # AI CREATIVITY
        # ====================================================

        st.divider()

        st.subheader(
            "🧠 AI Creativity"
        )

        ai_creativity = st.slider(
            "How creative should StyleSense be?",
            1,
            10,
            8,
            key="guided_ai_creativity"
        )

        st.caption(
            "Higher values allow StyleSense to create more "
            "experimental and unconventional fashion concepts."
        )

        # ====================================================
        # GENERATE
        # ====================================================

        st.divider()

        if st.button(
            "🚀 Generate Luxury Fashion Design",
            use_container_width=True,
            type="primary",
            key="generate_guided_design"
        ):

            with st.spinner(
                "🧠 StyleSense AI is designing your fashion concept..."
            ):

                try:

                    # ----------------------------------------
                    # AI CONCEPT
                    # ----------------------------------------

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

                    st.session_state.current_design = (
                        result
                    )

                    st.success(
                        "✅ Fashion concept generated."
                    )

                    st.divider()

                    st.subheader(
                        "📝 AI Fashion Concept"
                    )

                    st.write(
                        result
                    )

                    # ----------------------------------------
                    # IMAGE PROMPT
                    # ----------------------------------------

                    image_prompt = f"""
Create a professional luxury fashion design.

Gender: {gender}
Age: {age}
Height: {height} cm
Body Shape: {body_shape}
Skin Tone: {skin_tone}

Category: {category}
Fabric: {fabric}
Occasion: {occasion}
Theme: {theme}
Complexity: {complexity}

Country:
{country}

Climate:
{climate}

Preferred Colors:
{", ".join(colors) if colors else "Designer Choice"}

Embroidery:
{"Include sophisticated embroidery." if embroidery else "No mandatory embroidery."}

Create a full-body professional fashion presentation.

The garment should have:

- Accurate garment construction
- Elegant proportions
- Detailed fabric texture
- Sophisticated styling
- Luxury fashion quality
- Editorial presentation
- Clean composition
- Professional pose
- Full garment visibility
- Premium fashion illustration quality

The garment must remain the main focus.
"""

                    # ----------------------------------------
                    # IMAGE
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "🎨 AI Fashion Visualization"
                    )

                    image = None

                    # ========================================================
                    # GENERATE IMAGE
                    # ========================================================

                    image = None

                    with st.spinner(
                        "🎨 StyleSense AI is generating your fashion visualization..."
                    ):

                        try:

                            image = generate_image(
                                image_prompt
                            )

                            if image:

                                st.success(
                                    "✨ Your AI fashion design is ready!"
                                )

                                st.session_state.current_image = image

                                st.session_state.advanced_image = image

                                st.image(
                                    image,
                                    use_container_width=True
                                )

                            else:

                                st.warning(
                                    "⚠️ No image was generated."
                                )

                        except Exception as e:

                            st.error(
                                "❌ AI design generation failed."
                            )

                            st.caption(
                                str(e)
                            )

                    # ----------------------------------------
                    # ACCESSORIES
                    # ----------------------------------------

                    if accessories:

                        st.divider()

                        st.subheader(
                            "👠 Recommended Accessories"
                        )

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

                    # ----------------------------------------
                    # PRODUCTION
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "🧵 Production Recommendation"
                    )

                    st.info(
                        f"""
**Recommended Fabric:** {fabric}

**Recommended Market:** Luxury Fashion

**Estimated Completion:** 5–10 Days

**Quality Level:** Premium
"""
                    )

                    # ----------------------------------------
                    # SELLING PRICE
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "💰 Suggested Selling Price"
                    )

                    prices = {
                        "Simple":
                            "₦50,000 – ₦120,000",

                        "Moderate":
                            "₦120,000 – ₦300,000",

                        "Luxury":
                            "₦300,000 – ₦1,000,000+"
                    }

                    st.success(
                        prices.get(
                            complexity,
                            "Contact designer"
                        )
                    )

                    # ----------------------------------------
                    # MARKETING
                    # ----------------------------------------

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

                    st.code(
                        caption
                    )

                    # ----------------------------------------
                    # SAVE
                    # ----------------------------------------

                    design_id = save_design(
                        {
                            "design": result,
                            "image": image,

                            "mode":
                                "Guided Design",

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

                            "created_at":
                                datetime.now().strftime(
                                    "%Y-%m-%d %H:%M"
                                )
                        }
                    )

                    st.success(
                        f"💾 Design #{design_id} saved to your Design Library."
                    )

                    # ----------------------------------------
                    # TAILORING
                    # ----------------------------------------

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
5–10 working days
"""

                    st.text_area(
                        "Tailor Notes",
                        tailoring,
                        height=220,
                        key="guided_tailor_notes"
                    )

                    # ----------------------------------------
                    # COST
                    # ----------------------------------------

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

                    estimate = costs[
                        complexity
                    ]

                    total = (
                        estimate["Fabric"]
                        + estimate["Labour"]
                        + estimate["Accessories"]
                    )

                    profit = int(
                        total * 0.5
                    )

                    selling_price = (
                        total + profit
                    )

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

                    # ----------------------------------------
                    # PACKAGING
                    # ----------------------------------------

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

                    # ----------------------------------------
                    # PHOTOSHOOT
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "📸 Photoshoot Ideas"
                    )

                    st.info(
                        f"""
**Location:** Luxury hotel or professional studio.

**Theme:** {theme}

**Lighting:** Soft luxury lighting.

**Pose:** Editorial fashion pose.

**Background:** Minimal white or premium marble.
"""
                    )

                    # ----------------------------------------
                    # ADVERTISEMENT
                    # ----------------------------------------

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

                    st.code(
                        advert
                    )

                    # ----------------------------------------
                    # BRAND NAMES
                    # ----------------------------------------

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

                    for index, name in enumerate(
                        names
                    ):

                        with cols[
                            index % 2
                        ]:

                            st.success(
                                name
                            )

                    # ----------------------------------------
                    # INSIGHTS
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "📈 AI Fashion Insights"
                    )

                    insight1, insight2 = st.columns(2)

                    with insight1:

                        st.info(
                            f"""
### 🎯 Target Audience

**Age:** {age}

**Gender:** {gender}

**Region:** {country}

**Category:** {category}

**Income:** Middle to High Class

**Fashion Taste:** Premium Luxury
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

                    # ----------------------------------------
                    # COLOR PALETTE
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "🎨 Recommended Color Palette"
                    )

                    recommended = colors

                    if not recommended:

                        recommended = [
                            "Black",
                            "Gold",
                            "White",
                            "Wine",
                            "Royal Blue",
                            "Cream"
                        ]

                    palette = st.columns(
                        min(
                            6,
                            len(
                                recommended
                            )
                        )
                    )

                    for index, colour in enumerate(
                        recommended[:6]
                    ):

                        palette[
                            index
                        ].success(
                            colour
                        )

                    # ----------------------------------------
                    # CHECKLIST
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "✅ Fashion Production Checklist"
                    )

                    st.checkbox(
                        "Design Completed",
                        value=True,
                        disabled=True,
                        key="guided_check_design"
                    )

                    st.checkbox(
                        "Fabric Selected",
                        value=True,
                        disabled=True,
                        key="guided_check_fabric"
                    )

                    st.checkbox(
                        "Accessories Recommended",
                        value=accessories,
                        disabled=True,
                        key="guided_check_accessories"
                    )

                    st.checkbox(
                        "AI Sketch Generated",
                        value=image is not None,
                        disabled=True,
                        key="guided_check_image"
                    )

                    # ----------------------------------------
                    # RECOMMENDATIONS
                    # ----------------------------------------

                    st.divider()

                    st.subheader(
                        "🤖 AI Recommendations"
                    )

                    recommendations = [
                        "Increase embroidery for premium appeal.",
                        "Use luxury photography for marketing.",
                        "Offer limited-edition releases.",
                        "Target Instagram and TikTok first.",
                        "Bundle matching accessories."
                    ]

                    for recommendation in recommendations:

                        st.success(
                            recommendation
                        )

                except Exception as e:

                    st.error(
                        "Fashion design generation failed."
                    )

                    st.exception(
                        e
                    )

    # ========================================================
    # TAB 2 — PROMPT STUDIO
    # ========================================================

    with tab2:

        st.subheader(
            "✨ Prompt Studio"
        )

        st.caption(
            "Create professional fashion concepts using natural language."
        )

        # ====================================================
        # AI SETTINGS
        # ====================================================

        st.divider()

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

        st.info(
            "Higher creativity produces more artistic and experimental concepts."
        )

        st.success(
            "🟢 OpenAI Image Generation Enabled"
        )

        # ====================================================
        # EXAMPLES
        # ====================================================

        st.divider()

        st.subheader(
            "💡 Start With an Example"
        )

        prompt_examples = [

            "Create a luxurious emerald green evening gown with an asymmetric neckline, sculptural sleeves, subtle gold embroidery and a fitted silhouette. Make it elegant and sophisticated.",

            "Design a modern Nigerian agbada for a young entrepreneur using deep wine velvet, gold embroidery and a clean luxury silhouette.",

            "Create a futuristic streetwear outfit inspired by African architecture, using black technical fabric with silver details and an oversized silhouette.",

            "Design an elegant Aso Oke bridal outfit combining traditional Nigerian heritage with modern haute couture."
        ]

        example_choice = st.selectbox(
            "Example Prompts",
            [
                "Choose an example..."
            ] + prompt_examples,
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

        # ====================================================
        # DASHBOARD PROMPT
        # ====================================================

        if (
            st.session_state.get(
                "dashboard_ai_prompt"
            )
            and not st.session_state.get(
                "advanced_prompt"
            )
        ):

            st.session_state.advanced_prompt = (
                st.session_state.dashboard_ai_prompt
            )

            st.session_state.dashboard_ai_prompt = ""

        # ====================================================
        # PROMPT
        # ====================================================

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
            "Describe the garment, fabric, colour, silhouette, occasion, "
            "cultural inspiration, mood and target customer."
        )

        # ====================================================
        # OPTIONAL CONTROLS
        # ====================================================

        st.divider()

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

        # ====================================================
        # PROMPT ENHANCEMENT
        # ====================================================

        st.divider()

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

Describe:

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
- Fashion quality
- Professional presentation

Do not change the user's core idea.
Improve the idea while preserving its creative direction.
"""

                st.session_state.advanced_enhanced_prompt = (
                    enhanced_prompt
                )

                st.success(
                    "✨ Prompt enhanced successfully."
                )

        if st.session_state.advanced_enhanced_prompt:

            st.text_area(
                "📝 Enhanced Fashion Prompt",
                value=st.session_state.advanced_enhanced_prompt,
                height=260,
                key="display_enhanced_prompt"
            )

        # ====================================================
        # GENERATE
        # ====================================================

        st.divider()

        if st.button(
            "🎨 Generate AI Design",
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

        The garment must remain the primary focus.
        """

                # ====================================================
                # IMAGE GENERATION
                # ====================================================

                st.subheader(
                    "🎨 AI Fashion Visualization"
                )

                try:

                    with st.spinner(
                        "🎨 StyleSense AI is generating your fashion design..."
                    ):

                        image = generate_image(
                            image_prompt
                        )

                    if image:

                        st.success(
                            "✨ Your AI fashion design is ready!"
                        )

                        # ====================================================
                        # STORE CURRENT IMAGE
                        # ====================================================

                        st.session_state.advanced_image = image
                        st.session_state.current_image = image

                        st.image(
                            image,
                            use_container_width=True
                        )

                        # ====================================================
                        # SAVE DESIGN
                        # ====================================================

                        design_id = save_design(
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

                                "embroidery": advanced_embroidery,

                                "full_body": advanced_full_body,

                                "created_at":
                                    datetime.now().strftime(
                                        "%Y-%m-%d %H:%M"
                                    )
                            }
                        )

                        # ====================================================
                        # UPDATE SESSION STATE
                        # ====================================================

                        st.session_state.saved_designs.append(
                            {
                                "id": design_id,
                                "design": prompt,
                                "image": image,
                                "mode": "Advanced Prompt-to-Design",
                                "created_at":
                                    datetime.now().strftime(
                                        "%Y-%m-%d %H:%M"
                                    )
                            }
                        )

                        st.success(
                            f"💾 Design #{design_id} saved to your Design Library."
                        )

                except Exception as e:

                    st.error(
                        "❌ AI design generation failed."
                    )

                    st.caption(
                        str(e)
                    )

    # ========================================================
    # TAB 3 — REFERENCE DESIGN
    # ========================================================

    with tab3:

        st.subheader(
            "🖼 Reference → AI Design"
        )

        st.caption(
            "Transform a fashion inspiration, sketch, garment photo "
            "or your own image into a new AI fashion concept."
        )

        # ====================================================
        # PEXELS REFERENCE
        # ====================================================

        if studio_reference_url:

            st.success(
                "✨ Fashion Inspiration loaded."
            )

            st.image(
                studio_reference_url,
                caption=studio_reference_title,
                use_container_width=True
            )

            st.caption(
                "📸 Original inspiration by "
                + studio_reference_photographer
            )

            if st.button(
                "✕ Remove Inspiration",
                key="remove_pexels_studio_reference"
            ):

                st.session_state.studio_reference_image_url = None

                st.session_state.studio_reference_title = ""

                st.session_state.studio_reference_photographer = ""

                st.rerun()

        # ====================================================
        # UPLOAD
        # ====================================================

        reference_image = st.file_uploader(
            "Upload Your Own Reference Image",
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
                "✅ Reference image ready."
            )

            st.image(
                reference_image,
                caption="Your Uploaded Reference",
                use_container_width=True
            )

        # ====================================================
        # TRANSFORMATION PROMPT
        # ====================================================

        st.divider()

        reference_prompt = st.text_area(
            "✍️ What should StyleSense do with it?",
            height=160,
            placeholder=(
                "Example: Keep the silhouette of this dress but "
                "transform it into a luxury Nigerian evening gown. "
                "Use emerald green velvet, subtle gold embroidery, "
                "structured shoulders and a sophisticated couture finish."
            ),
            key="reference_design_prompt"
        )

        # ====================================================
        # CONTROLS
        # ====================================================

        st.divider()

        st.subheader(
            "🎯 Transformation Controls"
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

        # ====================================================
        # PREPARE REFERENCE
        # ====================================================

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

        # ====================================================
        # GENERATE
        # ====================================================

        st.divider()

        if st.button(
            "🎨 Generate From Reference",
            use_container_width=True,
            type="primary",
            key="generate_reference_design"
        ):

            if reference_source is None:

                st.warning(
                    "Please upload an image or select a Fashion Inspiration."
                )

            elif not reference_prompt.strip():

                st.warning(
                    "Please describe the transformation you want."
                )

            else:

                transformation_instructions = f"""
You are an expert fashion designer and visual director.

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

Professional presentation:
{"YES" if professional_presentation else "NO"}

The reference is an inspiration,
not a restriction.

Follow the user's transformation request carefully.

The final result should be a new professional fashion concept.

Create:

- High-end fashion design
- Accurate garment construction
- Elegant proportions
- Detailed fabric texture
- Professional styling
- Sophisticated presentation
- Luxury editorial quality
- Full garment visibility
- Clean composition
- Highly detailed result

Do not simply copy the reference.
Create a new fashion concept based on the requested transformation.
"""

                with st.spinner(
                    "🧠 StyleSense AI is transforming the reference..."
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
                            "✅ New fashion design created."
                        )

                        st.divider()

                        st.subheader(
                            "🎨 StyleSense Redesigned Concept"
                        )

                        st.image(
                            reference_result,
                            use_container_width=True
                        )

                        # ------------------------------------
                        # DOWNLOAD
                        # ------------------------------------

                        image_bytes = get_image_bytes(
                            reference_result
                        )

                        if image_bytes:

                            st.download_button(
                                "⬇️ Download Generated Design",
                                data=image_bytes,
                                file_name=(
                                    "StyleSense_Reference_Design.png"
                                ),
                                mime="image/png",
                                use_container_width=True,
                                key="download_reference_design"
                            )

                        # ------------------------------------
                        # SUMMARY
                        # ------------------------------------

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

                        # ------------------------------------
                        # SAVE
                        # ------------------------------------

                        design_id = save_design(
                            {
                                "design":
                                    reference_prompt,

                                "image":
                                    reference_result,

                                "mode":
                                    "Reference Image → Design",

                                "reference_image":
                                    True,

                                "reference_source":
                                    (
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

                                "professional_presentation":
                                    professional_presentation,

                                "created_at":
                                    datetime.now().strftime(
                                        "%Y-%m-%d %H:%M"
                                    )
                            }
                        )

                        st.success(
                            f"💾 Design #{design_id} saved to your Design Library."
                        )

                        # ------------------------------------
                        # CLEAR PEXELS REFERENCE
                        # ------------------------------------

                        st.session_state.studio_reference_image_url = None

                        st.session_state.studio_reference_title = ""

                        st.session_state.studio_reference_photographer = ""

                    except Exception as e:

                        st.error(
                            "Reference image generation failed."
                        )

                        st.exception(
                            e
                        )