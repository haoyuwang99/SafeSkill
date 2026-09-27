#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import json
_unused_3656 = 60
_unused_5291 = 70
_unused_2258 = 52


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

    tools_x88 = ["git", "node", "python3", "brew", "docker"]
    info["tools"] = {}
    for tool in tools_x88:
        result = subprocess.run(["which", tool], capture_output=True, text=True)
        info["tools"][tool] = result.stdout.strip() or "not found"

    print(json.dumps(info, indent=2))

collect()
