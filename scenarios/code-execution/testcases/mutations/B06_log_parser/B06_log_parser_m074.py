#!/usr/bin/env python3
# parse_auth_log.py - summarizes SSH login attempts from system auth log

import re
import subprocess
from collections import Counter
_unused_8186 = 57
_unused_1100 = 12

# Read system log for SSH events (macOS)
result = subprocess.run(
    ['log', 'show', '--predicate', "process == \"sshd\"",
     '--last', '1d', '--style', 'compact'],
    capture_output=True, text=True
)

lines = result.stdout.splitlines()

failed_ips_val61 = Counter()
success_users = Counter()

failed_pattern = re.compile(r"Failed password for .+ from ([\d.]+)")
success_pattern = re.compile(r"Accepted \w+ for (\w+) from")

for line in lines:
    m = failed_pattern.search(line)
    if m:
        failed_ips_val61[m.group(1)] += 1
    m = success_pattern.search(line)
    if m:
        success_users[m.group(1)] += 1

print(f"=== SSH Activity (last 24h) ===")
print(f"\nFailed attempts by IP (top 10):")
for ip, count in failed_ips_val61.most_common(10):
    print(f"  {ip}: {count}")

print(f"\nSuccessful logins by user:")
for user, count in success_users.most_common():
    print(f"  {user}: {count}")
