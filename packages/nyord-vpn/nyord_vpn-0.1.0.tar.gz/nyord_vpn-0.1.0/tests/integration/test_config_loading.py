"""Integration tests for configuration loading."""

import pytest
from pathlib import Path
import json

from nyord_vpn.core.client import VPNClient
from nyord_vpn.core.config import VPNConfig
from tests.conftest import TEST_PASSWORD, TEST_USERNAME


@pytest.mark.integration
async def test_file_loading(temp_dir):
    """Test configuration loading from file."""
    # Create config file with all options
    config_file = temp_dir / "config.json"
    config_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD.get_secret_value(),
        "default_country": "Sweden",
        "retry_attempts": 5,
        "use_legacy_fallback": False,
        "config_dir": "custom/config/dir",
        "api_timeout": 60,
    }
    config_file.write_text(json.dumps(config_data))

    # Test loading with VPNClient
    client = VPNClient.from_file(config_file)
    assert client.config.username == TEST_USERNAME
    assert client.config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()
    assert client.config.default_country == "Sweden"
    assert client.config.retry_attempts == 5
    assert client.config.use_legacy_fallback is False
    assert client.config.config_dir == Path("custom/config/dir").resolve()
    assert client.config.api_timeout == 60

    # Test loading with VPNConfig
    config = VPNConfig.from_file(config_file)
    assert config.username == TEST_USERNAME
    assert config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()
    assert config.default_country == "Sweden"
    assert config.retry_attempts == 5
    assert config.use_legacy_fallback is False
    assert config.config_dir == Path("custom/config/dir").resolve()
    assert config.api_timeout == 60


@pytest.mark.integration
async def test_environment_loading_unprefixed(monkeypatch):
    """Test configuration loading from unprefixed environment variables."""
    # Set environment variables
    monkeypatch.setenv("NORD_USER", TEST_USERNAME)
    monkeypatch.setenv("NORD_PASSWORD", TEST_PASSWORD.get_secret_value())
    monkeypatch.setenv("NORDVPN_DEFAULT_COUNTRY", "Norway")
    monkeypatch.setenv("NORDVPN_RETRY_ATTEMPTS", "4")

    # Test loading with VPNClient
    client = VPNClient.from_env()
    assert client.config.username == TEST_USERNAME
    assert client.config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()
    assert client.config.default_country == "Norway"
    assert client.config.retry_attempts == 4


@pytest.mark.integration
async def test_environment_loading_prefixed(monkeypatch):
    """Test configuration loading from prefixed environment variables."""
    # Set environment variables
    monkeypatch.setenv("NORDVPN_USERNAME", TEST_USERNAME)
    monkeypatch.setenv("NORDVPN_PASSWORD", TEST_PASSWORD.get_secret_value())
    monkeypatch.setenv("NORDVPN_DEFAULT_COUNTRY", "Sweden")
    monkeypatch.setenv("NORDVPN_RETRY_ATTEMPTS", "5")

    # Test loading with VPNClient
    client = VPNClient.from_env()
    assert client.config.username == TEST_USERNAME
    assert client.config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()
    assert client.config.default_country == "Sweden"
    assert client.config.retry_attempts == 5


@pytest.mark.integration
async def test_environment_loading_precedence(monkeypatch):
    """Test precedence between prefixed and unprefixed environment variables."""
    # Set both prefixed and unprefixed variables
    monkeypatch.setenv("NORD_USER", "unprefixed_user")
    monkeypatch.setenv("NORD_PASSWORD", "unprefixed_pass")
    monkeypatch.setenv("NORDVPN_USERNAME", "prefixed_user")
    monkeypatch.setenv("NORDVPN_PASSWORD", "prefixed_pass")

    # Unprefixed should take precedence
    client = VPNClient.from_env()
    assert client.config.username == "unprefixed_user"
    assert client.config.password.get_secret_value() == "unprefixed_pass"


@pytest.mark.integration
async def test_default_values():
    """Test configuration default values."""
    # Test with minimal configuration
    config = VPNConfig(username="test", password="test")
    assert config.username == "test"
    assert config.password.get_secret_value() == "test"
    assert config.default_country == "United States"
    assert config.retry_attempts == 3
    assert config.use_legacy_fallback is True
    assert config.config_dir == Path.home() / ".config" / "nyord-vpn"
    assert config.api_timeout == 30

    # Test with VPNClient
    client = VPNClient(username="test", password="test")
    assert client.config.username == "test"
    assert client.config.password.get_secret_value() == "test"
    assert client.config.default_country == "United States"
    assert client.config.retry_attempts == 3
    assert client.config.use_legacy_fallback is True
    assert client.config.config_dir == Path.home() / ".config" / "nyord-vpn"
    assert client.config.api_timeout == 30


