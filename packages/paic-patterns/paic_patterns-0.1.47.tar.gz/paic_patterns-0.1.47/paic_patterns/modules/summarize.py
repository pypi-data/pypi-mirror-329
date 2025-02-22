import subprocess
import time
import logging
from datetime import datetime
from typing import Optional
from .logging import log_panel

logger = logging.getLogger(name="paic_patterns")

def get_git_diff_stats() -> str:
    """Run git diff --stat and return output."""
    try:
        result = subprocess.run(['git', 'diff', '--stat'], 
                              capture_output=True, 
                              text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error getting git diff stats: {str(e)}"

def format_duration(start_time: float) -> str:
    """Format duration from start time to now."""
    duration = time.time() - start_time
    return f"{duration:.2f} seconds"

def display_run_summary(start_time: float,
                       success: bool = True,
                       error: Optional[Exception] = None) -> None:
    """Display summary panel with timing and git diff stats."""
    duration = format_duration(start_time)
    diff_stats = get_git_diff_stats()
    
    summary = f"""Duration: {duration}

Git Diff Stats:
{diff_stats}"""

    if not success:
        summary += f"\n\nError: {str(error)}"

    emoji = "✅" if success else "❌"
    logger.info(
        f"{emoji} Run Summary",
        extra={
            "rich_type": "panel",
            "value": summary,
        }
    )
