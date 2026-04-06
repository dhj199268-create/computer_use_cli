from typing import Optional, Tuple, List, Union

import pyautogui
from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont
from PIL.Image import Image

from ..core.logger import get_logger
from ..core.exceptions import OperationFailedError
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

    @staticmethod
    def get_size() -> Tuple[int, int]:
        """Get screen size.

        Returns:
            Tuple of (width, height)
        """
        size = pyautogui.size()
        logger.debug(f"Screen size: {size}")
        return size

    @staticmethod
    def screenshot_with_regions(
        filename: Optional[str] = None,
        region: Optional[Tuple[int, int, int, int]] = None,
        boxes: Optional[List[Tuple[int, int, int, int, str]]] = None,
        points: Optional[List[Tuple[int, int, str]]] = None,
        box_color: str = "red",
        point_color: str = "blue",
    ) -> Image:
        """Take a screenshot and draw regions/points on it.

        Args:
            filename: Save to file (optional)
            region: Region to capture (left, top, width, height) (optional)
            boxes: List of boxes to draw: (left, top, width, height, label)
            points: List of points to draw: (x, y, label)
            box_color: Color for boxes (name or hex)
            point_color: Color for points (name or hex)

        Returns:
            PIL Image object with annotations
        """
        if region is not None:
            region = validate_region(region)

        # Take base screenshot
        img = pyautogui.screenshot(region=region)

        # Convert to RGB for drawing
        if img.mode != "RGB":
            img = img.convert("RGB")

        draw = ImageDraw.Draw(img)

        # Adjust coordinates if region was captured
        offset_x = region[0] if region else 0
        offset_y = region[1] if region else 0

        # Draw boxes
        if boxes:
            for box in boxes:
                if len(box) < 4:
                    continue
                left, top, width, height = box[0], box[1], box[2], box[3]
                label = box[4] if len(box) > 4 else ""

                # Adjust for region offset
                left -= offset_x
                top -= offset_y

                draw.rectangle(
                    [(left, top), (left + width, top + height)],
                    outline=box_color,
                    width=3
                )

                if label:
                    # Try to draw text
                    try:
                        font = ImageFont.load_default()
                        draw.text((left, top - 15), label, fill=box_color, font=font)
                    except Exception:
                        pass

        # Draw points
        if points:
            for point in points:
                if len(point) < 2:
                    continue
                x, y = point[0], point[1]
                label = point[2] if len(point) > 2 else ""

                # Adjust for region offset
                x -= offset_x
                y -= offset_y

                # Draw crosshair
                size = 10
                draw.line([(x - size, y), (x + size, y)], fill=point_color, width=2)
                draw.line([(x, y - size), (x, y + size)], fill=point_color, width=2)
                draw.ellipse([(x - 3, y - 3), (x + 3, y + 3)], fill=point_color)

                if label:
                    try:
                        font = ImageFont.load_default()
                        draw.text((x + 10, y), label, fill=point_color, font=font)
                    except Exception:
                        pass

        if filename:
            img.save(filename)
            logger.info(f"Annotated screenshot saved to: {filename}")

        return img

    @staticmethod
    def capture_ui_element(
        name: str,
        region: Tuple[int, int, int, int],
        description: str = "",
        tags: Optional[List[str]] = None,
    ) -> None:
        """Capture a UI element and save as a template.

        Args:
            name: Name for the template
            region: Region to capture (left, top, width, height)
            description: Description of the UI element
            tags: List of tags for categorization

        Raises:
            OperationFailedError: If template saving fails
        """
        try:
            from .template import get_template_manager
            template_manager = get_template_manager()
            template_manager.capture_and_save_template(
                name=name,
                region=region,
                description=description,
                tags=tags,
            )
        except ImportError:
            raise OperationFailedError("TemplateManager not available")
        except Exception as e:
            raise OperationFailedError(f"Failed to capture UI element: {e}")
