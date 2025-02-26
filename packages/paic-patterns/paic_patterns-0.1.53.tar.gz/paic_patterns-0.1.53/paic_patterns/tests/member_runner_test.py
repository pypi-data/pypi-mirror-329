import pytest
import yaml
import time
import logging
from unittest.mock import patch, Mock
from ..modules.member_runner import (
    set_api_key,
    validate_api_key,
    view_api_key,
    CONFIG_FILE_PATH,
    VALIDATION_INTERVAL_HOURS,
)
from ..modules.data_types import ApiPaicApiKeyResponse


@pytest.fixture
def mock_config_file(tmp_path):
    """Create a temporary config file"""
    temp_config = tmp_path / "test_config.yml"
    with patch("paic_patterns.modules.member_runner.CONFIG_FILE_PATH", temp_config):
        yield temp_config


@pytest.fixture
def mock_successful_validation():
    """Mock a successful API key validation"""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "type": "validate",
            "success": True,
            "error": None,
        }
        yield mock_post


@pytest.fixture
def mock_failed_validation():
    """Mock a failed API key validation"""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "type": "validate",
            "success": False,
            "error": "Invalid API key",
        }
        yield mock_post


def test_set_api_key_success(mock_config_file, mock_successful_validation):
    """Test setting a valid API key"""
    api_key = "test_key_123"
    set_api_key(api_key)

    # Verify config file was created with correct data
    config = yaml.safe_load(mock_config_file.read_text())
    assert config["api_key"] == api_key
    assert "last_validation" in config
    assert isinstance(config["last_validation"], int)


def test_set_api_key_failure(mock_config_file, mock_failed_validation):
    """Test setting an invalid API key"""
    api_key = "invalid_key"
    with pytest.raises(ValueError, match="Invalid API key"):
        set_api_key(api_key)

    # Verify config file was not created
    assert (
        not mock_config_file.exists()
        or yaml.safe_load(mock_config_file.read_text()) == {}
    )


def test_validate_api_key_success(mock_config_file, mock_successful_validation):
    """Test validating a valid API key"""
    # Set up initial config
    config = {
        "api_key": "test_key_123",
        "last_validation": int(time.time() * 1000),
    }
    mock_config_file.write_text(yaml.safe_dump(config))

    assert validate_api_key() is True


def test_validate_api_key_no_key(mock_config_file):
    """Test validation when no API key is set"""
    assert validate_api_key() is False


def test_validate_api_key_expired(mock_config_file, mock_successful_validation):
    """Test validation of an expired API key"""
    # Set up initial config with old validation timestamp
    config = {
        "api_key": "test_key_123",
        "last_validation": int(
            (time.time() - (VALIDATION_INTERVAL_HOURS + 1) * 3600) * 1000
        ),
    }
    mock_config_file.write_text(yaml.safe_dump(config))

    assert validate_api_key() is True

    # Verify last_validation was updated
    updated_config = yaml.safe_load(mock_config_file.read_text())
    assert updated_config["last_validation"] > config["last_validation"]


def test_validate_api_key_failure(mock_config_file, mock_failed_validation):
    """Test validation of an invalid API key"""
    # Set up initial config
    config = {
        "api_key": "invalid_key",
        "last_validation": int(
            (time.time() - (VALIDATION_INTERVAL_HOURS + 1) * 3600) * 1000
        ),
    }
    mock_config_file.write_text(yaml.safe_dump(config))

    assert validate_api_key() is False


@pytest.mark.parametrize(
    "config,expected_calls",
    [
        (
            {"api_key": "test_key", "last_validation": int(time.time() * 1000)},
            0,
        ),  # Recent validation
        (
            {
                "api_key": "test_key",
                "last_validation": int(
                    (time.time() - (VALIDATION_INTERVAL_HOURS - 0.5) * 3600) * 1000
                ),
            },
            0,
        ),  # Not yet expired
        (
            {
                "api_key": "test_key",
                "last_validation": int(
                    (time.time() - (VALIDATION_INTERVAL_HOURS + 0.5) * 3600) * 1000
                ),
            },
            1,
        ),  # Just expired
    ],
)
def test_validate_api_key_interval(
    mock_config_file, mock_successful_validation, config, expected_calls
):
    """Test that validation respects the bi-hourly interval"""
    mock_config_file.write_text(yaml.safe_dump(config))
    validate_api_key()
    assert mock_successful_validation.call_count == expected_calls


