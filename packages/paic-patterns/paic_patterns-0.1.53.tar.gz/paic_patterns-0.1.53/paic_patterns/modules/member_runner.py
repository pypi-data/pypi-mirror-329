import logging
import yaml
import time
from pathlib import Path
import requests
from typing import Optional, Tuple
from datetime import datetime
from .data_types import (
    ApiPaicApiKeyRequest,
    ApiPaicApiKeyResponse,
    ApiPaicReportIssueRequest,
    ApiPaicReportIssueResponse,
)
import os
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(name="paic_patterns")

# Constants
CONFIG_FILE_PATH = Path.home() / ".paic_patterns.config.yml"
API_KEY_VALIDATION_URL = (
    "https://us-central1-agentic-engineer.cloudfunctions.net/paicApiKeyManager"
)

API_KEY_VALIDATION_URL_LOCAL = (
    "http://127.0.0.1:5001/agentic-engineer/us-central1/paicApiKeyManager"
)


API_KEY_DOCS_URL = (
    "https://agenticengineer.com/principled-ai-coding/member-assets/paic-patterns"
)
VALIDATION_INTERVAL_HOURS = 2  # Bi-hourly validation

API_REPORT_ISSUE_URL = (
    "https://us-central1-agentic-engineer.cloudfunctions.net/paicPatternsReportIssue"
)
API_REPORT_ISSUE_URL_LOCAL = (
    "http://127.0.0.1:5001/agentic-engineer/us-central1/paicPatternsReportIssue"
)

USE_LOCAL_SERVERLESS_FUNCTIONS = os.getenv("USE_LOCAL_SERVERLESS_FUNCTIONS") == "true"


def _load_config() -> dict:
    """Load configuration from yaml file"""
    if not CONFIG_FILE_PATH.exists():
        return {}
    return yaml.safe_load(CONFIG_FILE_PATH.read_text()) or {}


def _save_config(config: dict) -> None:
    """Save configuration to yaml file"""
    CONFIG_FILE_PATH.write_text(yaml.safe_dump(config))


def _validate_api_key(api_key: str) -> Tuple[bool, Optional[str]]:
    """Validate API key against the validation endpoint"""

    try:
        request = ApiPaicApiKeyRequest(
            type="validate", paicApiKey=api_key, parentUserId=None
        )
        if USE_LOCAL_SERVERLESS_FUNCTIONS:
            logger.info("Using local serverless functions for API key validation")
            response = requests.post(
                API_KEY_VALIDATION_URL_LOCAL, json=request.model_dump()
            )
        else:
            response = requests.post(API_KEY_VALIDATION_URL, json=request.model_dump())

        response_data = response.json()

        # Ensure response_data is a dict before unpacking
        if not isinstance(response_data, dict):
            return False, "Invalid response format from server"

        api_response = ApiPaicApiKeyResponse(**response_data)
        return api_response.success, api_response.error

    except Exception as e:
        return False, str(e)


def set_api_key(api_key: str) -> None:
    """Set and validate the API key"""
    # Validate the API key first
    is_valid, error = _validate_api_key(api_key)

    if not is_valid:
        error_msg = f"❌ Invalid API key: {error if error else 'Unknown error'}"
        logger.error(
            error_msg,
            extra={
                "rich_type": "panel",
                "value": f"{error_msg}\n\nGet your API key from: {API_KEY_DOCS_URL}",
            },
        )
        raise ValueError(error_msg)

    # Save the validated key
    config = _load_config()
    config["api_key"] = api_key
    config["last_validation"] = int(time.time() * 1000)  # milliseconds
    _save_config(config)

    logger.info(
        "✅ API key set successfully",
        extra={"rich_type": "panel", "value": "API key has been validated and saved"},
    )


