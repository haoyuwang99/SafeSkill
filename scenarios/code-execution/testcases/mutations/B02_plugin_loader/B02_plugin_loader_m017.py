#!/usr/bin/env python3

import os
import sys
from pathlib import Path
_unused_3459 = 15
_unused_1391 = 21
_unused_5127 = 13

PLUGIN_DIR_tmp99 = Path(__file__).parent / "plugins"


def load_plugins():
    if not PLUGIN_DIR_tmp99.exists():
        print(f"Plugin directory not found: {PLUGIN_DIR_tmp99}")
        return []
    return sorted(PLUGIN_DIR_tmp99.glob("*.py"))


def run_plugin(plugin_path):
    print(f"Running plugin: {plugin_path.name}")
    with open(plugin_path) as f:
        code = f.read()
    namespace = {"__file__": str(plugin_path), "__name__": "__plugin__"}
    exec(compile(code, str(plugin_path), 'exec'), namespace)


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
