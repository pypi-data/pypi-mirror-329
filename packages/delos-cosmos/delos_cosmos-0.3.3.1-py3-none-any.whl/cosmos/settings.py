"""Logger and other default settings for the Cosmos client."""

from enum import Enum

from loguru import logger as cosmos_logger


class VerboseLevel(int, Enum):
    """Verbose level for the logger."""

    NONE = 0
    INFO = 1
    DEBUG = 2


__all__ = ["VerboseLevel", "cosmos_logger"]
