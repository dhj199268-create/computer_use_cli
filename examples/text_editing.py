#!/usr/bin/env python3
"""
Text editing demo - shows keyboard operations.
"""

import time

from computer_use.tools.keyboard import KeyboardTool


def main():
    print("Text Editing Demo")
    print("-" * 40)
    print("Please focus a text editor window in 3 seconds...")

    time.sleep(3)

    # Write some text
    print("\nWriting text...")
    KeyboardTool.write("Hello from Computer Use CLI!", interval=0.05)

    time.sleep(0.5)

    # Press enter twice
    print("\nPressing enter...")
    KeyboardTool.press("enter", presses=2)

    time.sleep(0.3)

    # Write more text
    KeyboardTool.write("This is a demonstration of keyboard automation.", interval=0.03)

    time.sleep(0.5)

    # Select all
    print("\nSelecting all text...")
    KeyboardTool.select_all()

    time.sleep(0.5)

    # Copy
    print("Copying to clipboard...")
    KeyboardTool.copy()

    time.sleep(0.3)

    # Deselect and paste twice
    print("Pressing right arrow...")
    KeyboardTool.press("right")

    time.sleep(0.3)

    KeyboardTool.press("enter")

    time.sleep(0.3)

    print("Pasting...")
    KeyboardTool.paste()

    time.sleep(0.3)

    KeyboardTool.press("enter")
    KeyboardTool.paste()

    print("\nDemo complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo stopped by user")
