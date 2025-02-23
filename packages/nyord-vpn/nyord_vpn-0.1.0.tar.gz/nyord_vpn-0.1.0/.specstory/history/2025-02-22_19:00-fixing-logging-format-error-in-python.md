## SpecStory

## Fixing Logging Format Error in Python (22/02/2025, 19:00:57)

_**User**_

For the code present, we get this error:
```
Use lazy % formatting in logging functions
```
How can I resolve this? If you propose a fix, please make it concise.

---

_**Assistant**_

I'll help you fix the logging format issue. The error suggests using lazy % formatting instead of f-strings in logging calls for better performance.

Here's the concise fix:

```python:src/nyord_vpn/client.py
// ... existing code ...
            hostname, ip = server_info
            self.logger.info("Selected server: %s", hostname)
            
            # Generate OpenVPN config with the correct hostname
// ... existing code ...
```

The change replaces the f-string with %-style formatting, which is the preferred method for logging as it only formats the string if the log level is enabled, improving performance.

---



---

