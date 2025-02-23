"""Main NordVPN client implementation.

This module contains the main Client class that extends the base NordVPNClient to add:
- OpenVPN connection management
- Status checking and monitoring
- Connection state persistence
- Error handling and recovery
"""

import json
import os, sys
import random
import signal
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, TypedDict, Union, cast

import psutil
from loguru import logger
import requests
from dotenv import load_dotenv
import shutil
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.logging import RichHandler

load_dotenv()
logger.configure(
    handlers=[
        {
            "sink": RichHandler(),
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        }
    ]
)

from ._templates import OPENVPN_TEMPLATE
from .base import NordVPNClient
from .models import (
    ConnectionError,
    CredentialsError,
    ServerError,
    DisconnectionError,
    VPNError,
)
from .utils import (
    API_HEADERS,
    CACHE_DIR,
    CONFIG_DIR,
    DATA_DIR,
    NORDVPN_COUNTRY_IDS,
    OPENVPN_AUTH,
    OPENVPN_CONFIG,
    OPENVPN_LOG,
    load_vpn_state,
    save_vpn_state,
)

# Constants
PACKAGE_DIR = Path(__file__).parent
CACHE_FILE = DATA_DIR / "countries.json"

# Rich console for pretty output
console = Console()


# Store cache in the package directory
COUNTRIES_CACHE = PACKAGE_DIR / "data" / "countries.json"


# Type definitions for country data
class City(TypedDict):
    """City information from NordVPN API."""

    dns_name: str
    hub_score: int
    id: int
    latitude: float
    longitude: float
    name: str
    serverCount: int


class Country(TypedDict):
    """Country information from NordVPN API."""

    cities: List[City]
    code: str
    id: int
    name: str
    serverCount: int


class CountryCache(TypedDict):
    """Cache file structure."""

    countries: List[Country]
    last_updated: str


# Fallback country list in case API is unreachable
FALLBACK_DATA: CountryCache = {
    "countries": [
        {
            "cities": [
                {
                    "dns_name": "new-york",
                    "hub_score": 0,
                    "id": 8971718,
                    "latitude": 40.7141667,
                    "longitude": -74.0063889,
                    "name": "New York",
                    "serverCount": 529,
                }
            ],
            "code": "US",
            "id": 228,
            "name": "United States",
            "serverCount": 529,
        },
        {
            "cities": [
                {
                    "dns_name": "london",
                    "hub_score": 0,
                    "id": 2989907,
                    "latitude": 51.514125,
                    "longitude": -0.093689,
                    "name": "London",
                    "serverCount": 785,
                }
            ],
            "code": "GB",
            "id": 227,
            "name": "United Kingdom",
            "serverCount": 785,
        },
        {
            "cities": [
                {
                    "dns_name": "frankfurt",
                    "hub_score": 0,
                    "id": 2215709,
                    "latitude": 50.116667,
                    "longitude": 8.683333,
                    "name": "Frankfurt",
                    "serverCount": 301,
                }
            ],
            "code": "DE",
            "id": 81,
            "name": "Germany",
            "serverCount": 301,
        },
    ],
    "last_updated": "2024-02-23T00:00:00Z",
}

# Cache expiry in seconds (24 hours)
CACHE_EXPIRY = 24 * 60 * 60


