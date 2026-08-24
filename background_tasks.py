import uuid
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

from database.database import (
    create_design_job,
    get_design_job,
    update_design_job,
)


# ============================================================
# BACKGROUND EXECUTOR
# ============================================================

executor = ThreadPoolExecutor(
    max_workers=3
)


# ============================================================
# TEMPORARY JOB STORAGE
# ============================================================

jobs = {}


# ============================================================
# CONVERT IMAGE RESULT TO BYTES
# ============================================================

def convert_image_to_bytes(image):

    if image is None:
        return None

    # --------------------------------------------------------
    # Already bytes
    # --------------------------------------------------------

    if isinstance(image, bytes):

        return image

    # --------------------------------------------------------
    # Bytearray
    # --------------------------------------------------------

    if isinstance(image, bytearray):

        return bytes(image)

    # --------------------------------------------------------
    # PIL Image
    # --------------------------------------------------------

    try:

        if hasattr(image, "save"):

            buffer = BytesIO()

            image.save(
                buffer,
                format="PNG"
            )

            return buffer.getvalue()

    except Exception:

        pass

    # --------------------------------------------------------
    # Streamlit / file-like objects
    # --------------------------------------------------------

    try:

        if hasattr(image, "getvalue"):

            return image.getvalue()

    except Exception:

        pass

    # --------------------------------------------------------
    # Unknown format
    # --------------------------------------------------------

    raise TypeError(
        f"Unsupported image result type: {type(image)}"
    )


# ============================================================
# BACKGROUND WORKER
# ============================================================

def _run_design_generation(
    job_id,
    image_generator,
    image_prompt
):
    """
    Actual background worker.

    This function runs outside the Streamlit UI thread.
    """

    try:

        # ----------------------------------------------------
        # Mark job as generating
        # ----------------------------------------------------

        update_design_job(
            job_id,
            "generating"
        )

        # ----------------------------------------------------
        # CALL AI IMAGE GENERATOR
        # ----------------------------------------------------

        result = image_generator(
            image_prompt
        )

        # ----------------------------------------------------
        # CONVERT IMAGE TO BYTES
        # ----------------------------------------------------

        image_data = convert_image_to_bytes(
            result
        )

        if not image_data:

            raise ValueError(
                "AI image generator returned no image data."
            )

        # ----------------------------------------------------
        # SAVE IMAGE TO DATABASE
        # ----------------------------------------------------

        update_design_job(
            job_id,
            "completed",
            image_data=image_data
        )

        # ----------------------------------------------------
        # UPDATE TEMPORARY JOB
        # ----------------------------------------------------

        if job_id in jobs:

            jobs[job_id]["status"] = "completed"

            jobs[job_id]["result"] = image_data

            jobs[job_id]["error"] = None

    except Exception as e:

        error_message = str(e)

        # ----------------------------------------------------
        # SAVE FAILURE TO DATABASE
        # ----------------------------------------------------

        try:

            update_design_job(
                job_id,
                "failed",
                error=error_message
            )

        except Exception:

            pass

        # ----------------------------------------------------
        # UPDATE TEMPORARY JOB
        # ----------------------------------------------------

        if job_id in jobs:

            jobs[job_id]["status"] = "failed"

            jobs[job_id]["result"] = None

            jobs[job_id]["error"] = error_message


# ============================================================
# START DESIGN GENERATION
# ============================================================

def start_design_generation(
    image_generator,
    image_prompt,
    user_id=None,
    job_type="advanced"
):
    """
    Start AI image generation in the background.

    The job is first stored permanently in SQLite,
    then the actual AI generation runs in the background.

    Returns:
        job_id
    """

    # --------------------------------------------------------
    # CREATE UNIQUE JOB ID
    # --------------------------------------------------------

    job_id = str(
        uuid.uuid4()
    )

    # --------------------------------------------------------
    # CREATE PERSISTENT DATABASE JOB
    # --------------------------------------------------------

    create_design_job(
        job_id=job_id,
        user_id=user_id,
        job_type=job_type,
        prompt=image_prompt
    )

    # --------------------------------------------------------
    # TEMPORARY JOB RECORD
    # --------------------------------------------------------

    jobs[job_id] = {

        "future": None,

        "status": "pending",

        "result": None,

        "error": None,
    }

    # --------------------------------------------------------
    # START BACKGROUND WORKER
    # --------------------------------------------------------

    future = executor.submit(
        _run_design_generation,
        job_id,
        image_generator,
        image_prompt
    )

    jobs[job_id]["future"] = future

    jobs[job_id]["status"] = "generating"

    return job_id


# ============================================================
# CHECK JOB STATUS
# ============================================================

def get_job_status(job_id):

    # --------------------------------------------------------
    # FIRST CHECK DATABASE
    # --------------------------------------------------------

    database_job = get_design_job(
        job_id
    )

    if database_job:

        status = database_job.get(
            "status"
        )

        # ----------------------------------------------------
        # COMPLETED
        # ----------------------------------------------------

        if status == "completed":

            return {

                "status": "completed",

                "result": database_job.get(
                    "image_data"
                ),

                "error": None,
            }

        # ----------------------------------------------------
        # FAILED
        # ----------------------------------------------------

        if status == "failed":

            return {

                "status": "failed",

                "result": None,

                "error": database_job.get(
                    "error"
                ),
            }

        # ----------------------------------------------------
        # GENERATING
        # ----------------------------------------------------

        if status in (
            "pending",
            "generating"
        ):

            return {

                "status": status,

                "result": None,

                "error": None,
            }

    # --------------------------------------------------------
    # FALLBACK TO TEMPORARY JOB STORAGE
    # --------------------------------------------------------

    job = jobs.get(
        job_id
    )

    if job is None:

        return {

            "status": "not_found",

            "result": None,

            "error": None,
        }

    future = job.get(
        "future"
    )

    # --------------------------------------------------------
    # CHECK FUTURE
    # --------------------------------------------------------

    if future is not None and future.done():

        try:

            result = future.result()

            job["status"] = "completed"

            job["result"] = result

        except Exception as e:

            job["status"] = "failed"

            job["error"] = str(e)

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "status": job.get(
            "status"
        ),

        "result": job.get(
            "result"
        ),

        "error": job.get(
            "error"
        ),
    }


# ============================================================
# REMOVE JOB
# ============================================================

def remove_job(job_id):

    jobs.pop(
        job_id,
        None
    )