#!/usr/bin/env python3
"""
Screenshot demo - takes a screenshot and checks pixel colors.
"""

from computer_use.tools.screen import ScreenTool
from computer_use.tools.mouse import MouseTool


def main():
    print("Screenshot Demo")
    print("-" * 40)

    # Get screen size
    img = ScreenTool.screenshot()
    print(f"Screen size: {img.size[0]} x {img.size[1]}")

    # Get current mouse position
    x, y = MouseTool.position()
    print(f"Current mouse position: ({x}, {y})")

    # Get pixel color at mouse position
    if 0 <= x < img.size[0] and 0 <= y < img.size[1]:
        r, g, b = ScreenTool.pixel(x, y)
        print(f"Pixel color at ({x}, {y}): RGB({r}, {g}, {b})")
        print(f"  Hex: #{r:02x}{g:02x}{b:02x}")

    # Take and save a screenshot
    print("\nTaking screenshot (screenshot.png)...")
    ScreenTool.screenshot(filename="screenshot.png")
    print("Screenshot saved as screenshot.png")

    print("\nDemo complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo stopped by user")
