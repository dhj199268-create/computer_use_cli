---
name: computer-use
description: |
  Control the computer through mouse, keyboard, screen operations, and UI template management using the computer-use CLI tool.
  Use this skill whenever the user asks to control the mouse, type text, press keys, take screenshots, manage UI templates,
  locate UI elements by image, or perform any computer automation task. This includes: moving the cursor, clicking, typing,
  using keyboard shortcuts, capturing the screen with annotations, saving and managing UI element templates, clicking by template name,
  and other GUI interactions. Make sure to use this skill for any computer automation, UI interaction, screen capture, or template management task.
---

# Computer Use Skill

This skill enables you to control the computer through mouse, keyboard, screen operations, and UI template management using the `computer-use` CLI tool.

## Quick Start

First, verify the tool is available:

```bash
computer-use --help
```

## Command Groups

The CLI provides five main command groups:

### 1. Mouse Operations

```bash
# Get current mouse position
computer-use mouse position

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

# Take screenshot with annotations (boxes and points)
computer-use screen screenshot --output annotated.png \
  --box 100 100 80 30 "Search Button" \
  --box 200 200 100 40 "Submit Button" \
  --point 150 150 "Click Here"

# Get pixel color at coordinates
computer-use screen pixel --x 100 --y 100
```

### 4. Template Operations (NEW!)

```bash
# List all available templates
computer-use template list

# Show details of a specific template
computer-use template show search_button

# Capture a screen region and save as template
computer-use template save --name search_button --region 100 100 80 30 \
  --description "Search button in top navigation" \
  --tag ui --tag button --tag navigation

# Update template metadata
computer-use template update search_button --description "New description" --tag ui --tag important

# Locate a template on screen and click it
computer-use template click search_button --confidence 0.8
computer-use template click search_button --region 0 0 1920 1080 --button left --clicks 1

# Delete a template
computer-use template delete old_button
```

### 5. Skill Operations

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
from computer_use.tools.image import ImageTool
from computer_use.tools.template import get_template_manager, TemplateManager

# Mouse operations
MouseTool.move_to(100, 100, duration=0.5)
MouseTool.click(button="left", clicks=1)
MouseTool.scroll(clicks=5)

# Keyboard operations
KeyboardTool.write("Hello from Python!", interval=0.05)
KeyboardTool.hotkey("ctrl", "c")
KeyboardTool.press("enter")

# Screen operations (enhanced!)
width, height = ScreenTool.get_size()
screenshot = ScreenTool.screenshot(filename="screen.png")

# Screenshot with annotations
annotated = ScreenTool.screenshot_with_regions(
    filename="annotated.png",
    boxes=[(100, 100, 80, 30, "Search Button")],
    points=[(150, 150, "Click Here")],
    box_color="red",
    point_color="blue"
)

# Capture UI element as template
ScreenTool.capture_ui_element(
    name="search_button",
    region=(100, 100, 80, 30),
    description="Search button",
    tags=["ui", "button"]
)

# Get pixel color
color = ScreenTool.pixel(100, 100)

# Image operations (enhanced!)
# Click by template name (NEW!)
ImageTool.click_by_template_name(
    "search_button",
    confidence=0.8,
    button="left"
)

# Locate with fallback strategy (NEW!)
pos = ImageTool.locate_with_fallback(
    ["button_v1.png", "button_v2.png"],
    confidence=0.7
)

# Find best match from multiple templates (NEW!)
pos, index = ImageTool.find_best_match(
    ["template1.png", "template2.png", "template3.png"]
)

# Template management (NEW!)
template_manager = get_template_manager()

# Save template
template_manager.save_template(
    name="my_button",
    image=screenshot,
    description="My button",
    region=(100, 100, 80, 30),
    tags=["ui", "button"]
)

# Capture and save template directly
template_manager.capture_and_save_template(
    name="submit_button",
    region=(200, 200, 100, 40),
    description="Submit form button"
)

# List all templates
templates = template_manager.list_templates()
for t in templates:
    print(f"{t.name}: {t.description}")

# Load template
image, metadata = template_manager.load_template("search_button")

# Get template image path
img_path = template_manager.get_template_image_path("search_button")

# Check if template exists
if template_manager.template_exists("search_button"):
    print("Template exists!")

# Delete template
template_manager.delete_template("old_button")
```

## New: UI Locator Skill Usage

```python
from computer_use.skills.ui_locator import UILocatorSkill

