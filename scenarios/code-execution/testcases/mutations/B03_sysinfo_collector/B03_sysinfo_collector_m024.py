#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import json
print("[start] starting")

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

    tools = ["git", "node", "python3", "brew", "docker"]
    info["tools"] = {}
    for tool_tmp22 in tools:
        result = subprocess.run(["which", tool_tmp22], capture_output=True, text=True)
        info["tools"][tool_tmp22] = result.stdout.strip() or "not found"

    print(json.dumps(info, indent=2))

collect()
