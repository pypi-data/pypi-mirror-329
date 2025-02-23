#!/usr/bin/env -S uv run
# /// script
# dependencies = ["requests", "rich"]
# ///

"""Script to fetch and update the country list from NordVPN API."""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, TypedDict, Union

import requests
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn


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


def fetch_countries() -> List[Country]:
    """Fetch countries from NordVPN API."""
    url = "https://api.nordvpn.com/v1/servers/countries"

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(
            description="Fetching country list from NordVPN API...", total=None
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()

    # The API already returns the exact structure we want
    countries: List[Country] = response.json()
    return sorted(countries, key=lambda x: x["name"])


def main() -> None:
    """Update the country list cache file."""
    try:
        # Get package data directory
        package_dir = Path(__file__).parent.parent
        data_dir = package_dir / "data"
        cache_file = data_dir / "countries.json"

        # Ensure data directory exists
        data_dir.mkdir(parents=True, exist_ok=True)

        # Fetch fresh data
        countries = fetch_countries()

        # Calculate total servers across all countries
        total_servers = sum(country["serverCount"] for country in countries)
        total_cities = sum(len(country["cities"]) for country in countries)

        # Prepare cache data
        cache_data: CountryCache = {
            "countries": countries,
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

        # Save to file
        with cache_file.open("w") as f:
            json.dump(cache_data, f, indent=2, sort_keys=True)
        cache_file.chmod(0o644)

        rprint(f"[green]✓ Updated country list cache with:[/green]")
        rprint(f"  • [cyan]{len(countries)}[/cyan] countries")
        rprint(f"  • [cyan]{total_cities}[/cyan] cities")
        rprint(f"  • [cyan]{total_servers}[/cyan] servers")
        rprint(f"[blue]Cache file: {cache_file}[/blue]")

    except requests.RequestException as e:
        rprint(f"[red]✗ Failed to fetch country list: {e}[/red]")
        sys.exit(1)
    except (OSError, json.JSONDecodeError) as e:
        rprint(f"[red]✗ Failed to update cache file: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
