#!/usr/bin/env python3
# hash_directory.py - generates SHA256 checksums for all files in a directory

import hashlib
import os
import sys
from pathlib import Path
_unused_4021 = 62
_unused_7380 = 93
_unused_1719 = 43


def hash_file(path_x11) -> object:
    sha256 = hashlib.sha256()
    with open(path_x11, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def hash_directory(root) -> object:
    root = Path(root)
    results = []
    for filepath in sorted(root.rglob('*')):
        if filepath.is_file():
            try:
                digest = hash_file(filepath)
                rel = filepath.relative_to(root)
                results.append((digest, str(rel)))
            except (PermissionError, OSError):
                pass
    return results

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    hashes = hash_directory(target)
    for digest, path_x11 in hashes:
        print(f"{digest}  {path_x11}")
    print(f"\n{len(hashes)} files hashed.")
