import os
from typing import Tuple

import pyautogui
from dotenv import load_dotenv


class Config:
    """Global configuration for computer use operations."""

    # Default values
    DEFAULT_PAUSE = 0.1
    DEFAULT_FAILSAFE = True
    DEFAULT_FAILSAFE_POINT = (0, 0)
    DEFAULT_MINIMUM_DURATION = 0.0
    DEFAULT_LOG_LEVEL = "INFO"

    def __init__(self):
        load_dotenv()
        self._load_config()
        self._apply_to_pyautogui()

    def _load_config(self):
        """Load configuration from environment variables."""
        self.pause = self._get_float("PAUSE", self.DEFAULT_PAUSE)
        self.failsafe = self._get_bool("FAILSAFE", self.DEFAULT_FAILSAFE)
        self.failsafe_point = self._get_tuple(
            "FAILSAFE_POINT", self.DEFAULT_FAILSAFE_POINT
        )
        self.minimum_duration = self._get_float(
            "MINIMUM_DURATION", self.DEFAULT_MINIMUM_DURATION
        )
        self.log_level = self._get_str("LOG_LEVEL", self.DEFAULT_LOG_LEVEL)

    def _apply_to_pyautogui(self):
        """Apply configuration to pyautogui."""
        pyautogui.PAUSE = self.pause
        pyautogui.FAILSAFE = self.failsafe

    def _get_str(self, key: str, default: str) -> str:
        """Get string value from environment."""
        return os.getenv(key, default)

    def _get_float(self, key: str, default: float) -> float:
        """Get float value from environment."""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            return default

    def _get_bool(self, key: str, default: bool) -> bool:
        """Get bool value from environment."""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")

    def _get_tuple(self, key: str, default: Tuple[int, int]) -> Tuple[int, int]:
        """Get tuple value from environment (format: "x,y")."""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            parts = value.split(",")
            return (int(parts[0].strip()), int(parts[1].strip()))
        except (ValueError, IndexError):
            return default

    def update(self, **kwargs):
        """Update configuration and apply to pyautogui."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self._apply_to_pyautogui()


# Global config instance
config = Config()
