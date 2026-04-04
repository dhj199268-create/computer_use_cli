from typing import Optional, Tuple, TypeVar

from ..core.exceptions import ValidationError, InvalidButtonError

T = TypeVar("T", int, float)


def validate_int(
    value: int,
    name: str,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
) -> int:
    """Validate an integer value.

    Args:
        value: Value to validate
        name: Name of the parameter for error messages
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validated integer

    Raises:
        ValidationError: If value is invalid
    """
    if not isinstance(value, int):
        raise ValidationError(f"{name} must be an integer, got {type(value).__name__}")

    if min_val is not None and value < min_val:
        raise ValidationError(f"{name} must be >= {min_val}, got {value}")

    if max_val is not None and value > max_val:
        raise ValidationError(f"{name} must be <= {max_val}, got {value}")

    return value


def validate_float(
    value: float,
    name: str,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
) -> float:
    """Validate a float value.

    Args:
        value: Value to validate
        name: Name of the parameter for error messages
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validated float

    Raises:
        ValidationError: If value is invalid
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(f"{name} must be a number, got {type(value).__name__}")

    value = float(value)

    if min_val is not None and value < min_val:
        raise ValidationError(f"{name} must be >= {min_val}, got {value}")

    if max_val is not None and value > max_val:
        raise ValidationError(f"{name} must be <= {max_val}, got {value}")

    return value


def validate_button(
    button: str,
    valid_buttons: set,
) -> str:
    """Validate a mouse button.

    Args:
        button: Button to validate
        valid_buttons: Set of valid button names

    Returns:
        Validated button

    Raises:
        InvalidButtonError: If button is invalid
    """
    if not isinstance(button, str):
        raise InvalidButtonError(f"Button must be a string, got {type(button).__name__}")

    button_lower = button.lower()
    if button_lower not in valid_buttons:
        raise InvalidButtonError(
            f"Invalid button: {button}. Valid buttons: {', '.join(valid_buttons)}"
        )

    return button_lower


def validate_region(
    region: Tuple[int, int, int, int],
) -> Tuple[int, int, int, int]:
    """Validate a region tuple (left, top, width, height).

    Args:
        region: Region tuple to validate

    Returns:
        Validated region

    Raises:
        ValidationError: If region is invalid
    """
    if not isinstance(region, tuple) or len(region) != 4:
        raise ValidationError(
            "Region must be a tuple of (left, top, width, height)"
        )

    left, top, width, height = region

    validate_int(left, "left")
    validate_int(top, "top")
    validate_int(width, "width", min_val=0)
    validate_int(height, "height", min_val=0)

    return region
