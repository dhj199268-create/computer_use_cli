import pytest

from computer_use.tools.keyboard import KeyboardTool
from computer_use.core.exceptions import InvalidKeyError


class TestKeyboardTool:
    def test_write(self, mock_pyautogui):
        KeyboardTool.write("Hello, World!", interval=0.1)
        mock_pyautogui.write.assert_called_once_with("Hello, World!", interval=0.1)

    def test_press_single_key(self, mock_pyautogui):
        KeyboardTool.press("enter", presses=2, interval=0.1)
        mock_pyautogui.press.assert_called_once_with("enter", presses=2, interval=0.1)

    def test_press_multiple_keys(self, mock_pyautogui):
        KeyboardTool.press(["a", "b", "c"])
        mock_pyautogui.press.assert_called_once_with(["a", "b", "c"], presses=1, interval=0.0)

    def test_invalid_key(self, mock_pyautogui):
        mock_pyautogui.KEY_NAMES = {"enter", "space", "a"}
        with pytest.raises(InvalidKeyError):
            KeyboardTool.press("invalid_key_that_does_not_exist")

    def test_key_down(self, mock_pyautogui):
        KeyboardTool.key_down("shift")
        mock_pyautogui.keyDown.assert_called_once_with("shift")

    def test_key_up(self, mock_pyautogui):
        KeyboardTool.key_up("shift")
        mock_pyautogui.keyUp.assert_called_once_with("shift")

    def test_hotkey(self, mock_pyautogui):
        KeyboardTool.hotkey("ctrl", "c", interval=0.05)
        mock_pyautogui.hotkey.assert_called_once_with("ctrl", "c", interval=0.05)

    def test_hold_context_manager(self, mock_pyautogui):
        with KeyboardTool.hold("ctrl"):
            pass
        mock_pyautogui.keyDown.assert_called_once_with("ctrl")
        mock_pyautogui.keyUp.assert_called_once_with("ctrl")

    def test_hold_multiple_keys(self, mock_pyautogui):
        with KeyboardTool.hold(["ctrl", "shift"]):
            pass
        calls = mock_pyautogui.keyDown.call_args_list
        assert [call[0][0] for call in calls] == ["ctrl", "shift"]
        calls = mock_pyautogui.keyUp.call_args_list
        assert [call[0][0] for call in calls] == ["shift", "ctrl"]