class Client(NordVPNClient):
    """NordVPN client for managing VPN connections."""

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        verbose: bool = False,
    ):
        """Initialize NordVPN client."""
        username_str = username or os.getenv("NORD_USER")
        password_str = password or os.getenv("NORD_PASSWORD")
        if not username_str or not password_str:
            raise CredentialsError(
                "NORD_USER and NORD_PASSWORD environment variables must be set"
            )
        super().__init__(username_str, password_str, verbose)
        self.country: Optional[str] = None
        self._initial_ip: Optional[str] = None
        self._connected_ip: Optional[str] = None
        self._server: Optional[str] = None
        self._country_name: Optional[str] = None
        self.logger = logger
        self.logger.add(sys.stdout, level="DEBUG" if self.verbose else "INFO")

        # Load saved state
        state = load_vpn_state()
        self._initial_ip = state.get("initial_ip")
        self._connected_ip = state.get("connected_ip")
        self._server = state.get("server")
        self._country_name = state.get("country")

    BASE_API_URL: str = "https://api.nordvpn.com/v1"

    def _create_auth_file(self) -> None:
        """Create auth file with credentials."""
        OPENVPN_AUTH.write_text(f"{self.username}\n{self.password}")
        OPENVPN_AUTH.chmod(0o600)

    def _save_state(self) -> None:
        """Save current connection state."""
        state = {
            "connected": self.is_protected(),
            "initial_ip": self._initial_ip,  # This will be converted to non_vpn_ip if disconnected
            "connected_ip": self._connected_ip,
            "server": self._server,
            "country": self._country_name,
            "timestamp": time.time(),
        }
        save_vpn_state(state)

    def fetch_server_info(
        self, country: str | None = None
    ) -> Optional[Tuple[str, str]]:
        """Fetch information about a recommended server that supports OpenVPN.

        Args:
            country: Optional 2-letter country code (e.g. 'us', 'uk')
        """
        # Add browser-like headers to avoid 403
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://nordvpn.com/",
            "Origin": "https://nordvpn.com",
        }

        url = f"{self.BASE_API_URL}/servers/recommendations"
        params = {
            "filters[servers_technologies][identifier]": "openvpn_tcp",
            "limit": "5",  # Get top 5 servers to show stats
        }

        if country:
            # Get country ID from mapping
            country_id = NORDVPN_COUNTRY_IDS.get(country.upper())
            if not country_id:
                raise ServerError(f"Country code '{country}' not found")
            params["filters[country_id]"] = country_id

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not isinstance(data, list) or not data:
                # If no servers found with initial query, try without technology filter
                params.pop("filters[servers_technologies][identifier]", None)
                response = requests.get(url, params=params, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()

            if not isinstance(data, list) or not data:
                raise ServerError(
                    f"No servers available{' in ' + country.upper() if country else ''}"
                )

            # Show server stats if verbose
            if self.verbose:
                table = Table(
                    title=f"Available servers in {country if country else 'recommended locations'}"
                )
                table.add_column("Server", style="cyan")
                table.add_column("Load", justify="right")

                for server in data:
                    load = server.get("load", 0)
                    hostname = server.get("hostname", "")
                    # Color code based on load
                    load_style = (
                        "green" if load < 30 else "yellow" if load < 70 else "red"
                    )
                    table.add_row(hostname, f"[{load_style}]{load}%[/{load_style}]")

                console.print(table)

            # Select the server with lowest load
            server = min(data, key=lambda x: x.get("load", 100))
            hostname = server.get("hostname")
            if not isinstance(hostname, str) or not hostname:
                raise ServerError(
                    f"Invalid server data received for {country if country else 'recommended locations'}"
                )

            return hostname, server.get("station", "")

        except requests.RequestException as e:
            raise ServerError(f"Failed to fetch server info: {e}")

    def list_countries(self, use_cache: bool = True) -> List[Country]:
        """Fetch a list of all available server countries from the NordVPN API.

        Args:
            use_cache: Whether to use cached country list (default: True)
                     If False, forces a fresh fetch from the API

        Returns:
            List of dictionaries containing country information
        """
        try:
            url = f"{self.BASE_API_URL}/servers/countries"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            countries: List[Country] = response.json()

            # Cache the fresh data
            cache_data: CountryCache = {
                "countries": countries,
                "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            self._cache_countries(cache_data)
            return countries

        except requests.RequestException as e:
            self.logger.warning(f"Failed to fetch countries: {e}")
            # Try to use cache regardless of use_cache setting
            cached = self._get_cached_countries()
            if cached:
                return cached["countries"]

            # If no cache available, use fallback list
            return FALLBACK_DATA["countries"]

    def _get_cached_countries(self) -> Optional[CountryCache]:
        """Get cached country list if available and not expired."""
        try:
            if not COUNTRIES_CACHE.exists():
                return None

            # Check if cache is expired
            if time.time() - COUNTRIES_CACHE.stat().st_mtime > CACHE_EXPIRY:
                return None

            with COUNTRIES_CACHE.open("r") as f:
                return json.load(f)

        except (json.JSONDecodeError, OSError):
            return None

    def _cache_countries(self, data: CountryCache) -> None:
        """Cache the country list to disk.

        Args:
            data: Dictionary containing countries list and last_updated timestamp
        """
        try:
            COUNTRIES_CACHE.parent.mkdir(parents=True, exist_ok=True)
            with COUNTRIES_CACHE.open("w") as f:
                json.dump(data, f, indent=2, sort_keys=True)
            COUNTRIES_CACHE.chmod(0o644)  # Make readable for all users
        except OSError:
            pass  # Silently fail if caching isn't possible

    def connect(self, country: str | None = None, max_retries: int = 5) -> bool:
        """Connect to a NordVPN server.

        Args:
            country: Optional 2-letter country code (e.g. 'us', 'uk')
            max_retries: Number of connection retry attempts
        """
        raise NotImplementedError("Use go() method instead")

    def status(self) -> dict:
        """Get current VPN status."""
        try:
            # First try the more reliable IP API
            response = requests.get("https://api.ipify.org?format=json", timeout=5)
            response.raise_for_status()
            current_ip = response.json().get("ip")
            if self.verbose:
                self.logger.debug(f"Current IP: {current_ip}")

            # Load cached state
            state = load_vpn_state()
            initial_ip = state.get("initial_ip")
            connected_ip = state.get("connected_ip")
            if self.verbose:
                self.logger.debug(f"Initial IP: {initial_ip}")
                self.logger.debug(f"Connected IP: {connected_ip}")

            # Check if OpenVPN is running
            openvpn_running = False
            for proc in psutil.process_iter(["name"]):
                if proc.info["name"] == "openvpn":
                    openvpn_running = True
                    break
            if self.verbose:
                self.logger.debug(f"OpenVPN running: {openvpn_running}")

            # Then check if it's a NordVPN IP
            try:
                response = requests.get(
                    "https://nordvpn.com/wp-admin/admin-ajax.php?action=get_user_info_data",
                    headers=API_HEADERS,
                    timeout=5,
                )
                response.raise_for_status()
                nord_data = response.json()
                if self.verbose:
                    self.logger.debug(f"NordVPN data: {nord_data}")

                # We're connected if:
                # 1. OpenVPN is running AND
                # 2. Current IP matches our last known VPN IP OR NordVPN recognizes the IP
                # 3. Current IP is different from our initial non-VPN IP
                is_connected = (
                    openvpn_running
                    and (current_ip == connected_ip or nord_data.get("status", False))
                    and (not initial_ip or current_ip != initial_ip)
                )

                # Additional check - if we're not connected but OpenVPN is running and IP matches connected_ip,
                # we might have stale state
                if not is_connected and openvpn_running and current_ip == connected_ip:
                    is_connected = True

                if self.verbose:
                    self.logger.debug(f"Connection status: {is_connected}")
                    self.logger.debug(f"Status check conditions:")
                    self.logger.debug(f"  1. OpenVPN running: {openvpn_running}")
                    self.logger.debug(
                        f"  2a. Current IP matches connected IP: {current_ip == connected_ip}"
                    )
                    self.logger.debug(
                        f"  2b. NordVPN recognizes IP: {nord_data.get('status', False)}"
                    )
                    self.logger.debug(
                        f"  3. Current IP differs from initial: {not initial_ip or current_ip != initial_ip}"
                    )

                if is_connected:
                    # Update state to ensure it's fresh
                    state = {
                        "connected": True,
                        "initial_ip": initial_ip or self._initial_ip,
                        "connected_ip": current_ip,
                        "server": self._server or state.get("server"),
                        "country": self._country_name or state.get("country"),
                        "timestamp": time.time(),
                    }
                    save_vpn_state(state)
                    if self.verbose:
                        self.logger.debug("Updated state with connected status")

                return {
                    "status": is_connected,
                    "ip": current_ip,
                    "country": nord_data.get(
                        "country", state.get("country", "Unknown")
                    ),
                    "city": nord_data.get("city", "Unknown"),
                    "server": state.get("server"),
                }
            except requests.RequestException:
                # If NordVPN API check fails, use process and IP check
                # We're connected if:
                # 1. OpenVPN is running AND
                # 2. Current IP matches our last known VPN IP
                # 3. Current IP is different from our initial non-VPN IP
                is_connected = (
                    openvpn_running
                    and current_ip == connected_ip
                    and (not initial_ip or current_ip != initial_ip)
                )

                # Additional check - if we're not connected but OpenVPN is running and IP matches connected_ip,
                # we might have stale state
                if not is_connected and openvpn_running and current_ip == connected_ip:
                    is_connected = True

                if is_connected:
                    # Update state to ensure it's fresh
                    state = {
                        "connected": True,
                        "initial_ip": initial_ip or self._initial_ip,
                        "connected_ip": current_ip,
                        "server": self._server or state.get("server"),
                        "country": self._country_name or state.get("country"),
                        "timestamp": time.time(),
                    }
                    save_vpn_state(state)

                return {
                    "status": is_connected,
                    "ip": current_ip,
                    "country": state.get("country", "Unknown"),
                    "city": "Unknown",
                    "server": state.get("server"),
                }

        except Exception as e:
            raise ConnectionError(f"Failed to get status: {e}")

    def is_protected(self) -> bool:
        """Check if VPN is active by verifying IP change."""
        try:
            # Get current IP
            response = requests.get("https://api.ipify.org?format=json", timeout=5)
            response.raise_for_status()
            current_ip = response.json().get("ip")

            # Load state to get initial and connected IPs
            state = load_vpn_state()
            initial_ip = state.get("initial_ip")
            connected_ip = state.get("connected_ip")

            # If we don't have an initial IP yet, store this one
            if not initial_ip and not self._initial_ip:
                self._initial_ip = current_ip
                state = {
                    "connected": False,
                    "initial_ip": current_ip,
                    "connected_ip": None,
                    "server": None,
                    "country": None,
                    "timestamp": time.time(),
                }
                save_vpn_state(state)
                return False

            # Check if OpenVPN is running
            openvpn_running = False
            for proc in psutil.process_iter(["name"]):
                if proc.info["name"] == "openvpn":
                    openvpn_running = True
                    break

            # Connection is active if:
            # 1. OpenVPN is running AND
            # 2. Current IP matches our last known VPN IP
            # 3. Current IP is different from our initial non-VPN IP
            is_connected = (
                openvpn_running
                and current_ip == connected_ip
                and (not initial_ip or current_ip != initial_ip)
            )

            # Additional check - if we're not connected but OpenVPN is running and IP matches connected_ip,
            # we might have stale state
            if not is_connected and openvpn_running and current_ip == connected_ip:
                is_connected = True

            return is_connected

        except Exception:
            return False

    def go(self, country_code: str) -> None:
        """Connect to VPN in specified country."""
        try:
            # Always disconnect any existing connection first
            try:
                if self.verbose:
                    self.logger.info("Ensuring no existing VPN connection...")
                self.disconnect(verbose=self.verbose)
                time.sleep(2)  # Wait for cleanup
            except Exception as e:
                self.logger.warning(f"Error during disconnect: {e}")

            # Get fresh initial IP after disconnect
            try:
                response = requests.get("https://api.ipify.org?format=json", timeout=5)
                response.raise_for_status()
                self._initial_ip = response.json().get("ip")
                # Save initial state
                state = {
                    "connected": False,
                    "initial_ip": self._initial_ip,
                    "connected_ip": None,
                    "server": None,
                    "country": None,
                    "timestamp": time.time(),
                }
                save_vpn_state(state)
                if self.verbose:
                    self.logger.info(f"Normal IP: {self._initial_ip}")
                else:
                    console.print(f"[cyan]Normal IP:[/cyan] {self._initial_ip}")
            except Exception as e:
                self.logger.warning(f"Failed to get normal IP: {e}")

            country = self.get_country_by_code(country_code)
            if not country:
                raise ValueError(f"Country code '{country_code}' not found")

            if self.verbose:
                self.logger.info(f"Connecting to {country['name']}")

            # Get server info using the API
            server_info = self.fetch_server_info(country_code)
            if not server_info:
                raise ConnectionError("Failed to get server information")

            hostname, ip = server_info
            self._server = hostname
            self._country_name = country["name"]

            if self.verbose:
                self.logger.info(f"Selected server: {hostname}")
            else:
                console.print(f"[cyan]Server:[/cyan] {hostname}")

            # Create auth file and set up OpenVPN
            self._create_auth_file()
            config = OPENVPN_TEMPLATE.format(ip, hostname)
            OPENVPN_CONFIG.write_text(config)
            OPENVPN_CONFIG.chmod(0o600)

            cmd = [
                "sudo",
                "openvpn",
                "--config",
                str(OPENVPN_CONFIG),
                "--auth-user-pass",
                str(OPENVPN_AUTH),
                "--daemon",
                "--verb",
                str(3),
                "--connect-retry",
                str(2),
                "--connect-timeout",
                str(30),
                "--resolv-retry",
                "infinite",
                "--log",
                str(OPENVPN_LOG),
                "--ping",
                str(10),
                "--ping-restart",
                str(60),
                "--persist-tun",
                "--persist-key",
            ]

            if self.verbose:
                self.logger.debug(f"Running command: {' '.join(cmd)}")

            # Start OpenVPN
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Failed to start OpenVPN: {e}")
                raise ConnectionError("Failed to start OpenVPN")

            # Wait for connection with progress spinner
            start_time = time.time()
            initial_ip = self._initial_ip
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                disable=not self.verbose,
            ) as progress:
                task = progress.add_task("Connecting...", total=None)
                while time.time() - start_time < 60:
                    try:
                        # Check OpenVPN process
                        openvpn_running = False
                        for proc in psutil.process_iter(["name"]):
                            if "openvpn" in proc.info["name"]:
                                openvpn_running = True
                                break

                        if not openvpn_running:
                            if OPENVPN_LOG.exists():
                                log_content = OPENVPN_LOG.read_text()
                                if "AUTH_FAILED" in log_content:
                                    raise ConnectionError(
                                        "Authentication failed - check your credentials"
                                    )
                                elif "TLS Error" in log_content:
                                    raise ConnectionError(
                                        "TLS handshake failed - server may be down"
                                    )
                            raise ConnectionError("OpenVPN process died unexpectedly")

                        # Check if IP has changed
                        status = self.status()
                        current_ip = status.get("ip")

                        if current_ip and current_ip != initial_ip:
                            self._connected_ip = current_ip
                            # Save full state with all connection details
                            state = {
                                "connected": True,
                                "initial_ip": self._initial_ip,
                                "connected_ip": current_ip,
                                "server": self._server,
                                "country": self._country_name,
                                "timestamp": time.time(),
                            }
                            save_vpn_state(state)

                            if self.verbose:
                                self.logger.info(
                                    f"Successfully connected to {country['name']}"
                                )
                                self.logger.info(f"Private IP: {current_ip}")
                            else:
                                console.print(f"[cyan]Private IP:[/cyan] {current_ip}")
                            return

                        if self.verbose:
                            progress.update(
                                task, description="Waiting for VPN connection..."
                            )
                    except Exception as e:
                        if self.verbose:
                            self.logger.debug(f"Connection check error: {e}")

                    time.sleep(2)

            # If we get here, connection failed
            self.disconnect(verbose=self.verbose)
            raise ConnectionError("Failed to establish VPN connection after 60 seconds")

        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            self.disconnect(verbose=self.verbose)
            raise

    def flush(self) -> None:
        """Terminate all running OpenVPN processes."""
        try:
            # First try graceful shutdown
            for proc in psutil.process_iter(attrs=["name", "pid"]):
                if proc.info["name"] == "openvpn":
                    try:
                        # Try SIGTERM first
                        subprocess.run(
                            ["sudo", "kill", str(proc.info["pid"])],
                            check=True,
                            timeout=5,
                        )
                    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                        # If SIGTERM fails, force kill
                        subprocess.run(
                            ["sudo", "kill", "-9", str(proc.info["pid"])], check=True
                        )

            # Double check no processes remain
            time.sleep(1)
            for proc in psutil.process_iter(attrs=["name"]):
                if proc.info["name"] == "openvpn":
                    raise DisconnectionError(
                        "Failed to terminate all OpenVPN processes"
                    )

        except Exception as e:
            if isinstance(e, DisconnectionError):
                raise
            raise DisconnectionError(f"Failed to flush OpenVPN processes: {e}")

    def disconnect(self, verbose: bool = True) -> None:
        """Disconnect from the current server and clean up."""
        try:
            # Kill all OpenVPN processes
            self.flush()

            # Save disconnected state
            state = {
                "connected": False,
                "initial_ip": None,  # Reset initial IP so we get a fresh one next connect
                "connected_ip": None,
                "server": None,
                "country": None,
                "timestamp": time.time(),
            }
            save_vpn_state(state)

            # Reset instance state
            self._initial_ip = None
            self._connected_ip = None
            self._server = None
            self._country_name = None

            # Clean up files
            for file in [OPENVPN_CONFIG, OPENVPN_AUTH, OPENVPN_LOG]:
                if file.exists():
                    file.unlink()

            # Wait briefly for network to stabilize
            time.sleep(1)

            if verbose:
                print("Disconnected from VPN")
        except Exception as e:
            raise DisconnectionError(f"Error during disconnect: {e}")