def test_view_api_key_exists(mock_config_file, caplog):
    """Test viewing an existing API key"""
    config = {
        "api_key": "test_key_123",
        "last_validation": int(time.time() * 1000),
    }
    mock_config_file.write_text(yaml.safe_dump(config))

    with patch("paic_patterns.modules.member_runner.logger.info") as mock_logger:
        view_api_key()
        mock_logger.assert_called_once()
        args, kwargs = mock_logger.call_args
        assert "Current API Key" in args[0]
        assert kwargs.get("extra", {}).get("rich_type") == "panel"
        assert "test_key_123" in kwargs.get("extra", {}).get("value", "")


def test_view_api_key_not_exists(mock_config_file, caplog):
    """Test viewing when no API key exists"""
    with patch("paic_patterns.modules.member_runner.logger.info") as mock_logger:
        view_api_key()
        mock_logger.assert_called_once()
        args, kwargs = mock_logger.call_args
        assert "No API key set" in args[0]
        assert kwargs.get("extra", {}).get("rich_type") == "panel"
        assert "No API key is currently set" in kwargs.get("extra", {}).get("value", "")


import pytest
import yaml
import time
import logging
from unittest.mock import patch, Mock
from ..modules.member_runner import (
    set_api_key,
    validate_api_key,
    view_api_key,
    CONFIG_FILE_PATH,
    VALIDATION_INTERVAL_HOURS,
)
from ..modules.data_types import ApiPaicApiKeyResponse


@pytest.fixture
def mock_config_file(tmp_path):
    """Create a temporary config file"""
    temp_config = tmp_path / "test_config.yml"
    with patch("paic_patterns.modules.member_runner.CONFIG_FILE_PATH", temp_config):
        yield temp_config


@pytest.fixture
def mock_successful_validation():
    """Mock a successful API key validation"""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "type": "validate",
            "success": True,
            "error": None,
        }
        yield mock_post


@pytest.fixture
def mock_failed_validation():
    """Mock a failed API key validation"""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "type": "validate",
            "success": False,
            "error": "Invalid API key",
        }
        yield mock_post


def test_set_api_key_success(mock_config_file, mock_successful_validation):
    """Test setting a valid API key"""
    api_key = "test_key_123"
    set_api_key(api_key)

    # Verify config file was created with correct data
    config = yaml.safe_load(mock_config_file.read_text())
    assert config["api_key"] == api_key
    assert "last_validation" in config
    assert isinstance(config["last_validation"], int)


def test_set_api_key_failure(mock_config_file, mock_failed_validation):
    """Test setting an invalid API key"""
    api_key = "invalid_key"
    with pytest.raises(ValueError, match="Invalid API key"):
        set_api_key(api_key)

    # Verify config file was not created
    assert (
        not mock_config_file.exists()
        or yaml.safe_load(mock_config_file.read_text()) == {}
    )


def test_validate_api_key_success(mock_config_file, mock_successful_validation):
    """Test validating a valid API key"""
    # Set up initial config
    config = {
        "api_key": "test_key_123",
        "last_validation": int(time.time() * 1000),
    }
    mock_config_file.write_text(yaml.safe_dump(config))

    assert validate_api_key() is True


def test_validate_api_key_no_key(mock_config_file):
    """Test validation when no API key is set"""
    assert validate_api_key() is False


def test_validate_api_key_expired(mock_config_file, mock_successful_validation):
    """Test validation of an expired API key"""
    # Set up initial config with old validation timestamp
    config = {
        "api_key": "test_key_123",
        "last_validation": int(
            (time.time() - (VALIDATION_INTERVAL_HOURS + 1) * 3600) * 1000
        ),
    }
    mock_config_file.write_text(yaml.safe_dump(config))

    assert validate_api_key() is True

    # Verify last_validation was updated
    updated_config = yaml.safe_load(mock_config_file.read_text())
    assert updated_config["last_validation"] > config["last_validation"]


