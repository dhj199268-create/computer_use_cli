---
name: computer-use
description: |
  Control the computer through mouse, keyboard, and screen operations using the computer-use CLI tool.
  Use this skill whenever the user asks to control the mouse, type text, press keys, take screenshots,
  or perform any computer automation task. This includes: moving the cursor, clicking, typing,
  using keyboard shortcuts, capturing the screen, and other GUI interactions.
---

# Computer Use Skill

This skill enables you to control the computer through mouse, keyboard, and screen operations using the `computer-use` CLI tool.

## Quick Start

First, verify the tool is available:

```bash
computer-use --help
```

## Command Groups

The CLI provides four main command groups:

### 1. Mouse Operations

```bash
# Get current mouse position
computer-use mouse position

# Get screen size
computer-use mouse size

# Move mouse to absolute coordinates (x, y)
computer-use mouse move-to --x 100 --y 100

# Move mouse relative to current position
computer-use mouse move --x-offset 50 --y-offset -20

# Click at current position or specific coordinates
computer-use mouse click
computer-use mouse click --x 200 --y 300
computer-use mouse click --button right
computer-use mouse click --clicks 2

# Shortcut commands
computer-use mouse double-click
computer-use mouse right-click

# Scroll (positive = up, negative = down)
computer-use mouse scroll --clicks 5
computer-use mouse scroll --clicks -3

# Drag mouse to coordinates
computer-use mouse drag-to --x 500 --y 400
```

### 2. Keyboard Operations

```bash
# Write text
computer-use keyboard write --text "Hello, World!"
computer-use keyboard write --text "Hello" --interval 0.1

# Press single or multiple keys (keys are positional arguments)
computer-use keyboard press enter
computer-use keyboard press shift a

# Press hotkey combinations
computer-use keyboard hotkey cmd c
computer-use keyboard hotkey ctrl v
computer-use keyboard hotkey cmd shift 4

# Convenience commands
computer-use keyboard copy
computer-use keyboard paste
computer-use keyboard cut
computer-use keyboard undo
computer-use keyboard select-all

# List all available keys
computer-use keyboard list-keys
```

### 3. Screen Operations

```bash
# Get screen size
computer-use screen size

# Take screenshot (saved to screenshot.png by default)
computer-use screen screenshot
computer-use screen screenshot --output myscreen.png

# Take screenshot of a region (left, top, width, height)
computer-use screen screenshot --region 0 0 800 600

# Get pixel color at coordinates
computer-use screen pixel --x 100 --y 100
```

### 4. Skill Operations

```bash
# List available automation skills
computer-use skill list

# Show details of a specific skill
computer-use skill show --name automation
```

## Python API Usage

You can also use the Python API directly:

```python
from computer_use.tools.mouse import MouseTool
from computer_use.tools.keyboard import KeyboardTool
from computer_use.tools.screen import ScreenTool

# Mouse operations
MouseTool.move_to(100, 100, duration=0.5)
MouseTool.click(button="left", clicks=1)
MouseTool.scroll(clicks=5)

# Keyboard operations
KeyboardTool.write("Hello from Python!", interval=0.05)
KeyboardTool.hotkey("ctrl", "c")
KeyboardTool.press("enter")

# Screen operations
size = ScreenTool.get_size()
screenshot = ScreenTool.screenshot(output_file="screen.png")
color = ScreenTool.get_pixel_color(100, 100)
```

## Safety Features

- **Fail-Safe Mode**: Move mouse to top-left corner (0, 0) to abort all operations (enabled by default)
- **Input Validation**: All parameters are validated before execution
- **Coordinate Checking**: Ensures operations stay within screen bounds

## Best Practices

1. **Always check screen size first** when working with absolute coordinates
2. **Add small delays** between operations for reliability (configured via PAUSE env var)
3. **Use relative movements** when possible for more flexible automation
4. **Test coordinates** with `mouse position` before clicking
5. **Use hotkeys** instead of typing menu navigation when possible

## Configuration

The tool can be configured via environment variables (copy `.env.example` to `.env`):

- `PAUSE`: Delay between operations in seconds (default: 0.1)
- `FAILSAFE`: Enable fail-safe mode (default: true)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

## Common Workflows

### Opening an Application and Typing

```bash
# Open Spotlight (macOS)
computer-use keyboard hotkey cmd space
# Wait a moment
# Type application name
computer-use keyboard write --text "TextEdit"
computer-use keyboard press enter
# Wait for app to open
# Type some text
computer-use keyboard write --text "Hello from computer-use!"
```

### Taking a Screenshot of a Region

```bash
# Get mouse position for top-left
computer-use mouse position
# Move to top-left and note coordinates
# Get mouse position for bottom-right
computer-use mouse position
# Calculate width and height, then capture
computer-use screen screenshot --region 100 100 800 600 --output region.png
```

### Copy-Paste Workflow

```bash
# Select all
computer-use keyboard select-all
# Copy
computer-use keyboard copy
# Click to new location
computer-use mouse click --x 500 --y 500
# Paste
computer-use keyboard paste
```

## Troubleshooting

If commands don't work as expected:

1. Check that the package is installed in editable mode: `pip install -e .`
2. Verify the environment: `cp .env.example .env`
3. Check log output for errors
4. On macOS, ensure Terminal has accessibility permissions
5. Try simpler commands first to verify basic functionality
