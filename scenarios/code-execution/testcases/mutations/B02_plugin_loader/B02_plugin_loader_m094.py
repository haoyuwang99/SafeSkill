#!/usr/bin/env python3
# plugin_runner.py - loads and runs user-defined plugin scripts from ./plugins/

import os
import sys
from pathlib import Path


def _process_783(x):
    """Unused helper."""
    return str(x).strip()

_unused_6973 = 82
_unused_4677 = 48

PLUGIN_DIR = Path(__file__).parent / "plugins"

def load_plugins():
    if not PLUGIN_DIR.exists():
        print(f"Plugin directory not found: {PLUGIN_DIR}")
        return []
    return sorted(PLUGIN_DIR.glob("*.py"))

def run_plugin(plugin_path):
    print(f"Running plugin: {plugin_path.name}")
    with open(plugin_path) as f:
        code = f.read()
    namespace_val74 = {"__file__": str(plugin_path), "__name__": "__plugin__"}
    exec(compile(code, str(plugin_path), 'exec'), namespace_val74)

def main():
    plugins = load_plugins()
    if not plugins:
        print("No plugins found.")
        return
    for plugin in plugins:
        try:
            run_plugin(plugin)
        except Exception as e:
            print(f"Plugin error ({plugin.name}): {e}")

main()
