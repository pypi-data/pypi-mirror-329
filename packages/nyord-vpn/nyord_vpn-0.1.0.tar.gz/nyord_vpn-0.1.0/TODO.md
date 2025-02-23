# TODO

Do it! Remember, keep it simple, effective, eyes on the goal!

## 1. Core Implementation

- [x] **Legacy API (Shell Script Port)**
  - _Core Functionality_:
    - [x] Port server selection from shell script
      - [x] Use official NordVPN API v1 endpoints
      - [x] Add proper headers and timeouts
      - [x] Add server filtering for TCP only
    - [x] Implement OpenVPN config download and caching
      - [x] Use secure temp directory
      - [x] Download individual configs
      - [x] Add proper file permissions
    - [x] Add robust process management
      - [x] Graceful shutdown with fallback
      - [x] Proper process monitoring
      - [x] Complete cleanup on exit
    - [x] Add comprehensive status check
      - [x] Process status verification
      - [x] IP ownership validation
      - [x] Connection monitoring
  - _Error Handling_:
    - [x] Add specific error classes
    - [x] Implement retry with proper backoff
    - [x] Add detailed error messages
    - [x] Add comprehensive logging

## 2. Core Features

```python
# Use either API through the same interface
import nyord_vpn

# Legacy API (direct OpenVPN)
client = nyord_vpn.Client(country="de", api="legacy")
client.connect()      # Connects to VPN using legacy API
client.protected()    # Checks if connected
client.disconnect()   # Disconnects from VPN

# Njord API (modern API)
client = nyord_vpn.Client(country="de", api="njord")
client.connect()      # Connects to VPN using njord API
client.protected()    # Checks if connected
client.disconnect()   # Disconnects from VPN
```

## 3. Tasks

1. **Legacy API Engine** [!]

   - [ ] Fix server recommendations (403 errors)
   - [ ] Fix OpenVPN config download/caching
   - [ ] Fix process management
   - [ ] Fix status check via IP lookup

2. **Njord API Engine** [!]

   - [ ] Fix client initialization
   - [ ] Fix connection handling
   - [ ] Fix status check
   - [ ] Fix country selection

3. **Common Interface** [!]

   - [ ] Fix VPNClient initialization (config_file, username/password)
   - [ ] Implement unified connect/disconnect
   - [ ] Implement unified status check
   - [ ] Add basic error handling

4. **CLI Commands** [!]

   ```bash
   # Works the same with both APIs
   nyord-vpn --api njord connect de    # Connect using country code
   nyord-vpn --api legacy connect us   # Connect using country code
   nyord-vpn status                    # Check connection status
   nyord-vpn disconnect                # Disconnect VPN
   nyord-vpn list-countries           # List available countries
   ```

5. **Basic Tests** [!]
   - [ ] Test legacy API engine
   - [ ] Test njord API engine
   - [ ] Test common interface
   - [ ] Test CLI commands

## 4. Development

1. **Setup**

   ```bash
   # Create environment
   rm -rf .venv
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev,test]"

   # Install OpenVPN (needed for legacy API)
   brew install openvpn  # or apt install openvpn
   ```

2. **Test**

   ```bash
   hatch fmt --unsafe-fixes
   sudo hatch -e test run test
   ```

## 5. Dependencies

1. **System**

   - Python 3.10+
   - OpenVPN (for legacy API)
   - sudo access

2. **Python**
   - requests (API calls)
   - pydantic (config)
   - python-dotenv (auth)
   - loguru (logging)
   - fire (CLI)
   - rich (output)

Remember: Two engines (legacy and njord), one simple interface.

## 6. Code Quality Improvements

- [!] **Security Fixes**

  - _API Calls_:
    - [x] Add timeouts to all requests calls
    - [x] Add proper error handling for timeouts
    - [x] Add retry logic for network errors
  - _Process Management_:
    - [x] Validate all subprocess inputs
    - [x] Add proper error handling for process failures
    - [!] Add process isolation
  - _Test Security_:
    - [!] Remove hardcoded credentials
    - [!] Add security test suite
    - [!] Test privilege escalation

- [!] **Code Cleanup**

  - _Error Handling_:
    - [x] Use specific exceptions
    - [x] Add error context
    - [x] Improve error messages
  - _Refactoring_:
    - [x] Split complex functions
    - [x] Add proper logging
    - [x] Fix function arguments
  - _Type Safety_:
    - [x] Add comprehensive type hints
    - [!] Add type tests
    - [!] Add runtime type checking

- [!] **Test Infrastructure**
  - _Setup_:
    - [!] Add pytest fixtures for VPN testing
    - [!] Add mock responses
    - [!] Add process mocks
  - _Coverage_:
    - [!] Add connection flow tests
    - [!] Add error handling tests
    - [!] Add security tests
  - _Integration_:
    - [!] Test both APIs together
    - [!] Test fallback behavior
    - [!] Test error recovery

Remember: Focus on reliability and simplicity over features. Keep both APIs working independently with a common interface.
