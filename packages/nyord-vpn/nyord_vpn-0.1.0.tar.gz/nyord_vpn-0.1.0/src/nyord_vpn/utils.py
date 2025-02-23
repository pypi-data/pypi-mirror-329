"""Utility functions and constants for the NordVPN client.

This module contains:
- Logger configuration
- Path constants
- Country ID mapping
- API request headers
- Cache settings
"""

import json
from loguru import logger
from pathlib import Path
from platformdirs import user_cache_dir, user_config_dir
import time, sys

# Application directories
APP_NAME = "nyord-vpn"
APP_AUTHOR = "twardoch"
CACHE_DIR = Path(user_cache_dir(APP_NAME, APP_AUTHOR))
CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))

# Ensure directories exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# File paths
PACKAGE_DIR = Path(__file__).parent
DATA_DIR = PACKAGE_DIR / "data"
CACHE_FILE = DATA_DIR / "countries.json"
COUNTRIES_CACHE = CACHE_DIR / "countries.json"
COUNTRY_IDS_FILE = DATA_DIR / "country_ids.json"
STATE_FILE = CACHE_DIR / "vpn_state.json"
OPENVPN_CONFIG = CACHE_DIR / "openvpn.ovpn"
OPENVPN_AUTH = CACHE_DIR / "openvpn.auth"
OPENVPN_LOG = CACHE_DIR / "openvpn.log"

# Cache expiry in seconds (24 hours)
CACHE_EXPIRY = 24 * 60 * 60  # 24 hours in seconds


def ensure_data_dir() -> None:
    """Ensure the data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


# Create data directory if it doesn't exist
ensure_data_dir()


# Load country IDs from JSON file
try:
    with open(COUNTRY_IDS_FILE) as f:
        NORDVPN_COUNTRY_IDS: dict[str, str] = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    # Fallback data if file doesn't exist or is invalid
    NORDVPN_COUNTRY_IDS = {
        "US": "228",  # United States
        "GB": "227",  # United Kingdom
        "DE": "81",  # Germany
    }

# Browser-like headers for API requests
API_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://nordvpn.com/",
    "Origin": "https://nordvpn.com",
}


def save_vpn_state(state: dict) -> None:
    """Save VPN connection state to file.

    The state includes:
    - connected: bool - current connection status
    - initial_ip: str - the original IP before VPN connection
    - connected_ip: str - the IP address when connected to VPN
    - server: str - current VPN server hostname
    - country: str - current VPN server country
    - timestamp: float - when the state was last updated
    """
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2))
    except Exception as e:
        logger.warning(f"Failed to save VPN state: {e}")


def load_vpn_state() -> dict:
    """Load VPN connection state from file."""
    try:
        if STATE_FILE.exists():
            state = json.loads(STATE_FILE.read_text())
            # State is valid for 5 minutes
            if time.time() - state.get("timestamp", 0) < 300:
                return state
    except Exception as e:
        logger.warning(f"Failed to load VPN state: {e}")

    return {
        "connected": False,
        "initial_ip": None,  # Original IP before VPN connection
        "connected_ip": None,  # IP address when connected to VPN
        "server": None,
        "country": None,
        "timestamp": time.time(),
    }
