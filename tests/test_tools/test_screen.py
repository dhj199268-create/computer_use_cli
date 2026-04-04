from unittest.mock import MagicMock

from computer_use.tools.screen import ScreenTool


class TestScreenTool:
    def test_screenshot(self, mock_pyautogui):
        mock_image = MagicMock()
        mock_pyautogui.screenshot.return_value = mock_image

        result = ScreenTool.screenshot(filename="test.png")

        assert result == mock_image
        mock_pyautogui.screenshot.assert_called_once_with("test.png", region=None)

    def test_screenshot_with_region(self, mock_pyautogui):
        mock_image = MagicMock()
        mock_pyautogui.screenshot.return_value = mock_image

        result = ScreenTool.screenshot(region=(0, 0, 100, 100))

        assert result == mock_image
        mock_pyautogui.screenshot.assert_called_once_with(None, region=(0, 0, 100, 100))

    def test_pixel(self, mock_pyautogui):
        mock_pyautogui.pixel.return_value = (255, 0, 0)

        result = ScreenTool.pixel(100, 200)

        assert result == (255, 0, 0)
        mock_pyautogui.pixel.assert_called_once_with(100, 200)

    def test_pixel_matches_color_true(self, mock_pyautogui):
        mock_pyautogui.pixelMatchesColor.return_value = True

        result = ScreenTool.pixel_matches_color(100, 200, (255, 0, 0), tolerance=10)

        assert result is True
        mock_pyautogui.pixelMatchesColor.assert_called_once_with(
            100, 200, (255, 0, 0), tolerance=10
        )

    def test_pixel_matches_color_false(self, mock_pyautogui):
        mock_pyautogui.pixelMatchesColor.return_value = False

        result = ScreenTool.pixel_matches_color(100, 200, (0, 0, 0))

        assert result is False
