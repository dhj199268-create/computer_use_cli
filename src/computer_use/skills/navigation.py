from typing import Any, Dict, Optional, Tuple

from ..core.exceptions import ImageNotFoundError
from ..core.logger import get_logger
from ..tools.image import ImageTool
from ..tools.mouse import MouseTool
from .base import BaseSkill

logger = get_logger(__name__)


class NavigationSkill(BaseSkill):
    """Skill for navigating the screen: moving, clicking, scrolling, finding images."""

    @classmethod
    def get_description(cls) -> str:
        return "Navigate the screen, move mouse, click on elements, and scroll."

    @classmethod
    def get_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "action": {
                "type": "str",
                "required": True,
                "description": "Action to perform: move_to, move, click, click_image, scroll, find_image",
            },
            "x": {"type": "int", "required": False, "description": "X coordinate"},
            "y": {"type": "int", "required": False, "description": "Y coordinate"},
            "x_offset": {"type": "int", "required": False, "description": "X offset for relative move"},
            "y_offset": {"type": "int", "required": False, "description": "Y offset for relative move"},
            "image_path": {"type": "str", "required": False, "description": "Path to image for click_image/find_image"},
            "confidence": {"type": "float", "required": False, "default": 0.8, "description": "Confidence threshold for image matching"},
            "clicks": {"type": "int", "required": False, "default": 1, "description": "Number of clicks"},
            "scroll_clicks": {"type": "int", "required": False, "description": "Number of scroll clicks"},
            "duration": {"type": "float", "required": False, "default": 0.0, "description": "Movement duration"},
        }

    def execute(self, context: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        action = kwargs.get("action")

        if action == "move_to":
            return self._move_to(**kwargs)
        elif action == "move":
            return self._move(**kwargs)
        elif action == "click":
            return self._click(**kwargs)
        elif action == "click_image":
            return self._click_image(**kwargs)
        elif action == "scroll":
            return self._scroll(**kwargs)
        elif action == "find_image":
            return self._find_image(**kwargs)
        elif action == "get_position":
            return self._get_position()
        elif action == "get_size":
            return self._get_size()
        else:
            raise ValueError(f"Unknown action: {action}")

    def _move_to(self, **kwargs) -> None:
        x = kwargs["x"]
        y = kwargs["y"]
        duration = kwargs.get("duration", 0.0)
        MouseTool.move_to(x, y, duration=duration)
        logger.info(f"Moved to ({x}, {y})")

    def _move(self, **kwargs) -> None:
        x_offset = kwargs["x_offset"]
        y_offset = kwargs["y_offset"]
        duration = kwargs.get("duration", 0.0)
        MouseTool.move(x_offset, y_offset, duration=duration)
        logger.info(f"Moved by ({x_offset}, {y_offset})")

    def _click(self, **kwargs) -> None:
        x = kwargs.get("x")
        y = kwargs.get("y")
        button = kwargs.get("button", "left")
        clicks = kwargs.get("clicks", 1)
        MouseTool.click(x=x, y=y, button=button, clicks=clicks)
        logger.info(f"Clicked {clicks} times with {button} button")

    def _click_image(self, **kwargs) -> None:
        image_path = kwargs["image_path"]
        confidence = kwargs.get("confidence", 0.8)
        button = kwargs.get("button", "left")
        clicks = kwargs.get("clicks", 1)

        ImageTool.click_image(
            image_path, confidence=confidence, button=button, clicks=clicks
        )
        logger.info(f"Clicked on image: {image_path}")

    def _scroll(self, **kwargs) -> Tuple[int, int]:
        clicks = kwargs["scroll_clicks"]
        x = kwargs.get("x")
        y = kwargs.get("y")
        MouseTool.scroll(clicks, x=x, y=y)
        logger.info(f"Scrolled {clicks} clicks")
        return MouseTool.position()

    def _find_image(self, **kwargs) -> Optional[Tuple[int, int]]:
        image_path = kwargs["image_path"]
        confidence = kwargs.get("confidence", 0.8)
        center = ImageTool.locate_center_on_screen(image_path, confidence=confidence)
        if center:
            logger.info(f"Found image at: {center}")
        else:
            logger.info(f"Image not found: {image_path}")
        return center

    def _get_position(self) -> Tuple[int, int]:
        return MouseTool.position()

    def _get_size(self) -> Tuple[int, int]:
        return MouseTool.size()
