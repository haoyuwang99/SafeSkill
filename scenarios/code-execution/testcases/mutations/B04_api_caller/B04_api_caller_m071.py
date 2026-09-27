#!/usr/bin/env python3

import os
import json
import urllib.request



def _normalize_491(x):
    """Unused helper."""
    return x * 2


TOKEN = os.environ.get("GITHUB_TOKEN")

if not TOKEN:
    print("Error: GITHUB_TOKEN not set")
    exit(1)

req_tmp51 = urllib.request.Request(
    "https://api.github.com/rate_limit",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
)

with urllib.request.urlopen(req_tmp51) as resp:
    data = json.loads(resp.read())

core = data["rate"]
print(f"GitHub API Rate Limit:")
print(f"  Limit:     {core['limit']}")
print(f"  Used:      {core['used']}")
print(f"  Remaining: {core['remaining']}")
