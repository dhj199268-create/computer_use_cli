from typing import Generator, Optional, Tuple, Union

import pyautogui
from PIL.Image import Image

from ..core.exceptions import ImageNotFoundError
from ..core.logger import get_logger
from ..utils.validators import validate_region

logger = get_logger(__name__)


class ImageTool:
    """Image recognition tools."""

    @staticmethod
    def locate_on_screen(
        image: Union[str, Image],
        grayscale: bool = False,
        confidence: Optional[float] = None,
        region: Optional[Tuple[int, int, int, int]] = None,
    ) -> Optional[Tuple[int, int, int, int]]:
        """Locate an image on the screen.

        Args:
            image: Path to image file or PIL Image
            grayscale: Use grayscale matching (faster)
            confidence: Confidence threshold (0.0-1.0, requires opencv-python)
            region: Search region (left, top, width, height)

        Returns:
            Tuple of (left, top, width, height) if found, None otherwise
        """
        if region is not None:
            region = validate_region(region)

        logger.info(
            f"Locating image on screen"
            + (f" region={region}" if region else "")
            + (f" confidence={confidence}" if confidence else "")
        )
        return pyautogui.locateOnScreen(
            image, grayscale=grayscale, confidence=confidence, region=region
        )

    @staticmethod
    def locate_center_on_screen(
        image: Union[str, Image],
        grayscale: bool = False,
        confidence: Optional[float] = None,
        region: Optional[Tuple[int, int, int, int]] = None,
    ) -> Optional[Tuple[int, int]]:
        """Locate the center of an image on the screen.

        Args:
            image: Path to image file or PIL Image
            grayscale: Use grayscale matching (faster)
            confidence: Confidence threshold (0.0-1.0, requires opencv-python)
            region: Search region (left, top, width, height)

        Returns:
            Tuple of (x, y) center coordinates if found, None otherwise
        """
        if region is not None:
            region = validate_region(region)

        logger.info(
            f"Locating image center on screen"
            + (f" region={region}" if region else "")
            + (f" confidence={confidence}" if confidence else "")
        )
        return pyautogui.locateCenterOnScreen(
            image, grayscale=grayscale, confidence=confidence, region=region
        )

    @staticmethod
    def locate_all_on_screen(
        image: Union[str, Image],
        grayscale: bool = False,
        confidence: Optional[float] = None,
        region: Optional[Tuple[int, int, int, int]] = None,
    ) -> Generator[Tuple[int, int, int, int], None, None]:
        """Locate all occurrences of an image on the screen.

        Args:
            image: Path to image file or PIL Image
            grayscale: Use grayscale matching (faster)
            confidence: Confidence threshold (0.0-1.0, requires opencv-python)
            region: Search region (left, top, width, height)

        Yields:
            Tuples of (left, top, width, height) for each match
        """
        if region is not None:
            region = validate_region(region)

        logger.info(
            f"Locating all images on screen"
            + (f" region={region}" if region else "")
            + (f" confidence={confidence}" if confidence else "")
        )
        return pyautogui.locateAllOnScreen(
            image, grayscale=grayscale, confidence=confidence, region=region
        )

    @staticmethod
    def locate(
        needle: Union[str, Image],
        haystack: Union[str, Image],
        grayscale: bool = False,
    ) -> Optional[Tuple[int, int, int, int]]:
        """Locate a needle image within a haystack image.

        Args:
            needle: Path to needle image or PIL Image
            haystack: Path to haystack image or PIL Image
            grayscale: Use grayscale matching (faster)

        Returns:
            Tuple of (left, top, width, height) if found, None otherwise
        """
        logger.info("Locating image in haystack")
        return pyautogui.locate(needle, haystack, grayscale=grayscale)

    @staticmethod
    def locate_all(
        needle: Union[str, Image],
        haystack: Union[str, Image],
        grayscale: bool = False,
    ) -> Generator[Tuple[int, int, int, int], None, None]:
        """Locate all occurrences of a needle image within a haystack image.

        Args:
            needle: Path to needle image or PIL Image
            haystack: Path to haystack image or PIL Image
            grayscale: Use grayscale matching (faster)

        Yields:
            Tuples of (left, top, width, height) for each match
        """
        logger.info("Locating all images in haystack")
        return pyautogui.locateAll(needle, haystack, grayscale=grayscale)

    @staticmethod
    def center(
        box_tuple: Tuple[int, int, int, int],
    ) -> Tuple[int, int]:
        """Get the center coordinates of a bounding box.

        Args:
            box_tuple: Tuple of (left, top, width, height)

        Returns:
            Tuple of (x, y) center coordinates
        """
        if not isinstance(box_tuple, tuple) or len(box_tuple) != 4:
            raise ValueError("box_tuple must be a tuple of (left, top, width, height)")

        return pyautogui.center(box_tuple)

    @staticmethod
    def click_image(
        image: Union[str, Image],
        grayscale: bool = False,
        confidence: Optional[float] = None,
        region: Optional[Tuple[int, int, int, int]] = None,
        button: str = "left",
        clicks: int = 1,
        interval: float = 0.0,
    ) -> None:
        """Locate an image on screen and click its center.

        Args:
            image: Path to image file or PIL Image
            grayscale: Use grayscale matching (faster)
            confidence: Confidence threshold (0.0-1.0, requires opencv-python)
            region: Search region (left, top, width, height)
            button: Mouse button to use
            clicks: Number of clicks
            interval: Interval between clicks

        Raises:
            ImageNotFoundError: If the image is not found on screen
        """
        from .mouse import MouseTool

        center_pos = ImageTool.locate_center_on_screen(
            image, grayscale=grayscale, confidence=confidence, region=region
        )

        if center_pos is None:
            raise ImageNotFoundError(f"Image not found on screen: {image}")

        x, y = center_pos
        MouseTool.click(x=x, y=y, button=button, clicks=clicks, interval=interval)
