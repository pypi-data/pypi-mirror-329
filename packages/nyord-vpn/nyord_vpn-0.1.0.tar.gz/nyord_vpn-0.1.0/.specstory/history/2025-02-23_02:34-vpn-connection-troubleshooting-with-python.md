## SpecStory

## VPN Connection Troubleshooting with Python (23/02/2025, 02:34:11)

_**User**_

python -m nyord_vpn --verbose --api legacy connect

Using legacy VPN API
Initialized VPN client
Initializing legacy VPN client
Found OpenVPN version 2.6.13
Created config directory: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/T/nyord_vpn_juk09cz0
Requesting administrator password to configure VPN connection...
Initializing VPN connection...
Getting server recommendation for fastest server
Selected server: pl146.nordvpn.com
Downloading config for server: pl146.nordvpn.com
Saved config to: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/T/nyord_vpn_juk09cz0/pl146.nordvpn.com.ovpn
Created auth file: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/T/nordvpn_ownjywj_.auth
Starting OpenVPN process
OpenVPN process started with PID: 85031
Connecting to pl146.nordvpn.com...
OpenVPN process 85031 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 1/12
OpenVPN process 85031 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 2/12
OpenVPN process 85031 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 3/12
OpenVPN process 85031 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 4/12
OpenVPN process 85031 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 5/12
OpenVPN process 85031 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 6/12
^CCleaning up auth file
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/src/nyord_vpn/__main__.py", line 148, in <module>
    main()
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/src/nyord_vpn/__main__.py", line 141, in main
    fire.Fire(CLI)
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/.venv/lib/python3.12/site-packages/fire/core.py", line 135, in Fire
    component_trace = _Fire(component, args, parsed_flag_args, context, name)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/.venv/lib/python3.12/site-packages/fire/core.py", line 468, in _Fire
    component, remaining_args = _CallAndUpdateTrace(
                                ^^^^^^^^^^^^^^^^^^^^
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/.venv/lib/python3.12/site-packages/fire/core.py", line 684, in _CallAndUpdateTrace
    component = fn(*varargs, **kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/src/nyord_vpn/__main__.py", line 82, in connect
    self._client.connect(country)
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/src/nyord_vpn/api/legacy.py", line 206, in connect
    subprocess.run(["sleep", "5"], check=False)  # Wait 5 seconds between checks
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/subprocess.py", line 550, in run
    stdout, stderr = process.communicate(input, timeout=timeout)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/subprocess.py", line 1201, in communicate
    self.wait()
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/subprocess.py", line 1264, in wait
    return self._wait(timeout=timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/subprocess.py", line 2053, in _wait
    (pid, sts) = self._try_wait(0)
                 ^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/subprocess.py", line 2011, in _try_wait
    (pid, sts) = os.waitpid(self.pid, wait_flags)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt


---

_**Assistant**_

Let me help analyze this VPN connection issue. First, I'll examine the relevant code to understand what's happening.

---

_****_

<details>
            <summary>Searched codebase "VPN connection implementation in legacy.py" • **25** results</summary>
        
| File | Lines |
|------|-------|
| `src/nyord_vpn/api/legacy.py` | L151-172 |
| `src/nyord_vpn/api/legacy.py` | L172-216 |
| `src/nyord_vpn/api/legacy.py` | L216-257 |
| `src/nyord_vpn/core/client.py` | L29-82 |
| `src/nyord_vpn/core/client.py` | L1-14 |
| `src/nyord_vpn/__main__.py` | L46-104 |
| `src/nyord_vpn/api/legacy.py` | L257-278 |
| `src/nyord_vpn/api/legacy.py` | L113-151 |
| `src/nyord_vpn/api/legacy.py` | L32-60 |
| `src/nyord_vpn/api/legacy.py` | L315-348 |
| `src/nyord_vpn/api/legacy.py` | L278-315 |
| `src/nyord_vpn/core/config.py` | L1-55 |
| `src/nyord_vpn/core/client.py` | L82-128 |
| `src/nyord_vpn/core/base.py` | L18-88 |
| `src/nyord_vpn/api/base.py` | L1-61 |
| `src/nyord_vpn/core/factory.py` | L1-44 |
| `src/nyord_vpn/__main__.py` | L1-46 |
| `src/nyord_vpn/api/legacy.py` | L348-375 |
| `src/nyord_vpn/core/base.py` | L1-18 |
| `src/nyord_vpn/api/legacy.py` | L1-32 |
| `src/nyord_vpn/api/legacy.py` | L60-113 |
| `src/nyord_vpn/core/client.py` | L128-163 |
| `src/nyord_vpn/api/njord/client.py` | L54-111 |
| `src/nyord_vpn/core/exceptions.py` | L11-15 |
| `src/nyord_vpn/api/njord/client.py` | L111-147 |

</details>

---

_****_



After analyzing the code and the error output, I can see that the VPN connection attempt was interrupted (KeyboardInterrupt) during the connection process. The issue appears to be in the connection monitoring loop where the code uses `subprocess.run(["sleep", "5"])` to wait between connection status checks.

Here's what's happening:

1. The VPN process starts successfully and gets PID 85031
2. The code enters a loop to check if the connection is established
3. The connection check involves:
   - Verifying the OpenVPN process is running
   - Checking if the IP belongs to NordVPN
4. Between checks, there's a 5-second sleep using `subprocess.run(["sleep", "5"])`
5. The connection attempt was interrupted during one of these sleep periods

Let me propose a fix to improve this behavior. Instead of using `subprocess.run(["sleep", 5])`, we should use Python's native `time.sleep()` which is more graceful and can be interrupted properly.

---

_****_

```diff
  from pathlib import Path
  from typing import Any
+ import time  # Add time import
  
  import requests
                          f"Waiting for connection... attempt {retries}/{max_retries}"
                      )
-                     subprocess.run(["sleep", "5"], check=False)  # Wait 5 seconds between checks
+                     time.sleep(5)  # Use time.sleep instead of subprocess.run
  
                  # Connection failed
```

---

_****_



Now let me explain the changes and what to expect:

1. I've replaced the `subprocess.run(["sleep", "5"])` with Python's native `time.sleep(5)`. This is better because:
   - It's more graceful and can be properly interrupted with Ctrl+C
   - It doesn't spawn unnecessary subprocesses
   - It's more portable across different operating systems

2. The connection process will still:
   - Try to connect for up to 60 seconds (12 attempts × 5 seconds)
   - Check the connection status between attempts
   - Allow for proper interruption with Ctrl+C

To try the connection again:

---

_****_

```bash
python -m nyord_vpn --verbose --api legacy connect
```

```
(nyord_vpn) adam@Hamlet nyord_vpn % python -m nyord_vpn --verbose 
--api legacy c
onnect
Using legacy VPN API
Initialized VPN client
Initializing legacy VPN client
Found OpenVPN version 2.6.13
Created config directory: /var/folders/05/clcynl0509ldxltl599hhhx4
0000gn/T/nyord_vpn_rn5rfbu8
Requesting administrator password to configure VPN connection...
Initializing VPN connection...
Getting server recommendation for fastest server
Selected server: pl198.nordvpn.com
Downloading config for server: pl198.nordvpn.com
Saved config to: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/T/
nyord_vpn_rn5rfbu8/pl198.nordvpn.com.ovpn
Created auth file: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/
T/nordvpn__81vdos_.auth
Starting OpenVPN process
OpenVPN process started with PID: 85406
Connecting to pl198.nordvpn.com...
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
Password:VPN protection status: False
Waiting for connection... attempt 1/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 2/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 3/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 4/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 5/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 6/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 7/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 8/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 9/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 10/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 11/12
OpenVPN process 85406 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 12/12
Failed to establish VPN connection after 60 seconds
Cleaning up auth file
Connection failed: Failed to establish VPN connection after 60 sec
onds
Stopping OpenVPN process 85406
Graceful shutdown failed, force killing process
```

---

_****_



---

_**User**_

We don't need 12 fucking retries in the code. Just 2 

---

_**Assistant**_

I'll modify the connection retry logic to only attempt 2 retries instead of 12. This will make the connection attempt faster to fail if it's not working.

---

_****_

```diff
                  # Monitor connection status
                  retries = 0
-                 max_retries = 12  # 60 seconds total
+                 max_retries = 2  # 10 seconds total
                  while retries < max_retries:
                      if self.protected():
  
                  # Connection failed
-                 logger.error("Failed to establish VPN connection after 60 seconds")
-                 msg = "Failed to establish VPN connection after 60 seconds"
+                 logger.error("Failed to establish VPN connection after 10 seconds")
+                 msg = "Failed to establish VPN connection after 10 seconds"
                  raise VPNConnectionError(msg)
  
```

---

_****_



I've made the following changes:
1. Reduced `max_retries` from 12 to 2
2. Updated the comments and error messages to reflect the new 10-second total wait time (2 retries × 5 seconds)

This means:
- First attempt (0 seconds): Initial connection check
- First retry (5 seconds): Check if connection is established
- Second retry (10 seconds): Final check before failing

The connection will now fail faster if it's not working, instead of waiting for a full minute. You can try connecting again with:

---

_****_



---

_****_



---

_**User**_

But primarily try to fix why it fails

---

_**Assistant**_

Looking at the code more carefully, I notice a few potential issues that could be causing the connection failure:

1. We're not capturing OpenVPN's output, which means we can't see why it might be failing
2. We're running OpenVPN in daemon mode but not checking its actual status
3. The `protected()` check might be too aggressive too early

Let me modify the code to better handle and diagnose connection issues:

---

_****_

```diff
                          "--auth-user-pass",
                          str(auth_file),
-                         "--daemon",
                      ],
-                     stdout=subprocess.DEVNULL,
-                     stderr=subprocess.STDOUT,
+                     stdout=subprocess.PIPE,
+                     stderr=subprocess.PIPE,
+                     text=True,
+                     bufsize=1,
                  )
                  self._openvpn_pid = process.pid
                  max_retries = 2  # 10 seconds total
                  while retries < max_retries:
+                     # Check OpenVPN process status
+                     if process.poll() is not None:
+                         stdout, stderr = process.communicate()
+                         logger.error("OpenVPN process exited prematurely")
+                         logger.error(f"OpenVPN output: {stdout}")
+                         logger.error(f"OpenVPN errors: {stderr}")
+                         msg = f"OpenVPN failed: {stderr or stdout}"
+                         raise VPNConnectionError(msg)
+ 
+                     # Check if we're connected
                      if self.protected():
                          logger.info("VPN connection established")
                          return True
+ 
                      retries += 1
                      logger.debug(
                          f"Waiting for connection... attempt {retries}/{max_retries}"
                      )
-                     time.sleep(5)  # Use time.sleep instead of subprocess.run
+                     time.sleep(5)
  
-                 # Connection failed
+                 # Connection failed - get OpenVPN output
+                 stdout, stderr = process.communicate()
+                 logger.error(f"OpenVPN output: {stdout}")
+                 logger.error(f"OpenVPN errors: {stderr}")
                  logger.error("Failed to establish VPN connection after 10 seconds")
-                 msg = "Failed to establish VPN connection after 10 seconds"
+                 msg = f"OpenVPN failed: {stderr or stdout}"
                  raise VPNConnectionError(msg)
  
```

---

_****_



Key changes I've made:

1. Removed `--daemon` mode so we can properly capture OpenVPN's output
2. Added proper output capturing with `stdout=subprocess.PIPE` and `stderr=subprocess.PIPE`
3. Added process status checking to detect if OpenVPN exits prematurely
4. Added logging of OpenVPN's output and errors to help diagnose issues
5. Improved error messages to include actual OpenVPN output

These changes will help us see:
- If OpenVPN is failing to start
- If there are authentication issues
- If there are network/routing problems
- Any other OpenVPN-specific errors

Let's try connecting again:

---

_****_

```bash
python -m nyord_vpn --verbose --api legacy connect
```

```
(nyord_vpn) adam@Hamlet nyord_vpn % python -m nyord_vpn --verbose 
--api legacy connect                              python -m nyord_
vpn --verbose --api legacy connect
Using legacy VPN API
Initialized VPN client
Initializing legacy VPN client
Found OpenVPN version 2.6.13
Created config directory: /var/folders/05/clcynl0509ldxltl599hhhx4
0000gn/T/nyord_vpn_2tktxh5w
Requesting administrator password to configure VPN connection...
Initializing VPN connection...
Getting server recommendation for fastest server
Selected server: pl198.nordvpn.com
Downloading config for server: pl198.nordvpn.com
Saved config to: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/T/
nyord_vpn_2tktxh5w/pl198.nordvpn.com.ovpn
Created auth file: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/
T/nordvpn_r_tto9wu.auth
Starting OpenVPN process
OpenVPN process started with PID: 85623
Connecting to pl198.nordvpn.com...
OpenVPN process 85623 is running
Checking if IP belongs to NordVPN
Password:VPN protection status: False
Waiting for connection... attempt 1/2
OpenVPN process 85623 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 2/2
```

---

_****_



---

_**User**_

Hey, "Password:" means that it wants my sudo pwd. We should WAIT for it! 

---

_**Assistant**_

Ah, you're absolutely right! We're checking the connection status too quickly before the sudo password prompt is even handled. Let's add a delay after starting OpenVPN to allow time for the sudo password entry:

---

_****_

```diff
                  self._current_server = server
                  logger.debug(f"OpenVPN process started with PID: {self._openvpn_pid}")
+ 
+                 # Wait for sudo password entry
+                 logger.info("Waiting for sudo password entry...")
+                 time.sleep(10)  # Give user time to enter sudo password
  
                  # Wait for connection
```

---

_****_



I've added:
1. A 10-second delay after starting OpenVPN but before checking connection status
2. A log message to indicate we're waiting for the sudo password
3. This gives you time to enter your sudo password before we start checking if the connection is established

Let's try connecting again:

---

_****_

```bash
python -m nyord_vpn --verbose --api legacy connect
```

```
Using legacy VPN API
Initialized VPN client
Initializing legacy VPN client
Found OpenVPN version 2.6.13
Created config directory: /var/folders/05/clcynl0509ldxltl599hhhx4
0000gn/T/nyord_vpn_w83krvnb                                       Requesting adm
inistrator password to configure VPN connection...
Initializing VPN connection...
Getting server recommendation for fastest server
Selected server: pl198.nordvpn.com
Downloading config for server: pl198.nordvpn.com
Saved config to: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/T/
nyord_vpn_w83krvnb/pl198.nordvpn.com.ovpn                         Created auth f
ile: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/
T/nordvpn_fny5ubce.auth                                           Starting OpenV
PN process
OpenVPN process started with PID: 85709
Waiting for sudo password entry...
Password:
Connecting to pl198.nordvpn.com...
OpenVPN process 85709 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 1/2
OpenVPN process 85709 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 2/2
^CCleaning up auth file
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/sr
c/nyord_vpn/__main__.py", line 148, in <module>                       main()
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/sr
c/nyord_vpn/__main__.py", line 141, in main                           fire.Fire(
CLI)
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/.v
env/lib/python3.12/site-packages/fire/core.py", line 135, in Fire     component_
trace = _Fire(component, args, parsed_flag_args, con
text, name)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^                                                         File "/Users
/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/.v
env/lib/python3.12/site-packages/fire/core.py", line 468, in _Fire    component,
 remaining_args = _CallAndUpdateTrace(
                                ^^^^^^^^^^^^^^^^^^^^
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/.v
env/lib/python3.12/site-packages/fire/core.py", line 684, in _CallAndUpdateTrace
                                                        component = fn(*varargs,
 **kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/sr
c/nyord_vpn/__main__.py", line 82, in connect                         self._clie
nt.connect(country)
  File "/Users/adam/Developer/vcs/github.twardoch/pub/nyord_vpn/sr
c/nyord_vpn/api/legacy.py", line 226, in connect                      stdout, st
derr = process.communicate()
                     ^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/pyt
hon3.12/subprocess.py", line 1209, in communicate                     stdout, st
derr = self._communicate(input, endtime, timeout)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/pyt
hon3.12/subprocess.py", line 2115, in _communicate                    ready = se
lector.select(timeout)
            ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/pyt
hon3.12/selectors.py", line 415, in select                            fd_event_l
ist = self._selector.poll(timeout)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt


```

---

_****_



---

_**User**_

Why are we just waiting for 10 seconds. We should wait UNTIL THE USER ENTERS THE ADMIN PWD

---

_**Assistant**_

Ah, you're absolutely right! Instead of an arbitrary wait, we should actively monitor the OpenVPN process output for the sudo password prompt and wait until it's handled. Here's how we can do that:

---

_****_

```diff
                  logger.debug(f"OpenVPN process started with PID: {self._openvpn_pid}")
  
-                 # Wait for sudo password entry
+                 # Wait for sudo password entry to complete
                  logger.info("Waiting for sudo password entry...")
-                 time.sleep(10)  # Give user time to enter sudo password
+                 while True:
+                     if process.poll() is not None:
+                         # Process ended prematurely
+                         stdout, stderr = process.communicate()
+                         logger.error(
+                             "OpenVPN process exited during sudo password entry"
+                         )
+                         logger.error(f"OpenVPN output: {stdout}")
+                         logger.error(f"OpenVPN errors: {stderr}")
+                         msg = f"OpenVPN failed during sudo: {stderr or stdout}"
+                         raise VPNConnectionError(msg)
+ 
+                     # Check if sudo is done by trying a test command
+                     try:
+                         subprocess.run(
+                             ["sudo", "-n", "true"], check=True, capture_output=True
+                         )
+                         logger.debug(
+                             "Sudo password accepted, proceeding with connection"
+                         )
+                         break
+                     except subprocess.CalledProcessError:
+                         time.sleep(0.5)  # Wait a bit before checking again
  
                  # Wait for connection
```

---

_****_



Key changes:
1. Instead of a fixed 10-second wait, we now actively monitor for sudo password completion
2. We use `sudo -n true` to test if sudo password has been entered (the `-n` flag makes sudo fail immediately if it would need a password)
3. We check every 0.5 seconds until the sudo test passes
4. We also monitor if the OpenVPN process dies during this wait
5. Only proceed with connection checks after sudo is confirmed working

This means we'll:
1. Wait as long as needed for the user to enter their password
2. Detect immediately when the password is accepted
3. Catch any errors that happen during the sudo password entry phase

Let's try connecting again:

---

_****_

```bash
python -m nyord_vpn --verbose --api legacy connect
```

```
(nyord_vpn) adam@Hamlet nyord_vpn % python -m nyord_vpn --verbose 
--api legacy connect                python -m nyord_vpn --verbose 
--api legacy connect
Using legacy VPN API
Initialized VPN client
Initializing legacy VPN client
Found OpenVPN version 2.6.13
Created config directory: /var/folders/05/clcynl0509ldxltl599hhhx4
0000gn/T/nyord_vpn_x6kjs650
Requesting administrator password to configure VPN connection...
Initializing VPN connection...
Getting server recommendation for fastest server
Selected server: pl241.nordvpn.com
Downloading config for server: pl241.nordvpn.com
Saved config to: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/T/
nyord_vpn_x6kjs650/pl241.nordvpn.com.ovpn
Created auth file: /var/folders/05/clcynl0509ldxltl599hhhx40000gn/
T/nordvpn_8fksshyp.auth
Starting OpenVPN process
OpenVPN process started with PID: 86507
Waiting for sudo password entry...
Sudo password accepted, proceeding with connection
Connecting to pl241.nordvpn.com...
OpenVPN process 86507 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 1/2
OpenVPN process 86507 is running
Checking if IP belongs to NordVPN
VPN protection status: False
Waiting for connection... attempt 2/2
```

---

_****_



---

_**User**_

The verbose logging is fucking terrible

---

_**Assistant**_



---



---

