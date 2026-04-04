from typing import Optional, Tuple

import pyautogui
from PIL.Image import Image

from ..core.logger import get_logger
from ..utils.validators import validate_int, validate_region

logger = get_logger(__name__)


class ScreenTool:
    """Screen operation tools."""

    @staticmethod
    def screenshot(
        filename: Optional[str] = None,
        region: Optional[Tuple[int, int, int, int]] = None,
    ) -> Image:
        """Take a screenshot.

        Args:
            filename: Save to file (optional)
            region: Region to capture (left, top, width, height) (optional)

        Returns:
            PIL Image object
        """
        if region is not None:
            region = validate_region(region)

        logger.info(f"Taking screenshot" + (f" region={region}" if region else ""))
        # pyautogui screenshot with filename may not work reliably on all platforms
        # so we take the screenshot first, then save explicitly
        img = pyautogui.screenshot(region=region)
        if filename:
            img.save(filename)
            logger.info(f"Screenshot saved to: {filename}")
        return img

    @staticmethod
    def pixel(
        x: int,
        y: int,
    ) -> Tuple[int, int, int]:
        """Get RGB color of a pixel.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Tuple of (R, G, B) values
        """
        x = validate_int(x, "x")
        y = validate_int(y, "y")

        color = pyautogui.pixel(x, y)
        logger.debug(f"Pixel color at ({x}, {y}): {color}")
        return color

    @staticmethod
    def pixel_matches_color(
        x: int,
        y: int,
        rgb_tuple: Tuple[int, int, int],
        tolerance: int = 0,
    ) -> bool:
        """Check if a pixel matches a color with optional tolerance.

        Args:
            x: X coordinate
            y: Y coordinate
            rgb_tuple: Target (R, G, B) color
            tolerance: Tolerance level (0-255)

        Returns:
            True if pixel matches color within tolerance
        """
        x = validate_int(x, "x")
        y = validate_int(y, "y")
        tolerance = validate_int(tolerance, "tolerance", min_val=0, max_val=255)

        if not isinstance(rgb_tuple, tuple) or len(rgb_tuple) != 3:
            raise ValueError("rgb_tuple must be a tuple of 3 integers")

        for i, c in enumerate(rgb_tuple):
            if not isinstance(c, int) or c < 0 or c > 255:
                raise ValueError(
                    f"rgb_tuple value at index {i} must be between 0 and 255"
                )

        result = pyautogui.pixelMatchesColor(x, y, rgb_tuple, tolerance=tolerance)
        logger.debug(
            f"Pixel at ({x}, {y}) matches {rgb_tuple} (tolerance={tolerance}): {result}"
        )
        return result
