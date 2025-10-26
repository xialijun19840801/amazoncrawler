"""Logging configuration."""

from loguru import logger
import sys


def setup_logger() -> None:
    """Configure loguru logger."""
    logger.remove()  # Remove default handler
    
    # Add console handler with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )
    
    # Add file handler
    logger.add(
        "logs/crawler_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
    )


# Initialize logger
setup_logger()

