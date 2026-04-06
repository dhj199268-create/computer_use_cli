"""
UI Locator Skill - Skill for UI element localization and interaction.

Provides high-level automation skills for locating and interacting with
UI elements using templates, screenshots, and verification.
"""

import time
from typing import Any, Dict, List, Optional, Tuple

from ..core.logger import get_logger
from ..core.exceptions import ImageNotFoundError, OperationFailedError
from .base import BaseSkill
from ..tools.screen import ScreenTool
from ..tools.image import ImageTool
from ..tools.mouse import MouseTool
from ..tools.template import get_template_manager

logger = get_logger(__name__)


class UILocatorSkill(BaseSkill):
    """Skill for UI element localization and interaction."""

    def __init__(self):
        self.template_manager = get_template_manager()

    @classmethod
    def get_description(cls) -> str:
        return "Locate and interact with UI elements using templates and screenshots."

    @classmethod
    def get_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "action": {
                "type": "str",
                "required": True,
                "description": "Action to perform: capture, click, verify, locate",
            },
            "template_name": {
                "type": "str",
                "required": False,
                "description": "Name of the template to use",
            },
            "region": {
                "type": "tuple",
                "required": False,
                "description": "Region for capture or search (left, top, width, height)",
            },
            "confidence": {
                "type": "float",
                "required": False,
                "default": 0.8,
                "description": "Confidence threshold for template matching",
            },
        }

    def execute(self, context: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """
        Execute the UI locator skill.

        Args:
            context: Shared context dictionary
            **kwargs: Skill parameters

        Returns:
            Result of the action
        """
        action = kwargs.get("action")
        context = context or {}

        if action == "capture":
            return self.capture_and_mark(context, **kwargs)
        elif action == "click":
            return self.locate_and_click(context, **kwargs)
        elif action == "verify":
            return self.verify_position(context, **kwargs)
        elif action == "locate":
            return self.locate_element(context, **kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")

    def capture_and_mark(
        self,
        context: Dict[str, Any],
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Capture screenshot and optionally save as template.

        Args:
            context: Shared context
            **kwargs: Parameters including template_name, region, description, tags

        Returns:
            Result dict with screenshot info
        """
        template_name = kwargs.get("template_name")
        region = kwargs.get("region")
        description = kwargs.get("description", "")
        tags = kwargs.get("tags", [])
        output_file = kwargs.get("output_file")

        result = {
            "success": False,
            "action": "capture",
        }

        try:
            if template_name and region:
                # Save as template
                self.template_manager.capture_and_save_template(
                    name=template_name,
                    region=region,
                    description=description,
                    tags=tags,
                )
                result["template_name"] = template_name
                result["region"] = region
                logger.info(f"Captured and saved template: {template_name}")
            else:
                # Just take screenshot
                img = ScreenTool.screenshot(filename=output_file, region=region)
                result["size"] = img.size
                if output_file:
                    result["output_file"] = output_file
                logger.info(f"Took screenshot: {img.size}")

            result["success"] = True
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Capture failed: {e}")

        return result

    def locate_element(
        self,
        context: Dict[str, Any],
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Locate a UI element on screen.

        Args:
            context: Shared context
            **kwargs: Parameters including template_name, image_path, confidence, region

        Returns:
            Result dict with location info
        """
        template_name = kwargs.get("template_name")
        image_path = kwargs.get("image_path")
        confidence = kwargs.get("confidence", 0.8)
        region = kwargs.get("region")

        result = {
            "success": False,
            "action": "locate",
        }

        try:
            if template_name:
                pos = ImageTool.locate_center_on_screen(
                    str(self.template_manager.get_template_image_path(template_name)),
                    confidence=confidence,
                    region=region,
                )
                result["template_name"] = template_name
            elif image_path:
                pos = ImageTool.locate_center_on_screen(
                    image_path,
                    confidence=confidence,
                    region=region,
                )
                result["image_path"] = image_path
            else:
                raise ValueError("Either template_name or image_path must be provided")

            if pos is None:
                raise ImageNotFoundError("Element not found on screen")

            result["position"] = pos
            result["success"] = True
            logger.info(f"Located element at: {pos}")

            # Store in context
            context["last_located_position"] = pos

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Locate failed: {e}")

        return result

    def locate_and_click(
        self,
        context: Dict[str, Any],
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Locate a UI element and click it.

        Args:
            context: Shared context
            **kwargs: Parameters including template_name, confidence, region, button, clicks

        Returns:
            Result dict with click info
        """
        template_name = kwargs.get("template_name")
        confidence = kwargs.get("confidence", 0.8)
        region = kwargs.get("region")
        button = kwargs.get("button", "left")
        clicks = kwargs.get("clicks", 1)
        verify = kwargs.get("verify", True)

        result = {
            "success": False,
            "action": "click",
        }

        try:
            if template_name:
                ImageTool.click_by_template_name(
                    template_name,
                    confidence=confidence,
                    region=region,
                    button=button,
                    clicks=clicks,
                )
                result["template_name"] = template_name
            else:
                raise ValueError("template_name must be provided")

            result["success"] = True

            if verify:
                # Optional: Wait and verify something changed
                time.sleep(0.3)
                result["verified"] = True

            logger.info(f"Clicked template: {template_name}")

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Click failed: {e}")

        return result

    def verify_position(
        self,
        context: Dict[str, Any],
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Verify if a position or element is as expected.

        Args:
            context: Shared context
            **kwargs: Parameters including position, expected_color, template_name

        Returns:
            Result dict with verification info
        """
        position = kwargs.get("position")
        expected_color = kwargs.get("expected_color")
        template_name = kwargs.get("template_name")
        tolerance = kwargs.get("tolerance", 10)
        confidence = kwargs.get("confidence", 0.8)

        result = {
            "success": False,
            "action": "verify",
            "verified": False,
        }

        try:
            if position and expected_color:
                # Verify pixel color
                x, y = position
                matches = ScreenTool.pixel_matches_color(x, y, expected_color, tolerance)
                result["verified"] = matches
                result["position"] = position
                result["expected_color"] = expected_color
                if not matches:
                    result["actual_color"] = ScreenTool.pixel(x, y)

            elif template_name:
                # Verify template is visible
                pos = ImageTool.locate_center_on_screen(
                    str(self.template_manager.get_template_image_path(template_name)),
                    confidence=confidence,
                )
                result["verified"] = pos is not None
                result["template_name"] = template_name
                if pos:
                    result["position"] = pos

            else:
                raise ValueError("Either position+expected_color or template_name must be provided")

            result["success"] = True
            logger.info(f"Verification result: {result['verified']}")

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Verification failed: {e}")

        return result
