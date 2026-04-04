class ComputerUseError(Exception):
    """Base exception for all computer use errors."""

    pass


class InvalidCoordinateError(ComputerUseError):
    """Raised when coordinates are invalid."""

    pass


class ImageNotFoundError(ComputerUseError):
    """Raised when an image cannot be found on screen."""

    pass


class OperationFailedError(ComputerUseError):
    """Raised when an operation fails."""

    pass


class InvalidButtonError(ComputerUseError):
    """Raised when an invalid mouse button is specified."""

    pass


class InvalidKeyError(ComputerUseError):
    """Raised when an invalid keyboard key is specified."""

    pass


class ValidationError(ComputerUseError):
    """Raised when input validation fails."""

    pass
