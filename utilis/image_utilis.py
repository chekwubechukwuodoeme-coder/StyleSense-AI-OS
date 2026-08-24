import io
from pathlib import Path

from PIL import Image


def image_to_bytes(image):
    """
    Convert an image into PNG bytes.

    Supports:
    - bytes
    - bytearray
    - PIL Image
    - file paths
    - Streamlit UploadedFile
    """

    if image is None:
        return None

    # Already bytes
    if isinstance(image, bytes):
        return image

    # Bytearray
    if isinstance(image, bytearray):
        return bytes(image)

    # PIL Image
    if isinstance(image, Image.Image):

        buffer = io.BytesIO()

        image.convert("RGB").save(
            buffer,
            format="PNG"
        )

        buffer.seek(0)

        return buffer.getvalue()

    # Streamlit UploadedFile / file-like object
    if hasattr(image, "read"):

        try:
            image.seek(0)
        except Exception:
            pass

        try:
            data = image.read()

            if data:
                return data

        except Exception:
            pass

    # File path
    if isinstance(image, (str, Path)):

        path = Path(image)

        if path.exists() and path.is_file():
            return path.read_bytes()

    return None