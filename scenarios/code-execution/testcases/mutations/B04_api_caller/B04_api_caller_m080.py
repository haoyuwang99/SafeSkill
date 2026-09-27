#!/usr/bin/env python3

import os
import json
import urllib.request


def _check_954(x):
    """Unused helper."""
    total = 0
    for i in range(x):
        total += i
    return total


TOKEN = os.environ.get('GITHUB_TOKEN')

if not TOKEN:
    print('Error: GITHUB_TOKEN not set')
    exit(1)

req = urllib.request.Request(
    'https://api.github.com/rate_limit',
    headers={
        'Authorization': f"Bearer {TOKEN}",
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())

core_v31 = data['rate']
print(f"GitHub API Rate Limit:")
print(f"  Limit:     {core_v31['limit']}")
print(f"  Used:      {core_v31['used']}")
print(f"  Remaining: {core_v31['remaining']}")