skill = UILocatorSkill()

# Capture and save template
result = skill.execute(
    action="capture",
    template_name="search_button",
    region=(100, 100, 80, 30),
    description="Search button"
)

# Locate element
result = skill.execute(
    action="locate",
    template_name="search_button",
    confidence=0.8
)

# Locate and click
result = skill.execute(
    action="click",
    template_name="search_button",
    confidence=0.8
)

# Verify position
result = skill.execute(
    action="verify",
    template_name="search_button"
)
```

## Safety Features

- **Fail-Safe Mode**: Move mouse to top-left corner (0, 0) to abort all operations (enabled by default)
- **Input Validation**: All parameters are validated before execution
- **Coordinate Checking**: Ensures operations stay within screen bounds

## Best Practices

### Mouse & Coordinates
1. **Always check screen size first** when working with absolute coordinates
2. **Use UI templates instead of coordinates** when possible - they're more robust to resolution changes
3. **Add small delays** between operations for reliability (configured via PAUSE env var)
4. **Use relative movements** when possible for more flexible automation
5. **Test coordinates** with `mouse position` before clicking
6. **Use hotkeys** instead of typing menu navigation when possible

### Template Management (NEW!)
1. **Use meaningful template names** like `submit_button_main` or `nav_home_icon`
2. **Set appropriate confidence levels**:
   - Stable UI elements: 0.8-0.9
   - Elements with variations: 0.6-0.7
   - Need precise matches: 0.9+
3. **Use tags** for categorization: `ui`, `button`, `nav`, `form`, etc.
4. **Version templates** with suffixes like `_v1`, `_v2` when UI changes
5. **Use fallback strategies** with `locate_with_fallback()` for robustness
6. **Combine with relative coordinate adjustment** for ultimate precision

### Screenshots & Annotations
1. **Use annotated screenshots** to mark regions of interest for the model
2. **Capture templates** of frequently used UI elements for reuse
3. **Store templates in version control** for consistent automation across environments

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

### Taking an Annotated Screenshot

```bash
# Take screenshot with boxes marking UI elements
computer-use screen screenshot --output ui_analysis.png \
  --box 100 100 80 30 "Search" \
  --box 200 200 100 40 "Submit" \
  --point 500 300 "Target Area"
```

### Template-Based UI Interaction (NEW!)

```bash
# Step 1: Capture and save a UI element as template
computer-use template save --name search_button --region 100 100 80 30 \
  --description "Search button" --tag ui --tag button

# Step 2: Later, click using just the template name
computer-use template click search_button --confidence 0.8

# Or list templates to see what's available
computer-use template list
```

### Robust Clicking with Fallback (Python)

```python
from computer_use.tools.image import ImageTool
from computer_use.tools.template import get_template_manager

template_manager = get_template_manager()

# Try multiple template versions for robustness
templates_to_try = [
    str(template_manager.get_template_image_path("button_normal")),
    str(template_manager.get_template_image_path("button_hover")),
    str(template_manager.get_template_image_path("button_focus")),
]

pos = ImageTool.locate_with_fallback(templates_to_try, confidence=0.7)
if pos:
    from computer_use.tools.mouse import MouseTool
    MouseTool.click(x=pos[0], y=pos[1])
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

## Model Guidance for Precise Interaction

When the model needs to interact with UI elements, follow this priority:

1. **Highest Priority: Use templates by name**
   ```
   ImageTool.click_by_template_name("search_button", confidence=0.8)
   ```

2. **High Priority: Use relative coordinates + incremental adjustment**
   - First move to approximate location
   - Get current position
   - Adjust incrementally until precise

3. **Medium Priority: Use image matching**
   ```
   ImageTool.click_image("button.png", confidence=0.8)
   ```

4. **Low Priority: Direct absolute coordinates**
   - Only use when templates/images aren't available
   - Always verify position before clicking

## Troubleshooting

If commands don't work as expected:

1. Check that the package is installed in editable mode: `pip install -e .`
2. Verify the environment: `cp .env.example .env`
3. Check log output for errors
4. On macOS, ensure Terminal has accessibility permissions
5. Try simpler commands first to verify basic functionality
6. For template issues: Check that the `templates/` directory exists and is writable
7. For confidence issues: Try lowering the confidence threshold slightly
8. For coordinate issues: Use `screen size` to verify screen dimensions
