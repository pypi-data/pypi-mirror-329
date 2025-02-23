"""Tests for LegacyVPNClient implementation."""

import pytest
import requests
import os
import subprocess

from nyord_vpn.core.exceptions import VPNError
from nyord_vpn.api.legacy import LegacyVPNClient


def test_init(mock_env_credentials, mock_openvpn):
    """Test LegacyVPNClient initialization."""
    api = LegacyVPNClient()
    assert api.username == os.getenv("NORD_USER")
    assert isinstance(api.password, str)
    assert api.password == os.getenv("NORD_PASSWORD")


def test_connect_success(
    mock_env_credentials, mock_openvpn, mock_requests, mock_process, mock_ip_info
):
    """Test successful connection."""
    api = LegacyVPNClient()
    assert api.connect() is True


def test_connect_failure(
    mock_env_credentials, mock_openvpn, mock_requests, mock_process
):
    """Test connection failure."""
    mock_process.side_effect = requests.RequestException("Failed to connect")
    api = LegacyVPNClient()
    with pytest.raises(VPNError, match="Failed to connect"):
        api.connect()


def test_disconnect_success(mock_env_credentials, mock_openvpn, mock_process):
    """Test successful disconnection."""
    api = LegacyVPNClient()
    assert api.disconnect() is True


def test_status_connected(mock_env_credentials, mock_openvpn, mock_ip_info):
    """Test status when connected."""
    api = LegacyVPNClient()
    status = api.status()
    assert status["connected"] is True
    assert status["country"] == "US"
    assert status["ip"] == "1.2.3.4"
    assert status["server"] == ""


def test_list_countries(mock_env_credentials, mock_openvpn, mock_requests):
    """Test listing available countries."""
    mock_requests.return_value.json.return_value = [
        {"name": "United States", "id": 228},
        {"name": "United Kingdom", "id": 227},
    ]
    api = LegacyVPNClient()
    countries = api.list_countries()
    assert len(countries) == 2
    assert all(isinstance(c, dict) for c in countries)
    assert all("name" in c and "code" in c for c in countries)
    assert countries[0]["name"] == "United Kingdom"
    assert countries[1]["name"] == "United States"


def test_openvpn_not_found(mock_env_credentials):
    """Test OpenVPN not found error."""
    with pytest.raises(VPNError, match="OpenVPN not found"):
        LegacyVPNClient()


def test_server_not_found(mock_env_credentials, mock_openvpn, mock_requests):
    """Test server not found error."""
    mock_requests.return_value.json.return_value = []
    api = LegacyVPNClient()
    with pytest.raises(VPNError, match="No servers found"):
        api.connect("invalid_country")


def test_config_download_error(mock_env_credentials, mock_openvpn, mock_requests):
    """Test config download error."""
    mock_requests.side_effect = requests.RequestException("Failed to download")
    api = LegacyVPNClient()
    with pytest.raises(VPNError, match="Failed to download"):
        api.connect()


def test_process_error(mock_env_credentials, mock_openvpn, mock_requests, mock_process):
    """Test process error handling."""
    mock_process.side_effect = subprocess.SubprocessError("Process failed")
    api = LegacyVPNClient()
    with pytest.raises(VPNError, match="Failed to connect"):
        api.connect()
