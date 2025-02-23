# nyord-vpn

A simple and reliable NordVPN client for macOS with support for both legacy OpenVPN and njord APIs.

## Features

- Simple and reliable VPN connection management
- Support for both legacy OpenVPN and njord APIs
- Country selection
- Basic status monitoring
- Clear error messages
- Minimal dependencies

## Installation

```bash
# Install system requirements
brew install openvpn

# Install package
pip install nyord-vpn

# Optional: Install njord support
pip install nyord-vpn[njord]
```

## Usage

### Environment Variables

Set your NordVPN credentials:

```bash
export NORD_USER="your-username"
export NORD_PASSWORD="your-password"
```

### CLI Commands

```bash
# Connect to VPN (defaults to US)
nyord-vpn connect

# Connect to specific country
nyord-vpn connect --country netherlands

# Use njord API
nyord-vpn --api njord connect

# Enable debug logging
nyord-vpn --verbose connect

# Check status
nyord-vpn status

# List available countries
nyord-vpn list-countries

# Disconnect
nyord-vpn disconnect
```

### Python API

```python
from nyord_vpn.core.factory import create_client

# Create client (legacy or njord)
client = create_client("legacy")

# Connect to VPN
client.connect("netherlands")

# Check status
status = client.status()
print(f"Connected to {status['server']} ({status['ip']})")

# Disconnect
client.disconnect()
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Install optional njord support
pip install njord

# Run with debug logging
NORD_USER="username" NORD_PASSWORD="password" nyord-vpn --verbose connect
```

## Error Handling

The client uses simple retry logic for API calls and provides clear error messages. Common errors:

- `VPNCredentialsError`: Missing or invalid credentials
- `VPNConnectionError`: Failed to connect/disconnect
- `VPNConfigError`: Configuration issues (e.g., missing OpenVPN)
- `VPNServerError`: Failed to get server information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT 