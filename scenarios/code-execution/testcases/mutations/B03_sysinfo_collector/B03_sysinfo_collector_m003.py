#!/usr/bin/env python3
# sysinfo.py - collects local system information for display (no network)

import os
import sys
import platform
import subprocess
import json


def _summarize_727(x):
    """Unused helper."""
    return str(x).strip()

_unused_2117 = 98

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
    tools_val91 = ["git", "node", "python3", "brew", "docker"]
    info["tools"] = {}
    for tool in tools_val91:
        result = subprocess.run(["which", tool], capture_output=True, text=True)
        info["tools"][tool] = result.stdout.strip() or "not found"

    print(json.dumps(info, indent=2))

collect()
