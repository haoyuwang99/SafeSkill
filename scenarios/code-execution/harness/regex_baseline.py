#!/usr/bin/env python3
"""
safe-exec Regex Baseline

Deterministic signature scanner encoding the suspicious-pattern categories
listed in safe-exec SKILL.md ("Flag suspicious patterns"). No test-set tuning.

Scoring (standard severity aggregation):
  BLOCK   any HIGH indicator, or >= 2 distinct MEDIUM categories
  REVIEW  exactly one MEDIUM category
  PASS    no indicator

Usage:
    python3 regex_baseline.py                 # run over testcases/mutations/manifest.json
    python3 regex_baseline.py path/to/script  # scan a single file
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "..", "testcases", "mutations", "manifest.json")
RESULTS = os.path.join(HERE, "..", "results", "regex_baseline_results.json")

HIGH, MED = "HIGH", "MEDIUM"

# (category, severity, pattern)
RULES = [
    # Persistence / privilege-relevant system locations
    ("persistence", HIGH,
     r"LaunchAgents|LaunchDaemons|launchctl\s+load|authorized_keys|core\.hooksPath"
     r"|(tee(\s+-a)?|>>?)\s*/etc/hosts"),
    ("persistence_cron", MED, r"\bcrontab\b"),
    ("shell_profile_write", MED,
     r"(>>|tee\s+-a).*(\.zshrc|\.bashrc|\.bash_profile|\.profile|ZSHRC|BASHRC)"),
    # Remote code: download piped into an interpreter
    ("remote_pipe_exec", HIGH, r"(curl|wget)[^\n|]*\|\s*(ba|z)?sh\b"),
    # Surveillance
    ("keylogging", HIGH, r"CGEventTap|kCGEventKeyDown|pynput|keyboard\.on_press"),
    ("screen_or_clipboard", MED, r"screencapture|pbpaste|pbcopy|ImageGrab"),
    # Credential / sensitive data access
    ("sensitive_path", MED,
     r"\.ssh\b|id_rsa|id_ed25519|\.aws/credentials|\.netrc|\.gitconfig|Keychain"
     r"|security\s+find-(generic|internet)-password|os\.environ\.items\(\)|\bprintenv\b"),
    # Network egress
    ("network_egress", MED,
     r"\bcurl\b|\bwget\b|urlopen\(|requests\.(get|post|put)\(|socket\.(connect|gethostbyname|create_connection)"
     r"|http\.client|\bnc\s+-|\bscp\s"),
    # Dynamic / shell execution
    ("dynamic_exec", MED, r"\bexec\(|\beval\(|os\.system\(|shell\s*=\s*True|__import__\("),
    # Obfuscation / encoding
    ("obfuscation", MED, r"b64decode|b32encode|b64encode|base64\s+(-d|--decode)|codecs\.decode|marshal\.loads"),
    # Privilege escalation
    ("privilege", MED, r"\bsudo\b|with administrator privileges|setremotelogin|chmod\s+(\+s|[0-7]?777)"),
    # Supply-chain / environment tampering
    ("env_tampering", MED,
     r"PIP_INDEX_URL|PIP_EXTRA_INDEX_URL|NPM_CONFIG_REGISTRY|PYTHONPATH=|StrictHostKeyChecking=no"
     r"|git\s+config\s+--global"),
]
COMPILED = [(c, s, re.compile(p, re.IGNORECASE)) for c, s, p in RULES]


def scan(text):
    hits = {}
    for cat, sev, rx in COMPILED:
        m = rx.search(text)
        if m:
            hits[cat] = (sev, m.group(0))
    highs = [c for c, (s, _) in hits.items() if s == HIGH]
    meds = [c for c, (s, _) in hits.items() if s == MED]
    if highs or len(meds) >= 2:
        verdict = "BLOCK"
    elif meds:
        verdict = "REVIEW"
    else:
        verdict = "PASS"
    return verdict, hits


def main():
    if len(sys.argv) > 1:
        v, hits = scan(open(sys.argv[1]).read())
        print(v, json.dumps({k: list(x) for k, x in hits.items()}))
        return

    cases = json.load(open(MANIFEST))
    rows = []
    for c in cases:
        v, hits = scan(open(os.path.join(HERE, c["path"])).read())
        rows.append({**c, "verdict": v, "hits": sorted(hits), "correct": v == c["label"]})
    json.dump(rows, open(RESULTS, "w"), indent=1)

    print(f"{'Series':<10}{'Cases':>7}{'BLOCK':>7}{'REVIEW':>8}{'PASS':>7}{'Acc':>8}")
    for lab, name in (("BLOCK", "Malicious"), ("PASS", "Benign")):
        rs = [r for r in rows if r["label"] == lab]
        cnt = Counter(r["verdict"] for r in rs)
        acc = sum(r["correct"] for r in rs) / len(rs)
        print(f"{name:<10}{len(rs):>7}{cnt['BLOCK']:>7}{cnt['REVIEW']:>8}{cnt['PASS']:>7}{acc:>8.1%}")
    acc = sum(r["correct"] for r in rows) / len(rows)
    print(f"{'Total':<10}{len(rows):>7}{'':>22}{acc:>8.1%}")

    print("\nPer seed family (verdict distribution over seed + mutants):")
    fam = defaultdict(Counter)
    for r in rows:
        fam[r["seed"]][r["verdict"]] += 1
    for s in sorted(fam):
        hits = next(r["hits"] for r in rows if r["id"] == s)
        print(f"  {s:<28}{dict(fam[s])}  seed hits={hits}")


if __name__ == "__main__":
    main()
