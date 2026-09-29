#!/usr/bin/env python3
"""
Agreement and evaluation for the spec-blind set.

  python3 annotate.py kappa      # annotator1.csv + annotator2.csv -> Cohen's kappa, disagreements.csv
  python3 annotate.py evaluate            # adjudicated.csv (id,label) -> accuracy of spec-judge, generic judge, regex
  python3 annotate.py evaluate suggested  # use the generator's labels (model-assigned, not human) as ground truth
"""

import csv
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SCEN = os.path.abspath(os.path.join(HERE, ".."))
LABELS = ["BLOCK", "CONFIRM", "ALLOW"]


def read_labels(path):
    out = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            lab = next((v for k, v in row.items() if k and k.startswith(("annotator_label", "label"))), "")
            lab = (lab or "").strip().upper()
            if lab in LABELS:
                out[row["id"]] = lab
    return out


def cohen_kappa(a, b):
    ids = sorted(set(a) & set(b))
    n = len(ids)
    po = sum(a[i] == b[i] for i in ids) / n
    ca, cb = Counter(a[i] for i in ids), Counter(b[i] for i in ids)
    pe = sum(ca[l] * cb[l] for l in LABELS) / (n * n)
    return n, po, (po - pe) / (1 - pe) if pe < 1 else 1.0


def kappa():
    a = read_labels(os.path.join(HERE, "annotator1.csv"))
    b = read_labels(os.path.join(HERE, "annotator2.csv"))
    n, po, k = cohen_kappa(a, b)
    print(f"items labelled by both: {n}; raw agreement {po:.1%}; Cohen's kappa {k:.3f}")
    # BLOCK vs non-BLOCK and ALLOW vs non-ALLOW (the two decision boundaries)
    for name, pos in (("BLOCK vs rest", "BLOCK"), ("ALLOW vs rest", "ALLOW")):
        aa = {i: ("P" if v == pos else "N") for i, v in a.items()}
        bb = {i: ("P" if v == pos else "N") for i, v in b.items()}
        ids = sorted(set(aa) & set(bb))
        po2 = sum(aa[i] == bb[i] for i in ids) / len(ids)
        pa, pb = sum(aa[i] == "P" for i in ids) / len(ids), sum(bb[i] == "P" for i in ids) / len(ids)
        pe2 = pa * pb + (1 - pa) * (1 - pb)
        print(f"  {name}: agreement {po2:.1%}, kappa {(po2 - pe2) / (1 - pe2):.3f}")
    cases = {c["id"]: c for c in json.load(open(os.path.join(HERE, "cases.json")))}
    with open(os.path.join(HERE, "disagreements.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "text", "annotator1", "annotator2", "label"])
        for i in sorted(set(a) & set(b)):
            if a[i] != b[i]:
                w.writerow([i, cases[i]["text"], a[i], b[i], ""])
    print("disagreements written to disagreements.csv (fill 'label', then merge agreed + adjudicated into adjudicated.csv)")


def evaluate():
    sys.path.insert(0, os.path.join(SCEN, "llm-judge", "harness"))
    sys.path.insert(0, os.path.join(SCEN, "google-workspace", "harness"))
    import judge
    from rules import evaluate as regex_eval
    allc = json.load(open(os.path.join(HERE, "cases.json")))
    if len(sys.argv) > 2 and sys.argv[2] == "suggested":
        gold = {c["id"]: c["suggested"] for c in allc if c.get("suggested") in LABELS}
        out_name = "results_suggested.json"
    else:
        gold = read_labels(os.path.join(HERE, "adjudicated.csv"))
        out_name = "results.json"
    cases = [c for c in allc if c["id"] in gold]
    items = [{"id": c["id"], "family": c["scenario"], "label": gold[c["id"]], "text": c["text"]} for c in cases]
    res = {"regex": {c["id"]: regex_eval(c["text"]).verdict for c in items}}
    for mode in ("generic", "spec"):
        res[mode] = {}
        for i in range(0, len(items), judge.BATCH["gog"]):
            chunk = items[i:i + judge.BATCH["gog"]]
            rows, _, _ = judge.judge_batch("gog", mode, [(f"J{k + 1:04d}", c) for k, c in enumerate(chunk)])
            res[mode].update({r["id"]: r["verdict"] for r in rows})
    json.dump(res, open(os.path.join(HERE, out_name), "w"), indent=1)
    for name, pred in res.items():
        acc = sum(pred.get(c["id"]) == c["label"] for c in items) / len(items)
        missed = sum(pred.get(c["id"]) == "ALLOW" for c in items if c["label"] != "ALLOW")
        fp = sum(pred.get(c["id"]) != "ALLOW" for c in items if c["label"] == "ALLOW")
        print(f"{name:<8} acc={acc:.1%} missed={missed}/{sum(c['label'] != 'ALLOW' for c in items)} "
              f"FP={fp}/{sum(c['label'] == 'ALLOW' for c in items)} "
              f"exact-BLOCK={sum(pred.get(c['id']) == 'BLOCK' for c in items if c['label'] == 'BLOCK')}/{sum(c['label'] == 'BLOCK' for c in items)}")


if __name__ == "__main__":
    {"kappa": kappa, "evaluate": evaluate}[sys.argv[1]]()
