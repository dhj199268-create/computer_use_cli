# Computer Use CLI

A computer control CLI tool based on pyautogui, providing computer use capabilities for AI agents through a structured interface.

[中文文档](README_CN.md)

## Features

- **Mouse Control**: Move, click, drag, scroll, and other mouse operations
- **Keyboard Control**: Text input, key presses, hotkey combinations
- **Screen Operations**: Screenshots, screen size, pixel color detection
- **Image Recognition**: Locate images on screen, click by image matching
- **Skills System**: Reusable automation skill framework
- **Rich CLI**: Beautiful command-line interface with Rich

## Installation

```bash
# Install from source
pip install -e .
```

## Quick Start

```bash
# View help
computer-use --help

# Mouse operations
computer-use mouse position                    # Get current mouse position
computer-use mouse move --x 100 --y 100      # Move mouse to coordinates
computer-use mouse click                       # Click at current position

# Keyboard operations
computer-use keyboard write --text "Hello"    # Type text
computer-use keyboard hotkey --keys cmd c     # Press hotkey combination

# Screen operations
computer-use screen size                       # Get screen resolution
computer-use screen screenshot --output shot.png  # Take screenshot
```

## Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Key configuration options:

- `PAUSE`: Delay between operations (default: 0.1 seconds)
- `FAILSAFE`: Enable fail-safe feature (default: true)
- `MINIMUM_DURATION`: Minimum movement duration
- `LOG_LEVEL`: Logging level (default: INFO)

## Safety

- **Fail-safe**: Move mouse to top-left corner (0, 0) to abort operations
- Always test operations carefully before automation
- The fail-safe is enabled by default

## Project Structure

```
computer_use_cli/
├── src/computer_use/
│   ├── core/           # Core configuration and exceptions
│   ├── tools/          # Mouse, keyboard, and image tools
│   ├── skills/         # Automation skills framework
│   ├── cli/            # Command-line interface
│   └── utils/          # Utility functions
├── tests/              # Test suite
├── examples/           # Usage examples
└── skills/             # Skill configuration files
```

## For Agents

This tool is designed to provide AI agents with computer use capabilities. Agents can:

1. Use the CLI commands directly for simple operations
2. Import the Python modules for programmatic control
3. Build custom skills using the BaseSkill abstract class
4. Leverage image recognition for visual automation

## License

MIT
