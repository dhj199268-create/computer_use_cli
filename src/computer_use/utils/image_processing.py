import hashlib
from typing import Optional, Tuple

from PIL.Image import Image


def to_grayscale(
    image: Image,
) -> Image:
    """Convert an image to grayscale.

    Args:
        image: PIL Image to convert

    Returns:
        Grayscale PIL Image
    """
    return image.convert("L")


def calculate_hash(
    image: Image,
) -> str:
    """Calculate a hash for an image.

    Args:
        image: PIL Image to hash

    Returns:
        MD5 hash string of the image data
    """
    import io

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return hashlib.md5(buffer.getvalue()).hexdigest()


def resize_image(
    image: Image,
    size: Tuple[int, int],
) -> Image:
    """Resize an image.

    Args:
        image: PIL Image to resize
        size: New size as (width, height)

    Returns:
        Resized PIL Image
    """
    return image.resize(size)
