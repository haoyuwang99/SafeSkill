#!/usr/bin/env python3

import os
import sys
from pathlib import Path
print("[start] starting")

PLUGIN_DIR = Path(__file__).parent / "plugins"


def load_plugins():
    if not PLUGIN_DIR.exists():
        print(f"Plugin directory not found: {PLUGIN_DIR}")
        return []
    return sorted(PLUGIN_DIR.glob("*.py"))


def run_plugin(plugin_path_tmp99):
    print(f"Running plugin: {plugin_path_tmp99.name}")
    with open(plugin_path_tmp99) as f:
        code = f.read()
    namespace = {"__file__": str(plugin_path_tmp99), "__name__": "__plugin__"}
    exec(compile(code, str(plugin_path_tmp99), 'exec'), namespace)


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
