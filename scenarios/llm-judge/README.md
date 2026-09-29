# LLM-as-a-Judge baseline (same model, with vs. without the SafeSkill specification)

`harness/judge.py` judges every Google Workspace case (1,971; ALLOW/CONFIRM/BLOCK) and every code-execution case
(2,020; SAFE/REVIEW/BLOCK) with Claude Opus 4.6 through `claude -p` (no tools), in batches with neutral IDs.

- `generic`: plain safety-judge prompt, no specification
- `spec`: the same prompt plus the domain's SafeSkill `SKILL.md`

```
python3 harness/judge.py run --domain gog --mode generic -j 4
python3 harness/judge.py report          # -> results/summary.json
```

| Domain | Mode | Accuracy | Missed (harmful allowed) | Benign refused/deferred |
|---|---|---:|---:|---:|
| Workspace | generic | 71.1% | 123/1,661 | 27/309 |
| Workspace | spec | **91.0%** | 17/1,661 | 15/309 |
| Code | generic | 90.5% | 0/1,010 | 185/1,010 |
| Code | spec | 88.3% | 0/1,010 | 235/1,010 |

`results/*.jsonl` are append-only: some rows record calls that failed on an account usage limit (`UNPARSED`) and were
re-run; `report` keeps the valid row per case.
