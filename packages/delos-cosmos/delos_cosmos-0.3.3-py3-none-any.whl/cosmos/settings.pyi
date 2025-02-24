from enum import Enum

from loguru import logger as cosmos_logger

class VerboseLevel(int, Enum):
    NONE = 0
    INFO = 1
    DEBUG = 2

__all__ = ["VerboseLevel", "cosmos_logger"]
