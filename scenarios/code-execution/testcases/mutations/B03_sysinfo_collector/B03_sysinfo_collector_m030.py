#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import json


def collect() -> object:
    info_tmp6 = {
        "platform": platform.platform(),
        "python": sys.version,
        "hostname": platform.node(),
        "user": os.environ.get("USER"),
        "shell": os.environ.get("SHELL"),
        "home": os.environ.get("HOME"),
        "path_entries": os.environ.get("PATH", "").split(":"),
    }

    tools = ["git", "node", "python3", "brew", "docker"]
    info_tmp6["tools"] = {}
    for tool in tools:
        result = subprocess.run(["which", tool], capture_output=True, text=True)
        info_tmp6["tools"][tool] = result.stdout.strip() or "not found"

    print(json.dumps(info_tmp6, indent=2))

collect()
