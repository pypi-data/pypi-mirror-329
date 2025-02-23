"""Integration tests for VPN connection."""

import asyncio
import pytest

from nyord_vpn.core.exceptions import VPNError, VPNConnectionError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_connection_success(
    mock_client,
    mock_aiohttp_session,
    mock_subprocess,
    mock_pycountry,
    mock_env_credentials,
):
    """Test successful VPN connection."""
    # Test primary API
    async with mock_client as client:
        await client.connect()
        status = await client.status()
        assert status["connected"] is True
        assert status["country"] == "Test Country"
        assert status["ip"] == "1.2.3.4"
        assert status["server"] == "test.server.com"

    # Test fallback API
    mock_client.primary_api.connect.side_effect = VPNError("Primary API failed")
    async with mock_client as client:
        await client.connect()
        status = await client.status()
        assert status["connected"] is True
        assert status["country"] == "Test Country"
        assert status["ip"] == "1.2.3.4"
        assert status["server"] == "test.server.com"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_connection_failure(
    mock_client,
    mock_aiohttp_session,
    mock_subprocess,
    mock_pycountry,
    mock_env_credentials,
):
    """Test VPN connection failure handling."""
    # Test primary API failure
    mock_client.primary_api.connect.side_effect = VPNError("Primary API failed")
    mock_client.fallback_api.connect.side_effect = VPNError("Fallback API failed")

    with pytest.raises(VPNConnectionError, match="Both primary and fallback failed"):
        async with mock_client as client:
            await client.connect()

    # Test network error
    mock_aiohttp_session.get.side_effect = asyncio.TimeoutError()
    with pytest.raises(VPNConnectionError, match="Failed to connect"):
        async with mock_client as client:
            await client.connect()

    # Test subprocess error
    mock_subprocess.side_effect = Exception("Subprocess error")
    with pytest.raises(VPNConnectionError, match="Failed to connect"):
        async with mock_client as client:
            await client.connect()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_country_selection(
    mock_client,
    mock_aiohttp_session,
    mock_subprocess,
    mock_pycountry,
    mock_env_credentials,
):
    """Test VPN country selection."""
    # Test valid country
    async with mock_client as client:
        await client.connect("Test Country")
        status = await client.status()
        assert status["country"] == "Test Country"

    # Test invalid country
    mock_client.primary_api.connect.side_effect = VPNError("Invalid country")
    mock_client.fallback_api.connect.side_effect = VPNError("Invalid country")
    with pytest.raises(VPNConnectionError, match="Invalid country"):
        async with mock_client as client:
            await client.connect("Invalid Country")
