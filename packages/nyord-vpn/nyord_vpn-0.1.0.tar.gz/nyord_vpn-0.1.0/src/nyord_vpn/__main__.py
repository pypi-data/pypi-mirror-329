"""Command line interface for nyord-vpn."""

import os
import sys
from typing import List, Optional
import json
from datetime import datetime
import subprocess
import time

import fire
from rich.console import Console
from rich.table import Table

from .client import Client, VPNError
from .scripts.update_countries import fetch_countries

console = Console()


def _check_root() -> None:
    """Request root privileges using sudo."""
    if os.geteuid() != 0:
        try:
            # Re-run the script with sudo
            args = ["sudo", sys.executable] + sys.argv
            console.print(
                "[yellow]This command requires administrator privileges.[/yellow]"
            )
            console.print("[cyan]Please enter your password when prompted.[/cyan]")
            subprocess.run(args, check=True)
            sys.exit(0)
        except subprocess.CalledProcessError:
            console.print("[red]Error: Administrator privileges required.[/red]")
            console.print("[yellow]Please run the command again with sudo:[/yellow]")
            console.print(f"[blue]sudo {' '.join(sys.argv)}[/blue]")
            sys.exit(1)


class CLI:
    """NordVPN CLI interface."""

    def __init__(self, verbose: bool = False):
        """Initialize CLI."""
        try:
            self.client = Client(verbose=verbose)
        except VPNError as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)

    def go(self, country_code: str) -> None:
        """Connect to VPN in specified country.

        Args:
            country_code: Two-letter country code (e.g. 'us', 'uk')
        """
        _check_root()
        try:
            # First check if we're already connected
            status = self.client.status()
            if status and status.get("status", False):
                console.print("[yellow]Already connected to VPN.[/yellow]")
                console.print(f"Private IP: [cyan]{status.get('ip', 'Unknown')}[/cyan]")
                console.print(
                    f"Country: [cyan]{status.get('country', 'Unknown')}[/cyan]"
                )
                console.print(f"Server: [cyan]{status.get('server', 'Unknown')}[/cyan]")
                console.print("\n[yellow]Please disconnect first with:[/yellow]")
                console.print("[blue]sudo nyord-vpn bye[/blue]")
                sys.exit(1)

            # Connect to VPN
            self.client.go(country_code)
        except VPNError as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)

    def bye(self) -> None:
        """Disconnect from VPN."""
        _check_root()
        try:
            # First check if we're actually connected
            status = self.client.status()
            if not status or not status.get("status", False):
                console.print("[yellow]Not connected to VPN[/yellow]")
                console.print(f"Normal IP: [cyan]{status.get('ip', 'Unknown')}[/cyan]")
                return

            # Store the private IP for display
            private_ip = status.get("ip", "Unknown")

            # Disconnect
            self.client.disconnect()

            # Get new status for normal IP
            status = self.client.status()
            console.print("[green]Successfully disconnected from VPN[/green]")
            console.print(f"Normal IP: [cyan]{status.get('ip', 'Unknown')}[/cyan]")
            console.print(f"Previous Private IP: [yellow]{private_ip}[/yellow]")
        except VPNError as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)

    def info(self) -> None:
        """Show current connection info."""
        try:
            status = self.client.status()
            if status:
                connected = status.get("status", False)
                ip = status.get("ip", "Unknown")
                country = status.get("country", "Unknown")
                server = status.get("server", "Unknown")

                if connected:
                    console.print("[green]VPN Status: Connected[/green]")
                    console.print(f"Private IP: [cyan]{ip}[/cyan]")
                    console.print(f"Country: [cyan]{country}[/cyan]")
                    console.print(f"Server: [cyan]{server}[/cyan]")
                else:
                    console.print("[yellow]VPN Status: Not Connected[/yellow]")
                    console.print(f"Normal IP: [cyan]{ip}[/cyan]")
            else:
                console.print("[yellow]VPN Status: Not Connected[/yellow]")
                console.print(f"Normal IP: [cyan]{status.get('ip', 'Unknown')}[/cyan]")
        except VPNError as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)

    def where(self, live: bool = False) -> None:
        """List available countries.

        Args:
            live: If True, fetch fresh data from API instead of using cache
        """
        try:
            if live:
                countries = fetch_countries()
            else:
                countries = self.client.countries

            table = Table(title="Available Countries")
            table.add_column("Country", style="cyan")
            table.add_column("Code", style="yellow")
            table.add_column("Servers", justify="right", style="green")
            table.add_column("Cities", justify="right", style="blue")

            for country in sorted(countries, key=lambda x: x["name"]):
                table.add_row(
                    country["name"],
                    country["code"].lower(),
                    str(country["serverCount"]),
                    str(len(country["cities"])),
                )

            console.print(table)
            total_servers = sum(country["serverCount"] for country in countries)
            total_cities = sum(len(country["cities"]) for country in countries)
            console.print(
                f"\nTotal: [cyan]{len(countries)}[/cyan] countries, "
                f"[blue]{total_cities}[/blue] cities, "
                f"[green]{total_servers}[/green] servers"
            )

        except VPNError as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)

    def update(self) -> None:
        """Update country list from NordVPN API."""
        try:
            countries = fetch_countries()
            total_servers = sum(country["serverCount"] for country in countries)
            total_cities = sum(len(country["cities"]) for country in countries)

            with open(self.client.cache_file, "w") as f:
                json.dump(
                    {
                        "countries": countries,
                        "last_updated": time.strftime(
                            "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
                        ),
                    },
                    f,
                    indent=2,
                )

            console.print("[green]✓ Updated country list cache with:[/green]")
            console.print(f"  • [cyan]{len(countries)}[/cyan] countries")
            console.print(f"  • [blue]{total_cities}[/blue] cities")
            console.print(f"  • [green]{total_servers}[/green] servers")
            console.print(f"[blue]Cache file: {self.client.cache_file}[/blue]")

        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)


def main() -> None:
    """Main entry point."""
    try:
        fire.Fire(CLI)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
