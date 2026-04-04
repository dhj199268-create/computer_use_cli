import pytest

from computer_use.tools.mouse import MouseTool
from computer_use.core.exceptions import InvalidCoordinateError, InvalidButtonError


class TestMouseTool:
    def test_size(self, mock_pyautogui):
        mock_pyautogui.size.return_value = (1920, 1080)
        size = MouseTool.size()
        assert size == (1920, 1080)
        mock_pyautogui.size.assert_called_once()

    def test_position(self, mock_pyautogui):
        mock_pyautogui.position.return_value = (500, 300)
        pos = MouseTool.position()
        assert pos == (500, 300)
        mock_pyautogui.position.assert_called_once()

    def test_on_screen(self, mock_pyautogui):
        mock_pyautogui.onScreen.return_value = True
        result = MouseTool.on_screen(100, 100)
        assert result is True
        mock_pyautogui.onScreen.assert_called_once_with(100, 100)

    def test_move_to(self, mock_pyautogui):
        mock_pyautogui.onScreen.return_value = True
        MouseTool.move_to(500, 300, duration=0.5)
        mock_pyautogui.moveTo.assert_called_once_with(500, 300, duration=0.5, tween=None)

    def test_move_to_invalid_coordinates(self, mock_pyautogui):
        mock_pyautogui.onScreen.return_value = False
        with pytest.raises(InvalidCoordinateError):
            MouseTool.move_to(10000, 10000)

    def test_move(self, mock_pyautogui):
        MouseTool.move(100, -50, duration=0.25)
        mock_pyautogui.move.assert_called_once_with(100, -50, duration=0.25, tween=None)

    def test_click(self, mock_pyautogui):
        MouseTool.click(x=100, y=100, button="left", clicks=2, interval=0.1)
        mock_pyautogui.click.assert_called_once_with(
            x=100, y=100, button="left", clicks=2, interval=0.1
        )

    def test_invalid_button(self, mock_pyautogui):
        with pytest.raises(InvalidButtonError):
            MouseTool.click(button="invalid")

    def test_scroll(self, mock_pyautogui):
        MouseTool.scroll(5, x=200, y=200)
        mock_pyautogui.scroll.assert_called_once_with(5, x=200, y=200)
