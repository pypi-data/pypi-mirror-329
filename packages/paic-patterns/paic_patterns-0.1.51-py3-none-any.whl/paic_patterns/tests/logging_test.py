import os
import json
import tempfile
import pytest  # noqa: F401 - required for pytest to work
from paic_patterns.modules.logging import setup_logging


def test_rich_logging():
    """Test rich logging functionality with various metadata types"""
    # Create a temporary log file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Set up logging with our temp file
        logger = setup_logging(log_file=temp_path)

        # Test different types of rich logging
        test_data = {"name": "test", "value": 123, "nested": {"key": "value"}}
        logger.info("JSON Data", extra={"rich_type": "json", "value": test_data})

        code_snippet = "def hello():\n    print('world')"
        logger.info(
            "Python Code",
            extra={"rich_type": "code", "value": code_snippet, "language": "python"},
        )

        logger.info(
            "Important Message",
            extra={"rich_type": "panel", "value": "This is a highlighted message"},
        )

        logger.info("Status", extra={"rich_type": "text", "value": "SUCCESS"})

        # Regular log message without rich formatting
        logger.info("Regular log message")

        # Read the log file and verify the content
        with open(temp_path, "r") as f:
            log_content = f.read()

        # Verify JSON block
        assert "JSON Data" in log_content
        assert json.dumps(test_data, indent=2) in log_content

        # Verify code block
        assert "Python Code" in log_content
        assert "```python" in log_content
        assert code_snippet in log_content

        # Verify panel
        assert "Important Message" in log_content
        assert "This is a highlighted message" in log_content

        # Verify text
        assert "Status" in log_content
        assert "`SUCCESS`" in log_content

        # Verify regular message
        assert "Regular log message" in log_content

    finally:
        # Clean up the temporary file
        os.unlink(temp_path)
