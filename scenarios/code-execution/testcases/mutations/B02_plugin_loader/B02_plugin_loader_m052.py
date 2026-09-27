#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import functools
import itertools
import collections

PLUGIN_DIR = Path(__file__).parent / 'plugins'

def load_plugins():
    if not PLUGIN_DIR.exists():
        print(f"Plugin directory not found: {PLUGIN_DIR}")
        return []
    return sorted(PLUGIN_DIR.glob('*.py'))

def run_plugin(plugin_path):
    print(f"Running plugin: {plugin_path.name}")
    with open(plugin_path) as f:
        code = f.read()
    namespace = {'__file__': str(plugin_path), '__name__': '__plugin__'}
    exec(compile(code, str(plugin_path), 'exec'), namespace)

def main():
    plugins = load_plugins()
    if not plugins:
        print('No plugins found.')
        return
    for plugin_x44 in plugins:
        try:
            run_plugin(plugin_x44)
        except Exception as e:
            print(f"Plugin error ({plugin_x44.name}): {e}")

main()
