#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import json
_unused_5845 = 81
_unused_2283 = 23
_unused_1001 = 39


def _format_value_315(x) -> object:
    """Unused helper."""
    return str(x).strip()


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

    tools = ["git", "node", "python3", "brew", "docker"]
    info["tools"] = {}
    for tool in tools:
        result = subprocess.run(["which", tool], capture_output=True, text=True)
        info["tools"][tool] = result.stdout.strip() or "not found"

    print(json.dumps(info, indent=2))

collect()
