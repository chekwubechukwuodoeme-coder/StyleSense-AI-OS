from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
from datetime import datetime
import threading

from ai import generate_design
from image_generator import (
    generate_image,
    generate_image_from_reference
)

from database.database import save_design_to_database
from utilis.image_utilis import image_to_bytes


# ============================================================
# BACKGROUND WORKER
# ============================================================

executor = ThreadPoolExecutor(
    max_workers=3
)

jobs = {}

jobs_lock = threading.Lock()


# ============================================================
# IMAGE BYTES
# ============================================================

def get_image_bytes(image):

    if image is None:
        return None

    try:
        return image_to_bytes(image)

    except Exception:
        pass

    if isinstance(image, bytes):
        return image

    try:

        import io

        if isinstance(image, io.BytesIO):

            image.seek(0)

            return image.read()

    except Exception:
        pass

    try:

        from PIL import Image

        if isinstance(image, Image.Image):

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
# JOB STATUS
# ============================================================

def create_job():

    job_id = str(uuid4())

    with jobs_lock:

        jobs[job_id] = {
            "status": "queued",
            "progress": "Waiting for AI...",
            "result": None,
            "error": None,
            "created_at": datetime.now()
        }

    return job_id


def update_job(
    job_id,
    **updates
):

    with jobs_lock:

        if job_id in jobs:

            jobs[job_id].update(
                updates
            )


def get_job(job_id):

    with jobs_lock:

        job = jobs.get(job_id)

        if job is None:
            return None

        return dict(job)


# ============================================================
# GUIDED DESIGN WORKER
# ============================================================

def _generate_guided_design(
    job_id,
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
):

    try:

        update_job(
            job_id,
            status="running",
            progress="🧠 Creating fashion concept..."
        )

        # ----------------------------------------------------
        # AI CONCEPT
        # ----------------------------------------------------

        concept = generate_design(
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

        update_job(
            job_id,
            progress="🎨 Creating fashion visualization..."
        )

        # ----------------------------------------------------
        # IMAGE PROMPT
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------

        image = generate_image(
            image_prompt
        )

        update_job(
            job_id,
            progress="💾 Saving design to Design Library..."
        )

        image_bytes = get_image_bytes(
            image
        )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        design_data = {

            "design": concept,

            "image_data": image_bytes,

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

            "created_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
        }

        design_id = save_design_to_database(
            design_data
        )

        # ----------------------------------------------------
        # COMPLETE
        # ----------------------------------------------------

        update_job(
            job_id,
            status="completed",
            progress="✅ Design completed.",
            result={
                "design_id": design_id,
                "concept": concept,
                "image": image
            }
        )

    except Exception as e:

        update_job(
            job_id,
            status="failed",
            progress="❌ Generation failed.",
            error=str(e)
        )


# ============================================================
# START GUIDED GENERATION
# ============================================================

def start_guided_generation(
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
):

    job_id = create_job()

    executor.submit(
        _generate_guided_design,

        job_id,

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

    return job_id