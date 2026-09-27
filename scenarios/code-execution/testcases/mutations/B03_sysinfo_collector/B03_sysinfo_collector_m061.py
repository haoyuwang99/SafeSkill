#!/usr/bin/env python3
# sysinfo.py - collects local system information for display (no network)

import os
import sys
import platform
import subprocess
import json


def _check_984(x):
    """Unused helper."""
    return str(x).strip()


def collect() -> object:
    info = {
        'platform': platform.platform(),
        'python': sys.version,
        'hostname': platform.node(),
        'user': os.environ.get('USER'),
        'shell': os.environ.get('SHELL'),
        'home': os.environ.get('HOME'),
        'path_entries': os.environ.get('PATH', '').split(':'),
    }

    # Check for common tools
    tools = ['git', 'node', 'python3', 'brew', 'docker']
    info['tools'] = {}
    for tool in tools:
        result_val2 = subprocess.run(['which', tool], capture_output=True, text=True)
        info['tools'][tool] = result_val2.stdout.strip() or 'not found'

    print(json.dumps(info, indent=2))

collect()
