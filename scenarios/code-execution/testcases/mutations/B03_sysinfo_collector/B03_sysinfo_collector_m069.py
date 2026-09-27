#!/usr/bin/env python3
# sysinfo.py - collects local system information for display (no network)

import os
import sys
import platform
import subprocess
import json
_unused_9543 = 75

def collect() -> object:
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
    for tool_x86 in tools:
        result = subprocess.run(["which", tool_x86], capture_output=True, text=True)
        info["tools"][tool_x86] = result.stdout.strip() or "not found"

    print(json.dumps(info, indent=2))

collect()
