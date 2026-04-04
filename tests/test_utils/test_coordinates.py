import pytest

from computer_use.utils.coordinates import (
    clamp_coordinate,
    normalize_coordinate,
    is_valid_coordinate,
    calculate_distance,
)


class TestCoordinates:
    def test_clamp_coordinate(self, mocker):
        from computer_use.tools.mouse import MouseTool

        mocker.patch.object(MouseTool, "size", return_value=(1920, 1080))

        assert clamp_coordinate(2000, 2000) == (1919, 1079)
        assert clamp_coordinate(-100, -100) == (0, 0)
        assert clamp_coordinate(500, 500) == (500, 500)

    def test_normalize_coordinate(self, mocker):
        from computer_use.tools.mouse import MouseTool

        mocker.patch.object(MouseTool, "size", return_value=(1920, 1080))

        norm_x, norm_y = normalize_coordinate(960, 540)
        assert norm_x == pytest.approx(0.5)
        assert norm_y == pytest.approx(0.5)

    def test_is_valid_coordinate(self, mocker):
        from computer_use.tools.mouse import MouseTool

        mocker.patch.object(MouseTool, "on_screen", return_value=True)
        assert is_valid_coordinate(100, 100) is True

        mocker.patch.object(MouseTool, "on_screen", return_value=False)
        assert is_valid_coordinate(10000, 10000) is False

    def test_calculate_distance(self):
        assert calculate_distance(0, 0, 3, 4) == 5.0
        assert calculate_distance(10, 10, 10, 10) == 0.0
        assert calculate_distance(1, 2, 4, 6) == 5.0
