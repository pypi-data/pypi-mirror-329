"""Integration tests for validation."""

import os
import pytest

from nyord_vpn.core.exceptions import VPNError
from nyord_vpn.api.njord import NjordVPNClient
from nyord_vpn.api.legacy import LegacyVPNClient


@pytest.fixture(autouse=True)
def clear_env():
    """Clear environment variables before each test."""
    os.environ.pop("NORD_USER", None)
    os.environ.pop("NORD_PASSWORD", None)
    yield
    os.environ.pop("NORD_USER", None)
    os.environ.pop("NORD_PASSWORD", None)


def test_invalid_credentials_njord():
    """Test invalid credentials with Njord API."""
    with pytest.raises(VPNError, match="Missing credentials"):
        NjordVPNClient()


def test_invalid_credentials_legacy():
    """Test invalid credentials with Legacy API."""
    with pytest.raises(VPNError, match="Missing credentials"):
        LegacyVPNClient()


def test_invalid_country_njord():
    """Test invalid country with Njord API."""
    os.environ["NORD_USER"] = "test_user"
    os.environ["NORD_PASSWORD"] = "test_pass"
    with pytest.raises(VPNError):
        client = NjordVPNClient()
        client.connect("Invalid Country")


def test_invalid_country_legacy():
    """Test invalid country with Legacy API."""
    os.environ["NORD_USER"] = "test_user"
    os.environ["NORD_PASSWORD"] = "test_pass"
    with pytest.raises(VPNError):
        client = LegacyVPNClient()
        client.connect("Invalid Country")
