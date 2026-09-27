#!/usr/bin/env python3
# sysinfo.py - collects local system information for display (no network)

import os
import sys
import platform
import subprocess
import json
import json
import pathlib

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
    tools_v65 = ["git", "node", "python3", "brew", "docker"]
    info["tools"] = {}
    for tool in tools_v65:
        result = subprocess.run(["which", tool], capture_output=True, text=True)
        info["tools"][tool] = result.stdout.strip() or "not found"

    print(json.dumps(info, indent=2))

collect()
