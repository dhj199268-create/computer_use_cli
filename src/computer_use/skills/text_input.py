from typing import Any, Dict, List, Optional

from ..core.logger import get_logger
from ..tools.keyboard import KeyboardTool
from .base import BaseSkill

logger = get_logger(__name__)


class TextInputSkill(BaseSkill):
    """Skill for text input: typing, shortcuts, copy/paste."""

    @classmethod
    def get_description(cls) -> str:
        return "Input text, press keys, use shortcuts, and copy/paste."

    @classmethod
    def get_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "action": {
                "type": "str",
                "required": True,
                "description": "Action to perform: write, press, hotkey, copy, paste, cut, undo, select_all",
            },
            "text": {"type": "str", "required": False, "description": "Text to write (for 'write' action)"},
            "keys": {"type": "list", "required": False, "description": "Key or list of keys (for 'press' or 'hotkey')"},
            "interval": {"type": "float", "required": False, "default": 0.0, "description": "Interval between keystrokes"},
            "presses": {"type": "int", "required": False, "default": 1, "description": "Number of presses"},
        }

    def execute(self, context: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        action = kwargs.get("action")

        if action == "write":
            return self._write(**kwargs)
        elif action == "press":
            return self._press(**kwargs)
        elif action == "hotkey":
            return self._hotkey(**kwargs)
        elif action == "copy":
            return self._copy()
        elif action == "paste":
            return self._paste()
        elif action == "cut":
            return self._cut()
        elif action == "undo":
            return self._undo()
        elif action == "select_all":
            return self._select_all()
        else:
            raise ValueError(f"Unknown action: {action}")

    def _write(self, **kwargs) -> None:
        text = kwargs["text"]
        interval = kwargs.get("interval", 0.0)
        KeyboardTool.write(text, interval=interval)
        logger.info(f"Wrote text: {text[:50]}{'...' if len(text) > 50 else ''}")

    def _press(self, **kwargs) -> None:
        keys = kwargs["keys"]
        presses = kwargs.get("presses", 1)
        interval = kwargs.get("interval", 0.0)
        KeyboardTool.press(keys, presses=presses, interval=interval)
        logger.info(f"Pressed keys: {keys}")

    def _hotkey(self, **kwargs) -> None:
        keys = kwargs["keys"]
        interval = kwargs.get("interval", 0.0)
        if isinstance(keys, str):
            key_list = keys.split()
        else:
            key_list = keys
        KeyboardTool.hotkey(*key_list, interval=interval)
        logger.info(f"Pressed hotkey: {'+'.join(key_list)}")

    def _copy(self) -> None:
        KeyboardTool.copy()
        logger.info("Copied to clipboard")

    def _paste(self) -> None:
        KeyboardTool.paste()
        logger.info("Pasted from clipboard")

    def _cut(self) -> None:
        KeyboardTool.cut()
        logger.info("Cut to clipboard")

    def _undo(self) -> None:
        KeyboardTool.undo()
        logger.info("Undo")

    def _select_all(self) -> None:
        KeyboardTool.select_all()
        logger.info("Selected all")
