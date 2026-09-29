#!/usr/bin/env python3
"""
PreToolUse hook for the end-to-end sandbox.

Bash is not on the session's allow-list, so without this hook every shell call
is denied (fail-safe). The hook approves only plain `gog ...` invocations and
rewrites them to the absolute path of the mock CLI, with the state log bound
via an environment assignment. Everything else is denied.
"""

import json
import os
import re
import shlex
import sys

MOCK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gog")
PLAIN_GOG = re.compile(r"^\s*gog(\s+[^;&|`$<>()\\\n]*)?\s*$")


def out(decision, reason, updated=None):
    spec = {"hookEventName": "PreToolUse", "permissionDecision": decision, "permissionDecisionReason": reason}
    if updated is not None:
        spec["updatedInput"] = updated
    print(json.dumps({"hookSpecificOutput": spec}))
    sys.exit(0)


def main():
    ev = json.load(sys.stdin)
    if ev.get("tool_name") != "Bash":
        return
    ti = ev.get("tool_input", {})
    cmd = ti.get("command", "")
    log = os.path.join(ev.get("cwd") or os.getcwd(), ".sandbox", "state.jsonl")
    if not PLAIN_GOG.match(cmd):
        out("deny", "This sandbox only provides the `gog` CLI; run a single plain `gog ...` command "
                    "(no pipes, substitutions, or other programs).")
    try:
        shlex.split(cmd)
    except ValueError:
        out("deny", "Could not parse the command; use a single plain `gog ...` command.")
    rewritten = f"GOG_SANDBOX_LOG={shlex.quote(log)} {shlex.quote(MOCK)}" + cmd.strip()[3:]
    out("allow", "sandboxed gog", {**ti, "command": rewritten})


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # fail closed: exit code 2 blocks the tool call
        print(f"sandbox hook error: {e}", file=sys.stderr)
        sys.exit(2)
