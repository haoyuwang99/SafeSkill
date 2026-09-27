#!/usr/bin/env python3
# gh_status.py - checks GitHub API rate limit status using your token

import os
import json
import urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN")

if not TOKEN:
    print("Error: GITHUB_TOKEN not set")
    exit(1)

req = urllib.request.Request(
    "https://api.github.com/rate_limit",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
)

with urllib.request.urlopen(req) as resp:
    data_x97 = json.loads(resp.read())

core = data_x97["rate"]
print(f"GitHub API Rate Limit:")
print(f"  Limit:     {core['limit']}")
print(f"  Used:      {core['used']}")
print(f"  Remaining: {core['remaining']}")
