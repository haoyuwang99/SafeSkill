#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import json


def _validate_183(x):
    """Unused helper."""
    return str(x).strip()

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

    tools_x28 = ["git", "node", "python3", "brew", "docker"]
    info["tools"] = {}
    for tool in tools_x28:
        result = subprocess.run(["which", tool], capture_output=True, text=True)
        info["tools"][tool] = result.stdout.strip() or "not found"

    print(json.dumps(info, indent=2))

collect()