def test_validate_api_key_failure(mock_config_file, mock_failed_validation):
    """Test validation of an invalid API key"""
    # Set up initial config
    config = {
        "api_key": "invalid_key",
        "last_validation": int(
            (time.time() - (VALIDATION_INTERVAL_HOURS + 1) * 3600) * 1000
        ),
    }
    mock_config_file.write_text(yaml.safe_dump(config))

    assert validate_api_key() is False


@pytest.mark.parametrize(
    "config,expected_calls",
    [
        (
            {"api_key": "test_key", "last_validation": int(time.time() * 1000)},
            0,
        ),  # Recent validation
        (
            {
                "api_key": "test_key",
                "last_validation": int(
                    (time.time() - (VALIDATION_INTERVAL_HOURS - 0.5) * 3600) * 1000
                ),
            },
            0,
        ),  # Not yet expired
        (
            {
                "api_key": "test_key",
                "last_validation": int(
                    (time.time() - (VALIDATION_INTERVAL_HOURS + 0.5) * 3600) * 1000
                ),
            },
            1,
        ),  # Just expired
    ],
)
def test_validate_api_key_interval(
    mock_config_file, mock_successful_validation, config, expected_calls
):
    """Test that validation respects the bi-hourly interval"""
    mock_config_file.write_text(yaml.safe_dump(config))
    validate_api_key()
    assert mock_successful_validation.call_count == expected_calls


def test_view_api_key_exists(mock_config_file, caplog):
    """Test viewing an existing API key"""
    config = {
        "api_key": "test_key_123",
        "last_validation": int(time.time() * 1000),
    }
    mock_config_file.write_text(yaml.safe_dump(config))

    with patch("paic_patterns.modules.member_runner.logger.info") as mock_logger:
        view_api_key()
        mock_logger.assert_called_once()
        args, kwargs = mock_logger.call_args
        assert "Current API Key" in args[0]
        assert kwargs.get("extra", {}).get("rich_type") == "panel"
        assert "test_key_123" in kwargs.get("extra", {}).get("value", "")
        assert "Config File:" in kwargs.get("extra", {}).get("value", "")


def test_view_api_key_not_exists(mock_config_file, caplog):
    """Test viewing when no API key exists"""
    with patch("paic_patterns.modules.member_runner.logger.info") as mock_logger:
        view_api_key()
        mock_logger.assert_called_once()
        args, kwargs = mock_logger.call_args
        assert "No API key set" in args[0]
        assert kwargs.get("extra", {}).get("rich_type") == "panel"
        assert "No API key is currently set" in kwargs.get("extra", {}).get("value", "")


def test_report_issue_success(monkeypatch):
    import time
    import requests
    from paic_patterns.modules.member_runner import report_issue

    # Set up a temporary configuration with a valid API key
    temp_config = {
        "api_key": "valid_test_key",
        "last_validation": int(time.time() * 1000),
    }
    monkeypatch.setattr(
        "paic_patterns.modules.member_runner._load_config", lambda: temp_config
    )

    # Force _validate_api_key to succeed
    monkeypatch.setattr(
        "paic_patterns.modules.member_runner._validate_api_key",
        lambda key: (True, None),
    )

    # Create a dummy response for a successful report issue submission
    class DummyResponse:
        def json(self):
            return {"success": True}

    monkeypatch.setattr(requests, "post", lambda url, json: DummyResponse())

    # Call report_issue; no exception should be raised
    report_issue("Test issue report", no_chat_history=True)


def test_report_issue_invalid_api_key(monkeypatch):
    import time
    import pytest
    from paic_patterns.modules.member_runner import report_issue

    # Set up a temporary configuration with an invalid API key
    temp_config = {
        "api_key": "invalid_test_key",
        "last_validation": int(time.time() * 1000),
    }
    monkeypatch.setattr(
        "paic_patterns.modules.member_runner._load_config", lambda: temp_config
    )

    # Force _validate_api_key to fail
    monkeypatch.setattr(
        "paic_patterns.modules.member_runner._validate_api_key",
        lambda key: (False, "Invalid key for testing"),
    )

    # Assert that report_issue raises a ValueError because of the invalid API key
    with pytest.raises(ValueError, match="Invalid key for testing"):
        report_issue("Test issue report", no_chat_history=False)
