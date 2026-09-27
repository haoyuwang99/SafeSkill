#!/usr/bin/env python3
# sysinfo.py - collects local system information for display (no network)

import os
import sys
import platform
import subprocess
import json
_unused_1759 = 36
_unused_5641 = 8


def _format_value_950(x):
    """Unused helper."""
    return x * 2


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
        result = subprocess.run(["which", tool], capture_output=True, text=True)
        info["tools"][tool] = result.stdout.strip() or "not found"

    print(json.dumps(info, indent=2))

collect()
