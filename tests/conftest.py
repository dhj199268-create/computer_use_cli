import pytest


@pytest.fixture
def mock_pyautogui(mocker):
    """Fixture to mock pyautogui."""
    mock = mocker.patch("pyautogui")
    mock.size.return_value = (1920, 1080)
    mock.position.return_value = (100, 100)
    mock.onScreen.return_value = True
    return mock


@pytest.fixture
def sample_config():
    """Fixture for sample configuration."""
    return {
        "PAUSE": 0.1,
        "FAILSAFE": True,
        "MINIMUM_DURATION": 0.0,
    }
