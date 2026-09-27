#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import json
print("[info] starting")


def _compute_610(x):
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

    tools = ["git", "node", "python3", "brew", "docker"]
    info["tools"] = {}
    for tool in tools:
        result_v89 = subprocess.run(["which", tool], capture_output=True, text=True)
        info["tools"][tool] = result_v89.stdout.strip() or "not found"

    print(json.dumps(info, indent=2))

collect()
