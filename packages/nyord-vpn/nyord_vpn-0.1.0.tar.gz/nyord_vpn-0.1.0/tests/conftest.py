"""Test fixtures and configuration."""

from unittest.mock import patch
import json

import pytest

from nyord_vpn.core.client import VPNClient


@pytest.fixture
def mock_env_credentials(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("NORD_USER", "test_user")
    monkeypatch.setenv("NORD_PASSWORD", "test_pass")


@pytest.fixture
def mock_openvpn():
    """Mock OpenVPN command."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = b"OpenVPN 2.5.0\n"
        yield mock_run


@pytest.fixture
def mock_requests():
    """Mock requests for API calls."""
    with patch("requests.get") as mock_get:
        # Mock server recommendations
        mock_get.return_value.json.return_value = [
            {"hostname": "test.server.com", "load": 10, "status": "online"}
        ]
        mock_get.return_value.status_code = 200
        yield mock_get


@pytest.fixture
def mock_process():
    """Mock subprocess for OpenVPN."""
    with patch("subprocess.Popen") as mock_popen:
        mock_popen.return_value.pid = 12345
        mock_popen.return_value.returncode = 0
        yield mock_popen


@pytest.fixture
def mock_client(mock_env_credentials, mock_openvpn, mock_requests, mock_process):
    """Create a mock VPN client."""
    with patch("nyord_vpn.api.legacy.LegacyVPNClient") as mock_legacy:
        # Setup mock APIs
        mock_legacy.return_value.connect.return_value = True
        mock_legacy.return_value.disconnect.return_value = True
        mock_legacy.return_value.status.return_value = {
            "connected": True,
            "country": "Test Country",
            "ip": "1.2.3.4",
            "server": "test.server.com",
        }
        mock_legacy.return_value.list_countries.return_value = [
            {"name": "Country 1", "code": "1"},
            {"name": "Country 2", "code": "2"},
        ]

        # Create client
        client = VPNClient()
        yield client


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file."""
    config = {
        "username": "test_user",
        "password": "test_pass",
        "default_country": "us",
        "use_legacy_fallback": True,
    }

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config))
    return config_file


@pytest.fixture
def mock_ip_info():
    """Mock IP info response."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "ip": "1.2.3.4",
            "country": "US",
            "org": "NordVPN",
        }
        mock_get.return_value.status_code = 200
        yield mock_get
