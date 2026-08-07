def create_image_prompt(
    gender,
    complexity,
    category,
    fabric,
    theme,
    occasion,
    colors,
    body_shape,
    skin_tone
):

    return f"""
A professional fashion illustration of a {gender}
wearing a {complexity.lower()} {category.lower()}
made from {fabric}.

Theme: {theme}

Occasion: {occasion}

Preferred colors:
{", ".join(colors) if colors else "designer's choice"}

Body shape:
{body_shape}

Skin tone:
{skin_tone}

Luxury fashion sketch.

Full body.

Front view.

White background.

Highly detailed.

Professional fashion illustration.

Tailor concept art.
"""