from enum import IntEnum


class LogLevel(IntEnum):
    """Enumeration of available logging levels.

    Attributes:
        DEBUG: Detailed information for debugging.
        INFO: General information about program execution.
        WARNING: Indicates a potential problem.
        ERROR: A more serious problem.
        CRITICAL: A critical error that may prevent program execution.
    """

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
