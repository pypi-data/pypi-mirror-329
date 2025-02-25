import os
import requests
from paic_patterns import __version__
import logging

logger = logging.getLogger(name="paic_patterns")


def pattern_warning(spec_pattern: str) -> None:
    """
    Emit a warning if an experimental spec pattern is being used.
    """
    if spec_pattern == "list-director":
        logger.warning(
            "🟡 Experimental Pattern: list-director",
            extra={
                "rich_type": "panel",
                "value": "list-director is experimental. Use with caution.",
            },
        )


def need_to_upgrade_application() -> bool:
    # Read the custom domain from an environment variable
    version_url = f"https://paicpatterns.com/version.txt"
    try:
        response = requests.get(version_url, timeout=5)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if __version__ != latest_version:
                logger.info(f"🟡 Version check: {__version__} != {latest_version}")
                return True
            return False
        else:
            # If the HTTP status is not 200, assume no upgrade.
            return False
    except Exception:
        # In case of any request errors, assume no upgrade is needed.
        return False
