import inspect
import math
import os
import shutil
import warnings
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, List, Optional, TextIO

from .text_color import TextColor


class LogFormatter:
    """Handles formatting of log messages and headers.

    Attributes:
        level_width (int): Width reserved for log level text.
        margin_width (int): Width of margin including separator.
    """

    def __init__(self, level_width: int, margin_width: int):
        self.level_width = level_width
        self.margin_width = margin_width

    def format_lines(
        self, text: str, available_width: int, prefix: str = ""
    ) -> List[str]:
        """Generic line formatter that handles text wrapping and prefixing.

        Args:
            text (str): The text to format.
            available_width (int): Maximum width available for text.
            prefix (str, optional): Prefix to add to first line. Defaults to "".

        Returns:
            List[str]: List of formatted lines.
        """
        # Just return the text with prefix, no splitting
        return [f"{prefix}{text}"]

    def format_message(self, level: str, msg: str, terminal_width: int) -> List[str]:
        """Format message with log level prefix.

        Args:
            level (str): The log level to display.
            msg (str): The message to format.
            terminal_width (int): Width of the terminal.

        Returns:
            List[str]: List of formatted message lines.
        """
        available_width = terminal_width - (self.level_width + self.margin_width)
        prefix = f"{level.upper():>{self.level_width}} | "
        return self.format_lines(msg, available_width, prefix)

    def format_header(
        self, timestamp: str, caller_info: str, terminal_width: int
    ) -> List[str]:
        """Format header with timestamp prefix.

        Args:
            timestamp (str): The timestamp to display.
            caller_info (str): Information about the caller.
            terminal_width (int): Width of the terminal.

        Returns:
            List[str]: List of formatted header lines.
        """
        available_width = terminal_width - (self.level_width + self.margin_width)
        prefix = f"{timestamp:>{self.level_width}} | "
        return self.format_lines(caller_info, available_width, prefix)


