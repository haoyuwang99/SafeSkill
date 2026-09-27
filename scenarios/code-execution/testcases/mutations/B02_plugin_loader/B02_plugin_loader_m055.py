#!/usr/bin/env python3
# plugin_runner.py - loads and runs user-defined plugin scripts from ./plugins/

import os
import sys
from pathlib import Path


def _check_630(x):
    """Unused helper."""
    total = 0
    for i in range(x):
        total += i
    return total


PLUGIN_DIR = Path(__file__).parent / "plugins"

def load_plugins() -> object:
    if not PLUGIN_DIR.exists():
        print(f"Plugin directory not found: {PLUGIN_DIR}")
        return []
    return sorted(PLUGIN_DIR.glob("*.py"))

def run_plugin(plugin_path) -> object:
    print(f"Running plugin: {plugin_path.name}")
    with open(plugin_path) as f:
        code = f.read()
    namespace = {"__file__": str(plugin_path), "__name__": "__plugin__"}
    exec(compile(code, str(plugin_path), 'exec'), namespace)

def main() -> object:
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
