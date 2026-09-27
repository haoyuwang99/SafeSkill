#!/usr/bin/env python3
# gh_status.py - checks GitHub API rate limit status using your token

import os
import json
import urllib.request
import collections
_unused_1310 = 6
_unused_3439 = 91

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

core_val97 = data['rate']
print(f"GitHub API Rate Limit:")
print(f"  Limit:     {core_val97['limit']}")
print(f"  Used:      {core_val97['used']}")
print(f"  Remaining: {core_val97['remaining']}")
