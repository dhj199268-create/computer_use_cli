from contextlib import contextmanager
from typing import List, Optional, Union

import pyautogui

from ..core.exceptions import InvalidKeyError
from ..core.logger import get_logger
from ..utils.validators import validate_float, validate_int

logger = get_logger(__name__)


class KeyboardTool:
    """Keyboard operation tools."""

    # All valid keyboard keys from pyautogui
    KEYBOARD_KEYS = pyautogui.KEY_NAMES

    @staticmethod
    def write(
        text: str,
        interval: float = 0.0,
    ) -> None:
        """Type out a string of text.

        Args:
            text: Text to type
            interval: Interval between keystrokes in seconds
        """
        interval = validate_float(interval, "interval", min_val=0.0)

        logger.info(f"Writing text: {text[:50]}{'...' if len(text) > 50 else ''}")
        pyautogui.write(text, interval=interval)

    @staticmethod
    def press(
        keys: Union[str, List[str]],
        presses: int = 1,
        interval: float = 0.0,
    ) -> None:
        """Press and release a key or multiple keys.

        Args:
            keys: Key or list of keys to press
            presses: Number of times to press
            interval: Interval between presses in seconds
        """
        presses = validate_int(presses, "presses", min_val=1)
        interval = validate_float(interval, "interval", min_val=0.0)

        if isinstance(keys, str):
            key_list = [keys]
        else:
            key_list = keys

        for key in key_list:
            if key not in KeyboardTool.KEYBOARD_KEYS:
                raise InvalidKeyError(f"Invalid key: {key}")

        logger.info(f"Pressing keys: {key_list} {presses} times")
        pyautogui.press(keys, presses=presses, interval=interval)

    @staticmethod
    def key_down(
        key: str,
    ) -> None:
        """Press and hold a key.

        Args:
            key: Key to press
        """
        if key not in KeyboardTool.KEYBOARD_KEYS:
            raise InvalidKeyError(f"Invalid key: {key}")

        logger.info(f"Holding down key: {key}")
        pyautogui.keyDown(key)

    @staticmethod
    def key_up(
        key: str,
    ) -> None:
        """Release a key.

        Args:
            key: Key to release
        """
        if key not in KeyboardTool.KEYBOARD_KEYS:
            raise InvalidKeyError(f"Invalid key: {key}")

        logger.info(f"Releasing key: {key}")
        pyautogui.keyUp(key)

    @staticmethod
    @contextmanager
    def hold(
        keys: Union[str, List[str]],
    ):
        """Context manager to hold keys during a block.

        Args:
            keys: Key or list of keys to hold

        Example:
            with KeyboardTool.hold('ctrl'):
                KeyboardTool.press('c')
        """
        if isinstance(keys, str):
            key_list = [keys]
        else:
            key_list = keys

        for key in key_list:
            if key not in KeyboardTool.KEYBOARD_KEYS:
                raise InvalidKeyError(f"Invalid key: {key}")
            KeyboardTool.key_down(key)

        try:
            yield
        finally:
            for key in reversed(key_list):
                KeyboardTool.key_up(key)

    @staticmethod
    def hotkey(
        *keys: str,
        interval: float = 0.0,
    ) -> None:
        """Press a hotkey combination.

        Args:
            *keys: Keys to press in sequence (held down until last key)
            interval: Interval between key presses in seconds

        Example:
            KeyboardTool.hotkey('ctrl', 'c')
            KeyboardTool.hotkey('cmd', 'shift', '4')
        """
        interval = validate_float(interval, "interval", min_val=0.0)

        for key in keys:
            if key not in KeyboardTool.KEYBOARD_KEYS:
                raise InvalidKeyError(f"Invalid key: {key}")

        logger.info(f"Pressing hotkey: {'+'.join(keys)}")
        pyautogui.hotkey(*keys, interval=interval)

    @staticmethod
    def copy() -> None:
        """Copy selected text (Ctrl+C or Cmd+C)."""
        import platform

        if platform.system() == "Darwin":
            KeyboardTool.hotkey("command", "c")
        else:
            KeyboardTool.hotkey("ctrl", "c")

    @staticmethod
    def paste() -> None:
        """Paste clipboard text (Ctrl+V or Cmd+V)."""
        import platform

        if platform.system() == "Darwin":
            KeyboardTool.hotkey("command", "v")
        else:
            KeyboardTool.hotkey("ctrl", "v")

    @staticmethod
    def cut() -> None:
        """Cut selected text (Ctrl+X or Cmd+X)."""
        import platform

        if platform.system() == "Darwin":
            KeyboardTool.hotkey("command", "x")
        else:
            KeyboardTool.hotkey("ctrl", "x")

    @staticmethod
    def undo() -> None:
        """Undo (Ctrl+Z or Cmd+Z)."""
        import platform

        if platform.system() == "Darwin":
            KeyboardTool.hotkey("command", "z")
        else:
            KeyboardTool.hotkey("ctrl", "z")

    @staticmethod
    def select_all() -> None:
        """Select all (Ctrl+A or Cmd+A)."""
        import platform

        if platform.system() == "Darwin":
            KeyboardTool.hotkey("command", "a")
        else:
            KeyboardTool.hotkey("ctrl", "a")
