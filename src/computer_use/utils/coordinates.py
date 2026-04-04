import math
from typing import Tuple

import pyautogui


def clamp_coordinate(
    x: int,
    y: int,
) -> Tuple[int, int]:
    """Clamp coordinates to be within the screen bounds.

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        Tuple of clamped (x, y) coordinates
    """
    width, height = pyautogui.size()
    clamped_x = max(0, min(x, width - 1))
    clamped_y = max(0, min(y, height - 1))
    return clamped_x, clamped_y


def normalize_coordinate(
    x: int,
    y: int,
) -> Tuple[float, float]:
    """Normalize coordinates to range [0.0, 1.0].

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        Tuple of normalized (x, y) coordinates
    """
    width, height = pyautogui.size()
    norm_x = x / width
    norm_y = y / height
    return norm_x, norm_y


def is_valid_coordinate(
    x: int,
    y: int,
) -> bool:
    """Check if coordinates are valid (within screen bounds).

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        True if coordinates are valid
    """
    return pyautogui.onScreen(x, y)


def calculate_distance(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
) -> float:
    """Calculate the Euclidean distance between two points.

    Args:
        x1: X coordinate of first point
        y1: Y coordinate of first point
        x2: X coordinate of second point
        y2: Y coordinate of second point

    Returns:
        Distance between the two points
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