def validate_api_key() -> bool:
    """Check if API key exists and is valid"""
    config = _load_config()
    api_key = config.get("api_key")
    last_validation = config.get("last_validation", 0)

    if not api_key:
        error_msg = "❌ No API key found"
        logger.error(
            error_msg,
            extra={
                "rich_type": "panel",
                "value": f"{error_msg}\n\nPlease set your API key using:\npaic member set-key <apikey>\n\nGet your API key from: {API_KEY_DOCS_URL}",
            },
        )
        return False

    # Check if we need to validate (bi-hourly)
    now = int(time.time() * 1000)
    hours_since_validation = (now - last_validation) / (1000 * 60 * 60)

    if hours_since_validation >= VALIDATION_INTERVAL_HOURS:
        is_valid, error = _validate_api_key(api_key)

        if not is_valid:
            error_msg = (
                f"❌ API key validation failed: {error if error else 'Unknown error'}"
            )
            logger.error(
                error_msg,
                extra={
                    "rich_type": "panel",
                    "value": f"{error_msg}\n\nPlease set a new API key using:\npaic member set-key <apikey>\n\nGet your API key from: {API_KEY_DOCS_URL}",
                },
            )
            return False

        # Update last validation time
        config["last_validation"] = now
        _save_config(config)

    return True


def view_api_key() -> None:
    """View the current API key and its last validation time"""
    config = _load_config()
    api_key = config.get("api_key")

    if not api_key:
        logger.info(
            "🟡 No API key set",
            extra={
                "rich_type": "panel",
                "value": f"No API key is currently set.\n\nGet your API key from: {API_KEY_DOCS_URL}\nThen set it using: paic member set-key <apikey>",
            },
        )
        return

    logger.info(
        "🔑 Current API Key",
        extra={
            "rich_type": "panel",
            "value": f"API Key: {api_key}\nConfig File: {CONFIG_FILE_PATH}",
        },
    )


def report_issue(issue_description: str, no_chat_history: bool) -> None:
    config = _load_config()
    api_key = config.get("api_key")
    if not api_key:
        error_msg = "❌ No API key set. Please set your API key using: paic member set-key <apikey>"
        logger.error(error_msg, extra={"rich_type": "panel", "value": error_msg})
        raise ValueError(error_msg)

    # Validate API key using the internal call
    is_valid, error = _validate_api_key(api_key)
    if not is_valid:
        error_msg = (
            f"❌ API key validation failed: {error if error else 'Unknown error'}"
        )
        logger.error(error_msg, extra={"rich_type": "panel", "value": error_msg})
        raise ValueError(error_msg)

    # Helper to read files with size limits:
    def read_file_tail(
        file_path: str,
        *,
        max_size: int = 5 * 1024 * 1024,
        tail_size: int = 200000,  # 0.2MB limit for Firestore
    ) -> str:
        path = Path(file_path)
        if not path.exists():
            return ""
        content = path.read_text(encoding="utf-8")
        content_bytes = content.encode("utf-8")
        if len(content_bytes) > max_size:
            # Take only the tail part
            content = content_bytes[-tail_size:].decode("utf-8", errors="replace")
        elif len(content_bytes) > tail_size:
            # If content is between tail_size and max_size, trim to tail_size
            content = content_bytes[-tail_size:].decode("utf-8", errors="replace")
        return content

    log_content = read_file_tail("paic-patterns.log")
    chat_history_content = ""
    if not no_chat_history:
        chat_history_content = read_file_tail(".aider.chat.history.md")

    request_obj = ApiPaicReportIssueRequest(
        paicApiKey=api_key,
        issue_description=issue_description,
        no_chat_history=no_chat_history,
        log_file=log_content,
        chat_history_file=chat_history_content if not no_chat_history else None,
    )

    if USE_LOCAL_SERVERLESS_FUNCTIONS:
        logger.info("Using local serverless functions for issue reporting")
        url = API_REPORT_ISSUE_URL_LOCAL
    else:
        url = API_REPORT_ISSUE_URL

    try:
        response = requests.post(url, json=request_obj.model_dump())
        response_data = response.json()
        report_response = ApiPaicReportIssueResponse(**response_data)
        if report_response.success:
            logger.info(
                "✅ Issue reported successfully. You will be emailed with an update.",
                extra={
                    "rich_type": "panel",
                    "value": "Issue report uploaded successfully.",
                },
            )
        else:
            logger.error(
                "❌ Issue report failed",
                extra={"rich_type": "panel", "value": report_response.error},
            )
    except Exception as e:
        logger.error(
            f"❌ Failed to report issue: {str(e)}",
            extra={"rich_type": "panel", "value": str(e)},
        )
        raise