class Logger:
    """Main logger class that handles all logging functionality.

    Attributes:
        DEFAULT_TERMINAL_WIDTH (int): Default width if terminal width cannot be determined.
        TIMESTAMP_FORMAT (str): Format string for timestamps.
        LOG_LEVEL_WIDTH (int): Width reserved for log level text.
        MARGIN_WIDTH (int): Width of margin including separator.
        display_level (str): Current minimum log level to display.
        do_log (bool): Whether logging is enabled.
        do_log_to_file (bool): Whether file logging is enabled.
        log_file_name (str): Name of the current log file.
    """

    # Configuration constants
    DEFAULT_TERMINAL_WIDTH = 80
    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    LOG_LEVEL_WIDTH = 23
    MARGIN_WIDTH = 3  # For " | " separator

    def __init__(self):
        self.formatter = LogFormatter(self.LOG_LEVEL_WIDTH, self.MARGIN_WIDTH)

        # Initialize logging levels
        self._log_levels: Dict[str, int] = {
            "debug": 0,
            "info": 1,
            "warning": 2,
            "error": 3,
            "critical": 4,
        }

        # Initialize color mapping
        self._color_map: Dict[str, str] = {
            "warning": "yellow",
            "error": "orange",
            "critical": "red",
        }

        # Logging state
        self.display_level: str = "info"
        self.do_log: bool = True
        self.do_log_to_file: bool = False
        self.display_location: bool = False

        # File logging settings
        self._setup_file_logging()

    def _setup_file_logging(self) -> None:
        """Initialize file logging settings."""
        self._default_log_file_name: str = "%Y-%m-%d_%H-%M-%S.log"
        self.log_file_name: str = datetime.now().strftime(self._default_log_file_name)
        self._log_file: Optional[TextIO] = None

    def _get_timestamp(self) -> str:
        """Get formatted timestamp for logging.

        Returns:
            str: Formatted timestamp string.
        """
        return datetime.now().strftime(self.TIMESTAMP_FORMAT)[:-3]

    @staticmethod
    def _get_caller_info() -> str:
        """Get information about the caller of the logging function.

        Returns:
            str: Formatted string with caller information.
        """
        stack = inspect.stack()
        frame = stack[2]  # The caller's frame
        return f'File "{frame.filename}", line {frame.lineno}, in {frame.function}'

    def _get_terminal_width(self) -> int:
        """Get current terminal width with fallbacks.

        Returns:
            int: Width of the terminal in characters.
        """
        try:
            return shutil.get_terminal_size().columns
        except (AttributeError, ValueError, OSError):
            try:
                return int(os.environ.get("COLUMNS", self.DEFAULT_TERMINAL_WIDTH))
            except ValueError:
                return self.DEFAULT_TERMINAL_WIDTH

    @contextmanager
    def _log_file_context(self):
        """Context manager for file operations.

        Yields:
            Optional[TextIO]: File object if file logging is enabled, None otherwise.
        """
        if self.do_log_to_file:
            with open(self.log_file_name, "a") as file:
                yield file
        else:
            yield None

    def _should_log(self, level: str) -> bool:
        """Determine if message should be logged based on current settings.

        Args:
            level (str): The log level to check.

        Returns:
            bool: True if message should be logged, False otherwise.
        """
        return (
            self.do_log
            and self._log_levels[level] >= self._log_levels[self.display_level]
        )

    def _validate_log_level(self, level: str) -> None:
        """Ensure log level is valid.

        Args:
            level (str): The log level to validate.

        Raises:
            ValueError: If the log level is not valid.
        """
        if level.lower() not in self._log_levels:
            raise ValueError(
                f"Invalid logging level: {level}, must be one of: {list(self._log_levels.keys())}"
            )


    def __call__(
        self, msg: str, level: str = "info", color: Optional[str] = None
    ) -> None:
        """Log a message with the specified level.

        Args:
            msg (str): The message to log.
            level (str, optional): The log level. Defaults to "info".
        """
        level = level.lower()
        self._validate_log_level(level)

        if not self._should_log(level):
            return

        terminal_width = self._get_terminal_width()
        timestamp = self._get_timestamp()

        # Handle color output
        level_color = self._color_map.get(level, "")

        if color:
            level_color = color

        if level_color:
            print(TextColor.get_ansi_code(level_color), end="", flush=True)

        try:
            if self.display_location:
                # Multi-line output with location
                caller_info = self._get_caller_info()
                header_lines = self.formatter.format_header(
                    timestamp, caller_info, terminal_width
                )
                detail_lines = self.formatter.format_message(level, msg, terminal_width)
                self._write_log_lines(header_lines + detail_lines)
            else:
                # Single-line output without location
                prefix = f"{timestamp} | {level.upper()} | "
                available_width = terminal_width - len(prefix)
                msg_lines = self.formatter.format_lines(msg, available_width, prefix)
                self._write_log_lines(msg_lines)
        finally:
            if level_color:
                print(TextColor.reset, end="", flush=True)

    def _write_log_lines(self, lines: List[str]) -> None:
        """Write lines to console and log file.

        Args:
            lines (List[str]): The lines to write.
        """
        with self._log_file_context() as log_file:
            for line in lines:
                print(line)
                if log_file:
                    log_file.write(f"{line}\n")

    # Public API methods
    def log_on(self) -> None:
        """Enable logging."""
        self.do_log = True

    def log_off(self) -> None:
        """Disable logging."""
        self.do_log = False

    def set_display_level(self, level: str) -> None:
        """Set minimum logging level to display.

        Args:
            level (str): The minimum log level to display.

        Raises:
            ValueError: If the log level is not valid.
        """
        self._validate_log_level(level)
        self.display_level = level.lower()

    def log_to_file(self, file_name: Optional[str] = None) -> None:
        """Enable logging to file.

        Args:
            file_name (Optional[str], optional): Name of log file. Defaults to None.
        """
        if file_name is not None:
            self.log_file_name = file_name
        self.do_log_to_file = True

    def set_display_location(self, display: bool) -> None:
        """Set whether to display the location of the log message.

        Args:
            display (bool): Whether to display the location.
        """
        self.display_location = display

    def set_loglevel_color(self, level: str, color: str) -> None:
        """Set color for a log level.

        Args:
            level (str): The log level to set color for.
            color (str): The color to use (hex code or name).

        Raises:
            ValueError: If the log level or color is invalid.
        """
        self._validate_log_level(level)
        TextColor.validate_color(color)

        self._color_map[level] = color

    def create_custom_loglevel(self, name: str, color: Optional[str] = None) -> None:
        """Create new custom log level.

        Args:
            name (str): Name of the new log level.
            color (Optional[str], optional): Color for the new level. Defaults to None.
        """
        name = name.lower()
        try:
            self._validate_log_level(name)
            warnings.warn(f'Log level "{name}" already exists. Ignoring creation.')
            return
        except ValueError:
            pass

        self._log_levels[name] = len(self._log_levels)
        if color:
            self.set_loglevel_color(name, color)

    # Helper methods for color handling
    @staticmethod
    def _is_valid_hex_color(color: str) -> bool:
        """Validate hex color format.

        Args:
            color (str): The color code to validate.

        Returns:
            bool: True if valid hex color, False otherwise.
        """
        return len(color) == 7 and all(c in "0123456789ABCDEFabcdef" for c in color[1:])

    @staticmethod
    def _hex_to_ansi(hex_color: str) -> str:
        """Convert hex color to ANSI escape sequence.

        Args:
            hex_color (str): The hex color code to convert.

        Returns:
            str: ANSI escape sequence for the color.
        """
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f"\u001b[38;2;{r};{g};{b}m"


# Global logger instance
log = Logger()
