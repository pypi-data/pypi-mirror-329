import logging
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler
from rich.syntax import Syntax
from rich.panel import Panel
import json
import time


class RichMessageHandler(RichHandler):
    """Rich handler that supports metadata-based formatting"""

    def render_message(self, record: logging.LogRecord, message: str):
        if hasattr(record, "rich_type") and hasattr(record, "value"):
            if record.rich_type == "json":
                syntax = Syntax(
                    json.dumps(record.value, indent=2),
                    "json",
                    theme="monokai",
                    word_wrap=True,
                )
                return Panel(syntax, title=message)
            elif record.rich_type == "code":
                syntax = Syntax(
                    record.value,
                    getattr(record, "language", "python"),
                    theme="monokai",
                    word_wrap=True,
                )
                return Panel(syntax, title=message)
            elif record.rich_type == "panel":
                return Panel(str(record.value), title=message)
            elif record.rich_type == "text":
                return f"{message} `{record.value}`"
        return message


class FileFormatter(logging.Formatter):
    """Custom formatter that maintains rich-style messages in log files"""

    def format(self, record: logging.LogRecord) -> str:
        # First format with the standard formatter
        formatted_msg = super().format(record)

        # If it's a rich message with metadata, format it appropriately
        if hasattr(record, "rich_type") and hasattr(record, "value"):
            if record.rich_type == "json":
                json_str = json.dumps(record.value, indent=2)
                formatted_msg = f"{formatted_msg}\n```json\n{json_str}\n```"
            elif record.rich_type == "code":
                lang = getattr(record, "language", "python")
                formatted_msg = f"{formatted_msg}\n```{lang}\n{record.value}\n```"
            elif record.rich_type == "panel":
                formatted_msg = f"{formatted_msg}\n---\n{record.value}\n---"
            elif record.rich_type == "text":
                formatted_msg = f"{formatted_msg} `{record.value}`"

        return formatted_msg


def setup_logging(log_file: Optional[str] = None, level: int = logging.INFO):
    """Set up logging with rich console output and formatted file output."""
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

    file_handler = logging.FileHandler(log_file)
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
