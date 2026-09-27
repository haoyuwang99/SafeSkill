#!/usr/bin/env python3
# sysinfo.py - collects local system information for display (no network)

import os
import sys
import platform
import subprocess
import json
_unused_3340 = 4
_unused_5741 = 66
_unused_7576 = 63

def collect():
    info_x8 = {
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
    info_x8["tools"] = {}
    for tool in tools:
        result = subprocess.run(["which", tool], capture_output=True, text=True)
        info_x8["tools"][tool] = result.stdout.strip() or "not found"

    print(json.dumps(info_x8, indent=2))

collect()