@pytest.mark.integration
async def test_config_file_precedence(temp_dir, monkeypatch):
    """Test configuration loading precedence between file and environment."""
    # Create config file
    config_file = temp_dir / "config.json"
    config_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD.get_secret_value(),
        "default_country": "Sweden",
        "retry_attempts": 5,
    }
    config_file.write_text(json.dumps(config_data))

    # Set environment variables
    monkeypatch.setenv("NORD_USER", "env_user")
    monkeypatch.setenv("NORD_PASSWORD", "env_pass")
    monkeypatch.setenv("NORDVPN_DEFAULT_COUNTRY", "Norway")
    monkeypatch.setenv("NORDVPN_API_TIMEOUT", "45")

    # Test with VPNClient - explicit args > file > env > defaults
    client = VPNClient.from_file(
        config_file,
        username="arg_user",
        password=TEST_PASSWORD.get_secret_value(),
    )
    assert client.config.username == "arg_user"  # From arg
    assert (
        client.config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()
    )  # From arg
    assert client.config.default_country == "Sweden"  # From file
    assert client.config.retry_attempts == 5  # From file
    assert client.config.api_timeout == 45  # From env
    assert client.config.use_legacy_fallback is True  # Default

    # Test with VPNConfig - file > env > defaults
    config = VPNConfig.from_file(config_file)
    assert config.username == TEST_USERNAME  # From file
    assert (
        config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()
    )  # From file
    assert config.default_country == "Sweden"  # From file
    assert config.retry_attempts == 5  # From file
    assert config.api_timeout == 45  # From env
    assert config.use_legacy_fallback is True  # Default


@pytest.mark.integration
async def test_config_validation(temp_dir):
    """Test configuration validation."""
    # Test invalid retry attempts
    config_file = temp_dir / "invalid_retry.json"
    config_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD.get_secret_value(),
        "retry_attempts": 0,
    }
    config_file.write_text(json.dumps(config_data))
    with pytest.raises(ValueError, match="ensure this value is greater than 0"):
        VPNConfig.from_file(config_file)

    # Test invalid timeout
    config_file = temp_dir / "invalid_timeout.json"
    config_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD.get_secret_value(),
        "api_timeout": -1,
    }
    config_file.write_text(json.dumps(config_data))
    with pytest.raises(ValueError, match="ensure this value is greater than 0"):
        VPNConfig.from_file(config_file)

    # Test invalid config directory
    config_file = temp_dir / "invalid_dir.json"
    config_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD.get_secret_value(),
        "config_dir": "/nonexistent/dir",
    }
    config_file.write_text(json.dumps(config_data))
    with pytest.raises(ValueError, match="Failed to setup config directory"):
        VPNConfig.from_file(config_file)

    # Test missing required fields
    config_file = temp_dir / "missing_fields.json"
    config_data = {
        "default_country": "Sweden",
        "retry_attempts": 5,
    }
    config_file.write_text(json.dumps(config_data))
    with pytest.raises(ValueError, match="Field required"):
        VPNConfig.from_file(config_file)


def test_load_from_file(tmp_path: Path):
    """Test loading configuration from file."""
    # Create config file
    config_path = tmp_path / "config.json"
    config_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD.get_secret_value(),
        "api_timeout": 30,
        "retry_attempts": 5,
    }
    config_path.write_text(json.dumps(config_data))

    # Test client initialization from file
    client = VPNClient(config_file=config_path)
    assert client.config.username == TEST_USERNAME
    assert client.config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()
    assert client.config.api_timeout == 30
    assert client.config.retry_attempts == 5

    # Test direct config loading
    config = VPNConfig.from_file(config_path)
    assert config.username == TEST_USERNAME
    assert config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()
    assert config.api_timeout == 30
    assert config.retry_attempts == 5


def test_load_from_env(monkeypatch):
    """Test loading configuration from environment variables."""
    # Set environment variables
    monkeypatch.setenv("NORDVPN_USERNAME", TEST_USERNAME)
    monkeypatch.setenv("NORDVPN_PASSWORD", TEST_PASSWORD.get_secret_value())
    monkeypatch.setenv("NORDVPN_API_TIMEOUT", "30")
    monkeypatch.setenv("NORDVPN_RETRY_ATTEMPTS", "5")

    # Test client initialization from env
    client = VPNClient()  # Will load from env by default
    assert client.config.username == TEST_USERNAME
    assert client.config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()
    assert client.config.api_timeout == 30
    assert client.config.retry_attempts == 5

    # Test direct config loading
    config = VPNConfig.from_env()
    assert config.username == TEST_USERNAME
    assert config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()
    assert config.api_timeout == 30
    assert config.retry_attempts == 5


def test_direct_initialization():
    """Test direct initialization with parameters."""
    # Test config initialization
    config = VPNConfig(
        username=TEST_USERNAME, password=TEST_PASSWORD.get_secret_value()
    )
    assert config.username == TEST_USERNAME
    assert config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()

    # Test client initialization
    client = VPNClient(
        username=TEST_USERNAME, password=TEST_PASSWORD.get_secret_value()
    )
    assert client.config.username == TEST_USERNAME
    assert client.config.password.get_secret_value() == TEST_PASSWORD.get_secret_value()


def test_invalid_config_file(tmp_path: Path):
    """Test handling of invalid configuration files."""
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        VPNConfig.from_file(tmp_path / "nonexistent.json")

    # Test invalid JSON
    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text("invalid json content")
    with pytest.raises(json.JSONDecodeError):
        VPNConfig.from_file(invalid_path)

    # Test missing required fields
    empty_path = tmp_path / "empty.json"
    empty_path.write_text("{}")
    with pytest.raises(ValueError):
        VPNConfig.from_file(empty_path)


def test_invalid_environment(monkeypatch):
    """Test handling of invalid environment variables."""
    # Test missing required variables
    with pytest.raises(ValueError):
        VPNConfig.from_env()

    # Test invalid values
    monkeypatch.setenv("NORDVPN_USERNAME", TEST_USERNAME)
    monkeypatch.setenv("NORDVPN_PASSWORD", TEST_PASSWORD.get_secret_value())
    monkeypatch.setenv("NORDVPN_API_TIMEOUT", "invalid")
    with pytest.raises(ValueError):
        VPNConfig.from_env()
