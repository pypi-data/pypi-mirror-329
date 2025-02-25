"""Member commands for managing API keys."""

import typer
import logging
from ..modules.member_runner import set_api_key, view_api_key, report_issue

logger = logging.getLogger(name="paic_patterns")

app = typer.Typer(
    name="member",
    help="""
Manage PAIC Patterns membership and API key.

---

Commands:
1. Set API key: `paic member set-key <apikey>`
2. View current API key: `paic member view`
""",
)


@app.command("set-key")
def set_key(api_key: str = typer.Argument(..., help="The API key to set")) -> None:
    """
    Command Name:
        Set API Key

    Usage Template:
        paic member set-key <apikey>

    Description:
        Set and validate your PAIC Patterns API key.
        The key will be stored in ~/.paic_patterns.config.yml

    Example Usage:
        paic member set-key paic-member-1234567890
    """
    set_api_key(api_key)


@app.command("view")
def view() -> None:
    """
    Command Name:
        View API Key

    Usage Template:
        paic member view

    Description:
        View your current PAIC Patterns API key and its last validation time.

    Example Usage:
        paic member view
    """
    view_api_key()


@app.command("report-issue")
def report_issue_cmd(
    issue_description: str = typer.Argument(
        ..., help="Description of the issue to report"
    ),
    no_chat_history: bool = typer.Option(
        False, "--no-chat-history", help="Do not include chat history in the report"
    ),
) -> None:
    """
    Command Name:
        Report Issue

    Usage Template:
        paic member report-issue <issue description> [--no-chat-history]

    Description:
        Uploads diagnostic files (paic-patterns.log and .aider.chat.history.md) along with an issue description to help diagnose the reported issue.
        By default, the chat history file is included unless the --no-chat-history option is used.
        The log files are truncated to include only the most recent 1MB if they exceed 5MB in size.
        The API key is validated before sending the report; if invalid, an error is raised.

    Example Usage:
        paic member report-issue "The app crashes on startup"
        paic member report-issue "The app crashes on startup" --no-chat-history
    """
    report_issue(issue_description, no_chat_history)
