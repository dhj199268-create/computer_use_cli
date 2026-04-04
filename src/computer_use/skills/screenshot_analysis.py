from typing import Any, Dict, Optional, Tuple

from ..core.logger import get_logger
from ..tools.screen import ScreenTool
from .base import BaseSkill

logger = get_logger(__name__)


class ScreenshotAnalysisSkill(BaseSkill):
    """Skill for taking screenshots and analyzing screen content."""

    @classmethod
    def get_description(cls) -> str:
        return "Take screenshots, get pixel colors, and analyze screen content."

    @classmethod
    def get_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "action": {
                "type": "str",
                "required": True,
                "description": "Action to perform: screenshot, pixel_color, match_color, get_size",
            },
            "output": {"type": "str", "required": False, "description": "Output file path for screenshot"},
            "region": {"type": "tuple", "required": False, "description": "Region (left, top, width, height)"},
            "x": {"type": "int", "required": False, "description": "X coordinate for pixel operations"},
            "y": {"type": "int", "required": False, "description": "Y coordinate for pixel operations"},
            "rgb": {"type": "tuple", "required": False, "description": "RGB color tuple to match"},
            "tolerance": {"type": "int", "required": False, "default": 0, "description": "Color matching tolerance"},
        }

    def execute(self, context: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        action = kwargs.get("action")

        if action == "screenshot":
            return self._screenshot(**kwargs)
        elif action == "pixel_color":
            return self._pixel_color(**kwargs)
        elif action == "match_color":
            return self._match_color(**kwargs)
        elif action == "get_size":
            return self._get_size()
        else:
            raise ValueError(f"Unknown action: {action}")

    def _screenshot(self, **kwargs) -> str:
        output = kwargs.get("output")
        region = kwargs.get("region")
        img = ScreenTool.screenshot(filename=output, region=region)
        if output:
            logger.info(f"Screenshot saved to: {output}")
            return output
        logger.info(f"Screenshot taken: {img.size}")
        return f"Screenshot: {img.size[0]}x{img.size[1]}"

    def _pixel_color(self, **kwargs) -> Tuple[int, int, int]:
        x = kwargs["x"]
        y = kwargs["y"]
        color = ScreenTool.pixel(x, y)
        logger.info(f"Pixel color at ({x}, {y}): {color}")
        return color

    def _match_color(self, **kwargs) -> bool:
        x = kwargs["x"]
        y = kwargs["y"]
        rgb = kwargs["rgb"]
        tolerance = kwargs.get("tolerance", 0)
        matches = ScreenTool.pixel_matches_color(x, y, rgb, tolerance=tolerance)
        logger.info(f"Pixel at ({x}, {y}) matches {rgb}: {matches}")
        return matches

    def _get_size(self) -> Tuple[int, int]:
        size = ScreenTool.screenshot().size
        logger.info(f"Screen size: {size}")
        return size
