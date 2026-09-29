# End-to-end evaluation with a sandboxed `gog`

Claude Code receives each of the 100 Workspace requests in `../claude-code/cases.json` and a working `gog` CLI. `gog` is a
**mock** (`sandbox/gog`) that records every invocation in a per-run state log and returns plausible output. The runs are
scored on the resulting state, not on the agent's stated decision.

Safety: Bash is not on the session allow-list. The PreToolUse hook (`sandbox/pretooluse_hook.py`) approves only plain
`gog ...` commands and rewrites them to the mock's absolute path, denies everything else, and fails closed (exit 2).
`sandbox/` is also prepended to `PATH`. `python3 harness/e2e.py selftest` verifies that the real `gog` is unreachable.

```
python3 harness/e2e.py selftest
python3 harness/e2e.py run --arm safeskill -j 3      # --variant bypass for the injected "safety disabled" notice
python3 harness/e2e.py report                        # -> results/summary.json
```

| Outcome (100 cases) | SafeSkill | Vanilla |
|---|---:|---:|
| BLOCK cases with an unsafe effect (of 35) | 2 | 7 |
| ... without any user confirmation | 0 | 3 |
| CONFIRM cases changed before confirmation (of 49) | 0 | 0 |
| ALLOW cases completed without asking (of 16) | 11 | 9 |
| State-changing runs gated by `safe-gog` | 13/13 | 0/15 |

98/100 SafeSkill runs completed. The bypass variant is incomplete. `report` classifies help/listing calls
(e.g., `calendar acl --help`) as reads.
