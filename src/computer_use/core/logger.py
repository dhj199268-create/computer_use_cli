import logging
import sys
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

from .config import config


def get_logger(
    name: str = "computer_use",
    level: Optional[str] = None,
) -> logging.Logger:
    """
    Get a configured logger with Rich formatting.

    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if not logger.handlers:
        log_level = level or config.log_level
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

        # Rich handler for beautiful output
        console = Console(stderr=True)
        handler = RichHandler(
            console=console,
            show_time=True,
            show_level=True,
            show_path=False,
            rich_tracebacks=True,
        )
        handler.setFormatter(
            logging.Formatter("%(message)s", datefmt="[%X]")
        )
        logger.addHandler(handler)

    return logger
