"""Base NordVPN client implementation.

This module contains the base NordVPN client class that handles:
- Country list management
- Cache handling
- Location lookup
- API interaction

This class is extended by the main Client class to add connection functionality.
"""

import json
import time, sys
from typing import List, Optional
import requests
from loguru import logger

from .models import City, Country, CountryCache
from .utils import (
    CACHE_FILE,
    COUNTRIES_CACHE,
    CACHE_EXPIRY,
    API_HEADERS,
)

# Fallback data in case API is unreachable
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


class NordVPNClient:
    """Base NordVPN client for managing country data and API interactions."""

    BASE_API_URL: str = "https://api.nordvpn.com/v1"

    def __init__(self, username: str, password: str, verbose: bool = False):
        """Initialize NordVPN client.

        Args:
            username: NordVPN username
            password: NordVPN password
            verbose: Whether to enable verbose logging
        """
        self.username = username
        self.password = password
        self.verbose = verbose
        self.logger = logger
        self.cache_file = CACHE_FILE
        self.countries = self._load_countries()
        self.logger.add(sys.stdout, level="DEBUG" if self.verbose else "INFO")

    def _load_countries(self) -> List[Country]:
        """Load countries from cache or fallback data."""
        try:
            with open(self.cache_file, "r") as f:
                cache_data: CountryCache = json.load(f)
                return cache_data["countries"]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.warning(f"Failed to load cache: {e}. Using fallback data.")
            return FALLBACK_DATA["countries"]

    def get_country_by_code(self, code: str) -> Optional[Country]:
        """Get country by its code.

        Args:
            code: Two-letter country code (e.g. 'us', 'uk')
        """
        code = code.upper()
        for country in self.countries:
            if country["code"] == code:
                return country
        return None

    def get_country_by_name(self, name: str) -> Optional[Country]:
        """Get country by its name.

        Args:
            name: Country name (case-insensitive)
        """
        name = name.lower()
        for country in self.countries:
            if country["name"].lower() == name:
                return country
        return None

    def get_available_locations(self) -> List[str]:
        """Get list of available locations with server counts."""
        locations = []
        for country in sorted(self.countries, key=lambda x: x["name"]):
            total_servers = country["serverCount"]
            locations.append(
                f"{country['name']} ({country['code'].lower()}) - {total_servers} servers"
            )
            for city in sorted(country["cities"], key=lambda x: x["name"]):
                locations.append(f"  {city['name']} - {city['serverCount']} servers")
        return locations

    def get_best_city(self, country_code: str) -> Optional[City]:
        """Get the best city in a country based on hub score and server count.

        Args:
            country_code: Two-letter country code
        """
        country = self.get_country_by_code(country_code)
        if not country:
            return None

        # Sort cities by hub score (higher is better) and server count
        sorted_cities = sorted(
            country["cities"],
            key=lambda x: (x["hub_score"], x["serverCount"]),
            reverse=True,
        )
        return sorted_cities[0] if sorted_cities else None

    def list_countries(self, use_cache: bool = True) -> List[Country]:
        """Fetch a list of all available server countries from the NordVPN API.

        Args:
            use_cache: Whether to use cached country list (default: True)
                     If False, forces a fresh fetch from the API

        Returns:
            List of dictionaries containing country information
        """
        try:
            if use_cache:
                cached = self._get_cached_countries()
                if cached:
                    return cached["countries"]

            url = f"{self.BASE_API_URL}/servers/countries"
            response = requests.get(url, headers=API_HEADERS, timeout=10)
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

        except (json.JSONDecodeError, OSError) as e:
            self.logger.warning(f"Failed to load country cache: {e}")
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
        except OSError as e:
            self.logger.warning(f"Failed to cache countries: {e}")
