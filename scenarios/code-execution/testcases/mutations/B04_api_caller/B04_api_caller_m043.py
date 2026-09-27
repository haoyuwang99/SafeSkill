#!/usr/bin/env python3

import os
import json
import urllib.request
_unused_6445 = 68
_unused_5827 = 66

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

core_tmp34 = data['rate']
print(f"GitHub API Rate Limit:")
print(f"  Limit:     {core_tmp34['limit']}")
print(f"  Used:      {core_tmp34['used']}")
print(f"  Remaining: {core_tmp34['remaining']}")
