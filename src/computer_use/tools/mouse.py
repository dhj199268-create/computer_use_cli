from typing import Optional, Tuple

import pyautogui

from ..core.config import config
from ..core.exceptions import InvalidButtonError, InvalidCoordinateError
from ..core.logger import get_logger
from ..utils.validators import validate_button, validate_int

logger = get_logger(__name__)


class MouseTool:
    """Mouse operation tools."""

    # Valid mouse buttons
    VALID_BUTTONS = {"left", "right", "middle"}

    @staticmethod
    def size() -> Tuple[int, int]:
        """Get screen resolution.

        Returns:
            Tuple of (width, height)
        """
        size = pyautogui.size()
        logger.debug(f"Screen size: {size}")
        return size

    @staticmethod
    def position() -> Tuple[int, int]:
        """Get current mouse position.

        Returns:
            Tuple of (x, y) coordinates
        """
        pos = pyautogui.position()
        logger.debug(f"Mouse position: {pos}")
        return pos

    @staticmethod
    def on_screen(x: int, y: int) -> bool:
        """Check if coordinates are on screen.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if coordinates are on screen
        """
        result = pyautogui.onScreen(x, y)
        logger.debug(f"Coordinates ({x}, {y}) on screen: {result}")
        return result

    @staticmethod
    def move_to(
        x: int,
        y: int,
        duration: float = 0.0,
        tween: Optional = None,
    ) -> None:
        """Move mouse to absolute coordinates.

        Args:
            x: Target X coordinate
            y: Target Y coordinate
            duration: Duration of movement in seconds
            tween: Tweening function for movement
        """
        x = validate_int(x, "x")
        y = validate_int(y, "y")
        duration = max(duration, config.minimum_duration)

        if not MouseTool.on_screen(x, y):
            raise InvalidCoordinateError(f"Coordinates ({x}, {y}) are off-screen")

        logger.info(f"Moving mouse to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=duration, tween=tween)

    @staticmethod
    def move(
        x_offset: int,
        y_offset: int,
        duration: float = 0.0,
        tween: Optional = None,
    ) -> None:
        """Move mouse relative to current position.

        Args:
            x_offset: X offset from current position
            y_offset: Y offset from current position
            duration: Duration of movement in seconds
            tween: Tweening function for movement
        """
        x_offset = validate_int(x_offset, "x_offset")
        y_offset = validate_int(y_offset, "y_offset")
        duration = max(duration, config.minimum_duration)

        logger.info(f"Moving mouse by ({x_offset}, {y_offset})")
        pyautogui.move(x_offset, y_offset, duration=duration, tween=tween)

    @staticmethod
    def drag_to(
        x: int,
        y: int,
        duration: float = 0.0,
        tween: Optional = None,
        button: str = "left",
    ) -> None:
        """Drag mouse to absolute coordinates.

        Args:
            x: Target X coordinate
            y: Target Y coordinate
            duration: Duration of movement in seconds
            tween: Tweening function for movement
            button: Mouse button to use ('left', 'right', 'middle')
        """
        x = validate_int(x, "x")
        y = validate_int(y, "y")
        button = validate_button(button, MouseTool.VALID_BUTTONS)
        duration = max(duration, config.minimum_duration)

        if not MouseTool.on_screen(x, y):
            raise InvalidCoordinateError(f"Coordinates ({x}, {y}) are off-screen")

        logger.info(f"Dragging to ({x}, {y}) with {button} button")
        pyautogui.dragTo(x, y, duration=duration, tween=tween, button=button)

    @staticmethod
    def drag(
        x_offset: int,
        y_offset: int,
        duration: float = 0.0,
        tween: Optional = None,
        button: str = "left",
    ) -> None:
        """Drag mouse relative to current position.

        Args:
            x_offset: X offset from current position
            y_offset: Y offset from current position
            duration: Duration of movement in seconds
            tween: Tweening function for movement
            button: Mouse button to use ('left', 'right', 'middle')
        """
        x_offset = validate_int(x_offset, "x_offset")
        y_offset = validate_int(y_offset, "y_offset")
        button = validate_button(button, MouseTool.VALID_BUTTONS)
        duration = max(duration, config.minimum_duration)

        logger.info(f"Dragging by ({x_offset}, {y_offset}) with {button} button")
        pyautogui.drag(x_offset, y_offset, duration=duration, tween=tween, button=button)

    @staticmethod
    def click(
        x: Optional[int] = None,
        y: Optional[int] = None,
        button: str = "left",
        clicks: int = 1,
        interval: float = 0.0,
    ) -> None:
        """Click mouse at specified or current position.

        Args:
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
            button: Mouse button to use ('left', 'right', 'middle')
            clicks: Number of clicks
            interval: Interval between clicks in seconds
        """
        if x is not None:
            x = validate_int(x, "x")
        if y is not None:
            y = validate_int(y, "y")
        button = validate_button(button, MouseTool.VALID_BUTTONS)
        clicks = validate_int(clicks, "clicks", min_val=1)

        if x is not None and y is not None and not MouseTool.on_screen(x, y):
            raise InvalidCoordinateError(f"Coordinates ({x}, {y}) are off-screen")

        logger.info(f"Clicking {clicks} times with {button} button at ({x}, {y})")
        pyautogui.click(
            x=x, y=y, button=button, clicks=clicks, interval=interval
        )

    @staticmethod
    def double_click(
        x: Optional[int] = None,
        y: Optional[int] = None,
        button: str = "left",
        interval: float = 0.0,
    ) -> None:
        """Double-click mouse at specified or current position.

        Args:
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
            button: Mouse button to use ('left', 'right', 'middle')
            interval: Interval between clicks in seconds
        """
        if x is not None:
            x = validate_int(x, "x")
        if y is not None:
            y = validate_int(y, "y")
        button = validate_button(button, MouseTool.VALID_BUTTONS)

        if x is not None and y is not None and not MouseTool.on_screen(x, y):
            raise InvalidCoordinateError(f"Coordinates ({x}, {y}) are off-screen")

        logger.info(f"Double-clicking with {button} button at ({x}, {y})")
        pyautogui.doubleClick(x=x, y=y, button=button, interval=interval)

    @staticmethod
    def triple_click(
        x: Optional[int] = None,
        y: Optional[int] = None,
        button: str = "left",
        interval: float = 0.0,
    ) -> None:
        """Triple-click mouse at specified or current position.

        Args:
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
            button: Mouse button to use ('left', 'right', 'middle')
            interval: Interval between clicks in seconds
        """
        if x is not None:
            x = validate_int(x, "x")
        if y is not None:
            y = validate_int(y, "y")
        button = validate_button(button, MouseTool.VALID_BUTTONS)

        if x is not None and y is not None and not MouseTool.on_screen(x, y):
            raise InvalidCoordinateError(f"Coordinates ({x}, {y}) are off-screen")

        logger.info(f"Triple-clicking with {button} button at ({x}, {y})")
        pyautogui.tripleClick(x=x, y=y, button=button, interval=interval)

    @staticmethod
    def right_click(
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> None:
        """Right-click mouse at specified or current position.

        Args:
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
        """
        if x is not None:
            x = validate_int(x, "x")
        if y is not None:
            y = validate_int(y, "y")

        if x is not None and y is not None and not MouseTool.on_screen(x, y):
            raise InvalidCoordinateError(f"Coordinates ({x}, {y}) are off-screen")

        logger.info(f"Right-clicking at ({x}, {y})")
        pyautogui.rightClick(x=x, y=y)

    @staticmethod
    def mouse_down(
        x: Optional[int] = None,
        y: Optional[int] = None,
        button: str = "left",
    ) -> None:
        """Press and hold mouse button.

        Args:
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
            button: Mouse button to use ('left', 'right', 'middle')
        """
        if x is not None:
            x = validate_int(x, "x")
        if y is not None:
            y = validate_int(y, "y")
        button = validate_button(button, MouseTool.VALID_BUTTONS)

        if x is not None and y is not None and not MouseTool.on_screen(x, y):
            raise InvalidCoordinateError(f"Coordinates ({x}, {y}) are off-screen")

        logger.info(f"Pressing {button} mouse button at ({x}, {y})")
        pyautogui.mouseDown(x=x, y=y, button=button)

    @staticmethod
    def mouse_up(
        x: Optional[int] = None,
        y: Optional[int] = None,
        button: str = "left",
    ) -> None:
        """Release mouse button.

        Args:
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
            button: Mouse button to use ('left', 'right', 'middle')
        """
        if x is not None:
            x = validate_int(x, "x")
        if y is not None:
            y = validate_int(y, "y")
        button = validate_button(button, MouseTool.VALID_BUTTONS)

        if x is not None and y is not None and not MouseTool.on_screen(x, y):
            raise InvalidCoordinateError(f"Coordinates ({x}, {y}) are off-screen")

        logger.info(f"Releasing {button} mouse button at ({x}, {y})")
        pyautogui.mouseUp(x=x, y=y, button=button)

    @staticmethod
    def scroll(
        clicks: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> None:
        """Scroll vertically.

        Args:
            clicks: Number of clicks to scroll (positive = up, negative = down)
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
        """
        clicks = validate_int(clicks, "clicks")
        if x is not None:
            x = validate_int(x, "x")
        if y is not None:
            y = validate_int(y, "y")

        if x is not None and y is not None and not MouseTool.on_screen(x, y):
            raise InvalidCoordinateError(f"Coordinates ({x}, {y}) are off-screen")

        logger.info(f"Scrolling {clicks} clicks at ({x}, {y})")
        pyautogui.scroll(clicks, x=x, y=y)

    @staticmethod
    def hscroll(
        clicks: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> None:
        """Scroll horizontally.

        Args:
            clicks: Number of clicks to scroll (positive = right, negative = left)
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
        """
        clicks = validate_int(clicks, "clicks")
        if x is not None:
            x = validate_int(x, "x")
        if y is not None:
            y = validate_int(y, "y")

        if x is not None and y is not None and not MouseTool.on_screen(x, y):
            raise InvalidCoordinateError(f"Coordinates ({x}, {y}) are off-screen")

        logger.info(f"Scrolling horizontally {clicks} clicks at ({x}, {y})")
        pyautogui.hscroll(clicks, x=x, y=y)

    @staticmethod
    def vscroll(
        clicks: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> None:
        """Scroll vertically (alias for scroll).

        Args:
            clicks: Number of clicks to scroll (positive = up, negative = down)
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
        """
        MouseTool.scroll(clicks, x=x, y=y)
