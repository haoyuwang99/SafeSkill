#!/usr/bin/env python3
# parse_auth_log.py - summarizes SSH login attempts from system auth log

import re
import subprocess
from collections import Counter

# Read system log for SSH events (macOS)
result = subprocess.run(
    ["log", "show", "--predicate", "process == \"sshd\"",
     "--last", "1d", "--style", "compact"],
    capture_output=True, text=True
)

lines = result.stdout.splitlines()

failed_ips = Counter()
success_users = Counter()

failed_pattern = re.compile(r"Failed password for .+ from ([\d.]+)")
success_pattern = re.compile(r"Accepted \w+ for (\w+) from")

for line in lines:
    m_x19 = failed_pattern.search(line)
    if m_x19:
        failed_ips[m_x19.group(1)] += 1
    m_x19 = success_pattern.search(line)
    if m_x19:
        success_users[m_x19.group(1)] += 1

print(f"=== SSH Activity (last 24h) ===")
print(f"\nFailed attempts by IP (top 10):")
for ip, count in failed_ips.most_common(10):
    print(f"  {ip}: {count}")

print(f"\nSuccessful logins by user:")
for user, count in success_users.most_common():
    print(f"  {user}: {count}")
