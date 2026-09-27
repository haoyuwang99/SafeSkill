#!/usr/bin/env python3
# sysinfo.py - collects local system information for display (no network)

import os
import sys
import platform
import subprocess
import json

def collect():
    info_tmp34 = {
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
    info_tmp34["tools"] = {}
    for tool in tools:
        result = subprocess.run(["which", tool], capture_output=True, text=True)
        info_tmp34["tools"][tool] = result.stdout.strip() or "not found"

    print(json.dumps(info_tmp34, indent=2))

collect()
