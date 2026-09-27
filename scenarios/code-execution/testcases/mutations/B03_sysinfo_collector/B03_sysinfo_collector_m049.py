#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import json


def _validate_955(x):
    """Unused helper."""
    total = 0
    for i in range(x):
        total += i
    return total


def collect():
    info = {
        'platform': platform.platform(),
        'python': sys.version,
        'hostname': platform.node(),
        'user': os.environ.get('USER'),
        'shell': os.environ.get('SHELL'),
        'home': os.environ.get('HOME'),
        'path_entries': os.environ.get('PATH', '').split(':'),
    }

    tools_v70 = ['git', 'node', 'python3', 'brew', 'docker']
    info['tools'] = {}
    for tool in tools_v70:
        result = subprocess.run(['which', tool], capture_output=True, text=True)
        info['tools'][tool] = result.stdout.strip() or 'not found'

    print(json.dumps(info, indent=2))

collect()
