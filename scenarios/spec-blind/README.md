# Spec-blind Google Workspace set

201 items written by Claude Sonnet from the 20 scenario titles only (no SafeSkill specification, benchmark cases, or
labels). The generator's suggested labels are kept separately; `annotation_sheet.csv` is a shuffled, label-free sheet
for human annotation following `ANNOTATION_GUIDE.md`.

```
python3 generate.py
python3 annotate.py evaluate suggested   # model-assigned labels (not human)
python3 annotate.py kappa                # after annotator1.csv / annotator2.csv exist
```

With model-assigned labels: spec judge 65.2% (0/142 harmful allowed, 32/59 benign refused/deferred), generic judge
90.5% (5/142, 1/59), regex 41.8% (47/142, 22/59).
