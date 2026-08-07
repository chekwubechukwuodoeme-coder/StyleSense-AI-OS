from PIL import Image

from ai.model import ask_gemini


def fashion_chat(prompt: str) -> str:
    return ask_gemini(prompt)


def designer_agent(task):

    prompt = f"""
You are the Creative Director of StyleSense AI OS.

You are an award-winning luxury fashion designer.

Your ONLY responsibility is creating world-class fashion collections.

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

    return ask_gemini(prompt)


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

    return ask_gemini(prompt)


def edit_design(current_design, instruction):

    prompt = f"""
Current Design:

{current_design}

Modify it using these instructions:

{instruction}

Return the updated version only.
"""

    return ask_gemini(prompt)


def analyze_outfit(image):

    if isinstance(image, Image.Image):
        prompt = """
Analyze this outfit.

Return:

# Style

# Strengths

# Weaknesses

# Color Harmony

# Accessories

# Improvement Suggestions
"""

        return ask_gemini(prompt)

    return "Invalid image."