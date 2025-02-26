import json
import logging
import time
from pathlib import Path
from typing import Any, Optional, Protocol, TypeVar, Union, cast

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.syntax import Syntax

# Protocol for Rich's dynamic attributes
class RichLogRecord(Protocol):
    rich_type: str
    value: Any
    language: str = 'python'  # Default value

class RichMessageHandler(RichHandler):
    """Rich handler that supports metadata-based formatting"""

    def render_message(self, record: logging.LogRecord, message: str) -> Union[str, Panel]:
        rich_record = cast(RichLogRecord, record)
        if hasattr(rich_record, "rich_type") and hasattr(rich_record, "value"):
            if rich_record.rich_type == "json":
                syntax = Syntax(
                    json.dumps(rich_record.value, indent=2),
                    "json",
                    theme="monokai",
                    word_wrap=True,
                )
                return Panel(syntax, title=message)
            elif rich_record.rich_type == "code":
                syntax = Syntax(
                    rich_record.value,
                    getattr(rich_record, "language", "python"),
                    theme="monokai",
                    word_wrap=True,
                )
                return Panel(syntax, title=message)
            elif rich_record.rich_type == "panel":
                return Panel(str(rich_record.value), title=message)
            elif rich_record.rich_type == "text":
                return f"{message} `{rich_record.value}`"
        return message


class FileFormatter(logging.Formatter):
    """Custom formatter that maintains rich-style messages in log files"""

    def format(self, record: logging.LogRecord) -> str:
        rich_record = cast(RichLogRecord, record)
        # First format with the standard formatter
        formatted_msg = super().format(record)  # Use original record for standard formatting

        # Rich dynamically adds these attributes at runtime
        if hasattr(rich_record, "rich_type") and hasattr(rich_record, "value"):
            if rich_record.rich_type == "json":
                json_str = json.dumps(rich_record.value, indent=2)
                formatted_msg = f"{formatted_msg}\n```json\n{json_str}\n```"
            elif rich_record.rich_type == "code":
                lang = getattr(rich_record, "language", "python")
                formatted_msg = f"{formatted_msg}\n```{lang}\n{rich_record.value}\n```"
            elif rich_record.rich_type == "panel":
                formatted_msg = f"{formatted_msg}\n---\n{rich_record.value}\n---"
            elif rich_record.rich_type == "text":
                formatted_msg = f"{formatted_msg} `{rich_record.value}`"

        return formatted_msg


def setup_logging(log_file: Optional[str] = None, level: int = logging.INFO):
    """Set up logging with rich console output and formatted file output."""
    # Fix UTF-8 encoding for Windows and other platforms
    fix_utf8()
    
    # Configure the root logger
    logger = logging.getLogger("paic_patterns")
    logger.setLevel(level)
    logger.handlers.clear()

    # Console handler with rich formatting
    console = Console()
    console_handler = RichMessageHandler(
        console=console,
        show_time=True,
        show_level=True,
        show_path=False,
        markup=True,
    )
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    # File handler for formatted text logging
    if log_file is None:
        log_file = str(Path.cwd() / "paic-patterns.log")

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(
        FileFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    return logger


def log(console: Console, message: str, **kwargs):
    """Log a message to the console."""
    console.print(message, **kwargs)


def log_panel(console: Console, title: str, content: str):
    """Log content in a panel."""
    console.print(Panel(content, title=title))


def fix_utf8():
    """Fix UTF-8 encoding issues on Windows and other platforms."""
    try:
        import sys
        import os

        # On Windows, we need to enable UTF-8 mode
        if sys.platform == "win32":
            # Enable UTF-8 mode for the Python runtime
            os.environ["PYTHONIOENCODING"] = "utf-8"

            # Try to set console code page to UTF-8
            try:
                import ctypes

                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleOutputCP(65001)  # UTF-8 code page
            except:
                print("(Win) Failed to set console code page to UTF-8")
                pass  # Fail silently if we can't set the code page

        # For all platforms, try to reconfigure stdout/stderr if needed
        if (
            hasattr(sys.stdout, "reconfigure")
            and sys.stdout.encoding.lower() != "utf-8"
        ):
            sys.stdout.reconfigure(encoding="utf-8")  # type: ignore
            sys.stderr.reconfigure(encoding="utf-8")  # type: ignore
    except Exception as e:
        print(f"Failed to fix UTF-8 encoding: {e}")
