import base64
import io

from PIL import Image

from ai.model import ask_openai


# ============================================================
# FASHION CHAT
# ============================================================

def fashion_chat(prompt: str) -> str:
    """
    General fashion conversation using OpenAI.
    """
    return ask_openai(prompt)


# ============================================================
# DESIGNER AGENT
# ============================================================

def designer_agent(task):

    prompt = f"""
You are the Creative Director of StyleSense AI OS.

You are an award-winning luxury fashion designer.

Your ONLY responsibility is creating world-class fashion
collections.

Task:

{task}

Return beautiful Markdown.

Include:

# 👗 Design Concept

# 🎯 Target Customer

# 🎨 Color Palette

# 🧵 Recommended Fabrics

# ✂ Tailoring Details

# 💍 Accessories

# 👞 Footwear

# 💇 Hairstyle

# 🌦 Climate Suitability

# ⭐ Luxury Features

# 📸 Photoshoot Concept

Never discuss pricing.

Never discuss business.

Never discuss marketing.
"""

    return ask_openai(prompt)


# ============================================================
# GENERATE DESIGN
# ============================================================

def generate_design(
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
    creativity,
    country,
    climate,
):

    prompt = f"""
Create a luxury fashion design.

Gender: {gender}

Age: {age}

Height: {height}

Body Shape: {body_shape}

Skin Tone: {skin_tone}

Category: {category}

Fabric: {fabric}

Occasion: {occasion}

Budget: {budget}

Colors: {colors}

Complexity: {complexity}

Theme: {theme}

Embroidery: {embroidery}

Accessories: {accessories}

Creativity: {creativity}/10

Country: {country}

Climate: {climate}

Return beautiful Markdown with:

# Design Concept

# Fabrics

# Colors

# Tailoring

# Accessories

# Styling Tips
"""

    return ask_openai(prompt)


# ============================================================
# EDIT DESIGN
# ============================================================

def edit_design(current_design, instruction):

    prompt = f"""
Current Design:

{current_design}

Modify it using these instructions:

{instruction}

Return the updated version only.
"""

    return ask_openai(prompt)


# ============================================================
# OUTFIT ANALYZER
# ============================================================

def analyze_outfit(image):

    if not isinstance(image, Image.Image):
        return "Invalid image."

    try:

        # ----------------------------------------------------
        # Convert image to RGB
        # ----------------------------------------------------

        if image.mode != "RGB":
            image = image.convert("RGB")

        # ----------------------------------------------------
        # Resize very large images
        # ----------------------------------------------------

        max_size = 1600

        if max(image.size) > max_size:

            image.thumbnail(
                (max_size, max_size),
                Image.Resampling.LANCZOS
            )

        # ----------------------------------------------------
        # Convert to JPEG
        # ----------------------------------------------------

        image_bytes = io.BytesIO()

        image.save(
            image_bytes,
            format="JPEG",
            quality=90
        )

        image_bytes = image_bytes.getvalue()

        # ----------------------------------------------------
        # Convert image to Base64
        # ----------------------------------------------------

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        image_url = (
            "data:image/jpeg;base64,"
            + image_base64
        )

        # ----------------------------------------------------
        # Fashion analysis prompt
        # ----------------------------------------------------

        prompt = """
You are an expert fashion stylist, fashion designer,
and fashion image analyst for StyleSense AI OS.

Analyze the ACTUAL outfit visible in the uploaded image.

The image is already attached.

DO NOT:

- Ask the user to upload another image.
- Say that the image is missing.
- Pretend you cannot see the image.
- Invent clothing pieces that are not visible.
- Invent brands.
- Invent exact fabric compositions.
- Invent prices.

Analyze only what can reasonably be observed.

Look carefully at:

- Clothing pieces
- Silhouette
- Fit
- Proportions
- Colors
- Patterns
- Fabric appearance
- Footwear
- Accessories
- Layering
- Styling
- Overall aesthetic
- Color coordination

Return EXACTLY these sections:

# Style

Describe the overall style and aesthetic of the outfit.

# Strengths

Explain what works particularly well.

# Weaknesses

Explain what could be improved.

# Color Harmony

Analyze the color combination and coordination.

# Accessories

Analyze the visible accessories and suggest suitable
additions only when appropriate.

# Improvement Suggestions

Give practical suggestions for improving the outfit,
including fit, proportions, colors, footwear,
accessories, or styling.

Be specific and base the analysis on the actual image.
"""

        # ----------------------------------------------------
        # Send image + prompt to OpenAI
        # ----------------------------------------------------

        from ai.model import ask_openai_vision

        return ask_openai_vision(
            prompt=prompt,
            image_data=image_url
        )

    except Exception as e:

        return (
            f"❌ Outfit analysis failed: "
            f"{type(e).__name__}: {e}"
        )