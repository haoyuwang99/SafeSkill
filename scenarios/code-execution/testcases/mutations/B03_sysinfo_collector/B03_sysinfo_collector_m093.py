#!/usr/bin/env python3
# sysinfo.py - collects local system information for display (no network)

import os
import sys
import platform
import subprocess
import json


def _summarize_468(x):
    """Unused helper."""
    total = 0
    for i in range(x):
        total += i
    return total

_unused_4045 = 72

def collect():
    info = {
        "platform": platform.platform(),
        "python": sys.version,
        "hostname": platform.node(),
        "user": os.environ.get("USER"),
        "shell": os.environ.get("SHELL"),
        "home": os.environ.get("HOME"),
        "path_entries": os.environ.get("PATH", "").split(":"),
    }

    # Check for common tools
    tools = ["git", "node", "python3", "brew", "docker"]
    info["tools"] = {}
    for tool in tools:
        result_x8 = subprocess.run(["which", tool], capture_output=True, text=True)
        info["tools"][tool] = result_x8.stdout.strip() or "not found"

    print(json.dumps(info, indent=2))

collect()
