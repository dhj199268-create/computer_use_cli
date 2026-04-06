# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a computer control CLI tool based on pyautogui, allowing agents to interact with a computer through a structured interface. It provides mouse control, keyboard input, screen operations, image recognition, and automation skills.

## Common Commands

### Development Setup
```bash
# Install in editable mode
pip install -e .

# Copy environment configuration
cp .env.example .env
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools/test_mouse.py

# Run tests with coverage
pytest --cov=computer_use

# Run specific test
pytest tests/test_tools/test_mouse.py::test_mouse_position
```

### CLI Usage
```bash
# Get help
computer-use --help

# Mouse operations
computer-use mouse position
computer-use mouse move --x 100 --y 100
computer-use mouse click

# Keyboard operations
computer-use keyboard write --text "Hello, World!"
computer-use keyboard hotkey --keys cmd c

# Screen operations
computer-use screen size
computer-use screen screenshot --output screenshot.png
```

## Code Architecture

### Layered Structure

1. **Core Layer** (`src/computer_use/core/`)
   - `config.py`: Global configuration management via environment variables
   - `exceptions.py`: Custom exception hierarchy
   - `logger.py`: Logging setup

2. **Tools Layer** (`src/computer_use/tools/`)
   - `mouse.py`: `MouseTool` class - all mouse operations (move, click, drag, scroll)
   - `keyboard.py`: `KeyboardTool` class - text input, key presses, hotkeys
   - `image.py`: `ImageTool` class - image recognition, screen matching

3. **Skills Layer** (`src/computer_use/skills/`)
   - `base.py`: `BaseSkill` abstract base class for creating reusable automation skills
   - Skills inherit from `BaseSkill` and implement `execute()` method

4. **CLI Layer** (`src/computer_use/cli/`)
   - `main.py`: Main Click command group
   - `mouse_cmd.py`, `keyboard_cmd.py`, `screen_cmd.py`, `skill_cmd.py`: Subcommands
   - Uses Click for command-line interface with Rich for output formatting

5. **Utils Layer** (`src/computer_use/utils/`)
   - `validators.py`: Input validation functions
   - `coordinates.py`: Coordinate utilities
   - `image_processing.py`: Image processing helpers

### Key Patterns

- **Configuration**: Global singleton `config` instance in `core.config`
- **Validation**: All inputs validated through utils before pyautogui calls
- **Exceptions**: Custom exceptions inherit from `ComputerUseError`
- **Testing**: Tests use `mock_pyautogui` fixture to mock pyautogui

### Entry Points

- CLI: `computer_use.__main__:main` → `computer_use.cli.main:cli`
- Package: Import from `computer_use` namespace
