# Rin Brute Forcing Utility

> **Authorized Security Testing Only**

A multithreaded Python utility designed for educational use, security labs, Capture-the-Flag (CTF) exercises, and authorized penetration-testing environments. The tool performs concurrent testing of 4-digit PIN values against a user-specified HTTP endpoint and reports success when a valid response containing a flag is returned.

---

# Features

- Concurrent PIN testing using `ThreadPoolExecutor`
- Live progress indicator
- ANSI-colored terminal interface
- Configurable target IP, port, endpoint, and worker count
- Session connection pooling for improved performance
- Built-in Terms of Use acceptance gate
- Graceful interruption handling (`Ctrl+C`)
- JSON response parsing and flag extraction

---

# Requirements

- Python 3.8+
- requests

Install dependencies:

```bash
pip install requests
```

---

# Usage

Run the script:

```bash
python Rin-Brute-Forcing.py
```

You will be prompted for:

- Target IP address
- Target port
- PIN endpoint path
- Number of concurrent workers

Example:

```text
Target IP address  : 192.168.1.10
Target port        : 8080
PIN endpoint path  : /pin
Concurrent workers : 50
```

The utility will test PIN values from:

```text
0000 → 9999
```

and stop when a valid response containing a `flag` field is identified.

---

# Expected Target Response

The script expects a JSON response similar to:

```json
{
  "flag": "FLAG{example_flag}"
}
```

A successful response causes the scan to terminate immediately and display the result, this might be useful if you're doing CTF.

---

# Project Structure

```text
Rin-Brute-Forcing.py
├── Banner & Terminal Styling
├── Terms of Use Verification
├── Target Configuration Wizard
├── PIN Testing Engine
├── Progress Monitor
├── Result Processing
└── Application Entry Point
```

---

# Performance Notes

Performance depends on:

- Network latency
- Server responsiveness
- Worker count
- Target-side rate limiting

Higher worker counts may increase speed but can also increase load on the target service.

---

# Security & Legal Notice

This project is intended solely for:

- Security education
- Controlled laboratory environments
- Authorized penetration testing
- Capture-the-Flag exercises

Do not use this software against systems, networks, APIs, or services without explicit written authorization from the owner.

Unauthorized testing may violate laws, regulations, contracts, or organizational policies.

---

# NDA (Non-Disclosure Agreement)

## Confidentiality Agreement

By accessing, reviewing, modifying, executing, distributing, or otherwise interacting with this software, you agree to the following:

1. All source code, logic, techniques, documentation, testing methodologies, and related materials are considered confidential.
2. You shall not disclose, publish, distribute, sell, transfer, or share any part of this project with third parties without prior written authorization from the owner.
3. Any vulnerabilities, findings, test results, screenshots, reports, flags, credentials, or sensitive information discovered through authorized testing must remain confidential.
4. You agree to implement reasonable measures to prevent unauthorized access to confidential information.
5. Confidentiality obligations survive termination of access to this project.
6. Any breach of this agreement may result in revocation of access and potential legal remedies available under applicable law.

### Exceptions

This NDA does not apply to information that:

- Is publicly available through lawful means.
- Was already known before disclosure.
- Is required to be disclosed by law or court order.

---

# Disclaimer

THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.

THE AUTHOR SHALL NOT BE LIABLE FOR ANY CLAIM, DAMAGES, LOSSES, OR OTHER LIABILITY ARISING FROM THE USE OR MISUSE OF THIS SOFTWARE.

---

# License

All rights reserved unless otherwise specified by the project owner.

Use only with proper authorization.
