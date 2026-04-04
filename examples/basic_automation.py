#!/usr/bin/env python3
"""
Basic automation example - moves mouse and clicks.
"""

import time

from computer_use.tools.mouse import MouseTool
from computer_use.tools.keyboard import KeyboardTool


def main():
    print("Basic Automation Demo")
    print("-" * 40)

    # Get screen size
    width, height = MouseTool.size()
    print(f"Screen size: {width} x {height}")

    # Get current position
    x, y = MouseTool.position()
    print(f"Current mouse position: ({x}, {y})")

    # Move to center of screen
    center_x = width // 2
    center_y = height // 2
    print(f"Moving mouse to center ({center_x}, {center_y})...")
    MouseTool.move_to(center_x, center_y, duration=1.0)

    time.sleep(0.5)

    # Move in a square pattern
    print("Moving in a square pattern...")
    offset = 100
    moves = [
        (offset, 0),
        (0, offset),
        (-offset, 0),
        (0, -offset),
    ]

    for dx, dy in moves:
        MouseTool.move(dx, dy, duration=0.5)
        time.sleep(0.2)

    print("Demo complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo stopped by user")
