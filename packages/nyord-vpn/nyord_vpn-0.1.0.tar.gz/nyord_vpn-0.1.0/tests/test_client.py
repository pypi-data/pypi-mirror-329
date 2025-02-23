"""Tests for VPN client."""

import pytest

from nyord_vpn.core.exceptions import VPNError


def test_client_connect(mock_client):
    """Test VPN client connect."""
    # Test successful connection
    result = mock_client.connect("Test Country")
    assert result is True

    # Test connection status
    status = mock_client.status()
    assert status["connected"] is True
    assert status["country"] == "Test Country"
    assert status["ip"] == "1.2.3.4"
    assert status["server"] == "test.server.com"


def test_client_disconnect(mock_client):
    """Test VPN client disconnect."""
    # Connect first
    mock_client.connect("Test Country")

    # Test disconnection
    result = mock_client.disconnect()
    assert result is True

    # Test status after disconnect
    status = mock_client.status()
    assert status["connected"] is False


def test_client_list_countries(mock_client):
    """Test VPN client country listing."""
    countries = mock_client.list_countries()
    assert isinstance(countries, list)
    assert len(countries) > 0
    assert all(isinstance(c, dict) for c in countries)
    assert all("name" in c and "code" in c for c in countries)


def test_client_error_handling(mock_client, mocker):
    """Test VPN client error handling."""
    # Mock API to raise error
    mocker.patch.object(
        mock_client._connect,
        "__call__",
        side_effect=VPNError("Test error"),
    )

    # Test error handling
    with pytest.raises(VPNError, match="Test error"):
        mock_client.connect("Test Country")


@pytest.mark.asyncio
async def test_client_context_manager(mock_client):
    """Test VPN client context manager."""
    async with mock_client as client:
        # Test connection inside context
        result = await client.connect("Test Country")
        assert result is True

        # Test status
        status = await client.status()
        assert status["connected"] is True

    # Test auto-disconnect after context
    status = await mock_client.status()
    assert status["connected"] is False
