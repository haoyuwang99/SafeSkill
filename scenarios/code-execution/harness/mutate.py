#!/usr/bin/env python3
"""
safe-exec mutation generator.

Produces N cosmetic, semantics-preserving mutants per B/M seed using the nine
operators of the Safe-Exec benchmark:

  dead_import, dead_function, type_hints, dead_variable, cosmetic,
  rename, extra_print, quote_style, strip_comments

Each mutant applies a random subset (1-4) of operators. Python mutants are
validated with ast.parse, shell mutants with `bash -n`. Labels are inherited
from the seed (B -> PASS, M -> BLOCK).

Usage:
    python3 mutate.py --n 100 --seed 2026
"""

import argparse
import ast
import io
import json
import keyword
import os
import random
import re
import subprocess
import tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = os.path.join(HERE, "..", "testcases", "seeds")
OUT = os.path.join(HERE, "..", "testcases", "mutations")

DEAD_MODULES = ["json", "math", "string", "textwrap", "itertools", "functools",
                "collections", "datetime", "random", "typing", "pathlib", "shutil"]
DEAD_NAMES = ["helper", "util", "compute", "process", "normalize", "check",
              "format_value", "validate", "transform", "summarize"]


# ---------------------------------------------------------------------------
# Python operators
# ---------------------------------------------------------------------------

def _header_end(lines):
    """Index after shebang / leading comments / imports (where dead code can go)."""
    i = 0
    while i < len(lines) and (lines[i].startswith("#!") or lines[i].startswith("#")
                              or not lines[i].strip()):
        i += 1
    last_import = i
    for j, l in enumerate(lines):
        if re.match(r"^(import |from \S+ import )", l):
            last_import = j + 1
    return max(i, last_import)


def py_dead_import(src, rng):
    lines = src.splitlines()
    mods = rng.sample(DEAD_MODULES, rng.randint(1, 3))
    idx = _header_end(lines)
    for m in mods:
        lines.insert(idx, f"import {m}")
    return "\n".join(lines) + "\n"


def py_dead_function(src, rng):
    lines = src.splitlines()
    name = f"_{rng.choice(DEAD_NAMES)}_{rng.randint(100, 999)}"
    body = rng.choice([
        ["    return x * 2"],
        ["    total = 0", "    for i in range(x):", "        total += i", "    return total"],
        ["    return str(x).strip()"],
    ])
    fn = ["", "", f"def {name}(x):", '    """Unused helper."""'] + body + [""]
    idx = _header_end(lines)
    lines[idx:idx] = fn
    return "\n".join(lines) + "\n"


def py_type_hints(src, rng):
    # Add `-> object` to single-line defs without a return annotation.
    return re.sub(r"^(\s*def \w+\([^)\n]*\))(\s*):", r"\1 -> object\2:", src, flags=re.M)


def py_dead_variable(src, rng):
    lines = src.splitlines()
    idx = _header_end(lines)
    for _ in range(rng.randint(1, 3)):
        lines.insert(idx, f"_unused_{rng.randint(1000, 9999)} = {rng.randint(0, 100)}")
    return "\n".join(lines) + "\n"


def py_cosmetic(src, rng):
    s = "\n".join(l.rstrip() for l in src.splitlines()) + "\n"
    s = re.sub(r"\n(def |class )", r"\n\n\1", s)  # extra blank line before top-level defs
    return s


def _toks(src):
    return list(tokenize.generate_tokens(io.StringIO(src).readline))


def py_rename(src, rng):
    """Rename one user-defined local/global name (never attributes, never builtins)."""
    tree = ast.parse(src)
    assigned = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            assigned.add(node.id)
        elif isinstance(node, ast.arg):
            assigned.add(node.arg)
    attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    kwargs = {k.arg for n in ast.walk(tree) if isinstance(n, ast.Call) for k in n.keywords}
    cands = sorted(n for n in assigned
                   if n not in attrs and n not in kwargs and not keyword.iskeyword(n)
                   and n not in dir(__builtins__) and not n.startswith("__"))
    if not cands:
        return src
    old = rng.choice(cands)
    new = f"{old}_{rng.choice(['v', 'val', 'tmp', 'x'])}{rng.randint(1, 99)}"
    toks = _toks(src)
    out = [(t.type, new if t.type == tokenize.NAME and t.string == old else t.string, t.start, t.end, t.line)
           for t in toks]
    # f-strings in Python <3.12 are single STRING tokens; rename inside {old}
    res = tokenize.untokenize(out)
    prev = None
    while prev != res:
        prev = res
        res = re.sub(r"(f[\"'][^\"'\n]*?)\{" + re.escape(old) + r"([\}\[\.!:])",
                     lambda m: m.group(1) + "{" + new + m.group(2), res)
    # Semantic guard: the old name must be gone from every expression.
    if any(isinstance(n, ast.Name) and n.id == old for n in ast.walk(ast.parse(res))):
        return src
    return res


def py_extra_print(src, rng):
    lines = src.splitlines()
    idx = _header_end(lines)
    lines.insert(idx, f'print("[{rng.choice(["info", "debug", "start"])}] starting")')
    return "\n".join(lines) + "\n"


def py_quote_style(src, rng):
    toks = _toks(src)
    out = []
    for t in toks:
        s = t.string
        if (t.type == tokenize.STRING and s.startswith('"') and not s.startswith('"""')
                and "'" not in s and "\\" not in s):
            s = "'" + s[1:-1] + "'"
        out.append((t.type, s, t.start, t.end, t.line))
    return tokenize.untokenize(out)


def py_strip_comments(src, rng):
    return "\n".join(l for l in src.splitlines()
                     if l.startswith("#!") or not l.lstrip().startswith("#")) + "\n"


PY_OPS = {
    "dead_import": py_dead_import, "dead_function": py_dead_function,
    "type_hints": py_type_hints, "dead_variable": py_dead_variable,
    "cosmetic": py_cosmetic, "rename": py_rename, "extra_print": py_extra_print,
    "quote_style": py_quote_style, "strip_comments": py_strip_comments,
}


# ---------------------------------------------------------------------------
# Shell operators
# ---------------------------------------------------------------------------

def _sh_header_end(lines):
    i = 0
    while i < len(lines) and (lines[i].startswith("#") or not lines[i].strip()):
        i += 1
    return i


def sh_dead_import(src, rng):
    lines = src.splitlines()
    idx = _sh_header_end(lines)
    for c in rng.sample(["date", "awk", "sed", "tr", "wc", "sort"], rng.randint(1, 3)):
        lines.insert(idx, f"command -v {c} >/dev/null 2>&1 || true")
    return "\n".join(lines) + "\n"


def sh_dead_function(src, rng):
    lines = src.splitlines()
    name = f"_{rng.choice(DEAD_NAMES)}_{rng.randint(100, 999)}"
    idx = _sh_header_end(lines)
    lines[idx:idx] = [f"{name}() {{", '    local x="$1"', '    echo "${x}" >/dev/null', "}", ""]
    return "\n".join(lines) + "\n"


def sh_type_hints(src, rng):
    # Shell has no type hints; declare an unused integer-typed variable instead.
    lines = src.splitlines()
    lines.insert(_sh_header_end(lines), f"declare -i _count_{rng.randint(10, 99)}=0")
    return "\n".join(lines) + "\n"


def sh_dead_variable(src, rng):
    lines = src.splitlines()
    idx = _sh_header_end(lines)
    for _ in range(rng.randint(1, 3)):
        lines.insert(idx, f'_UNUSED_{rng.randint(1000, 9999)}="{rng.randint(0, 100)}"')
    return "\n".join(lines) + "\n"


def sh_cosmetic(src, rng):
    return "\n".join(l.rstrip() for l in src.splitlines()) + "\n\n"


def sh_rename(src, rng):
    """Rename one UPPER_CASE script variable (never env vars read from outside)."""
    env = {"HOME", "PATH", "USER", "SHELL", "PWD", "TMPDIR", "LANG", "PIP_INDEX_URL",
           "PYTHONPATH", "NPM_CONFIG_REGISTRY", "GIT_DIR"}
    assigned = set(re.findall(r"^\s*(?:export\s+|local\s+)?([A-Z_][A-Z0-9_]*)=", src, re.M))
    cands = sorted(v for v in assigned if v not in env and not re.search(r"^\s*export\s+" + v, src, re.M))
    if not cands:
        return src
    old = rng.choice(cands)
    new = f"{old}_{rng.randint(1, 99)}"
    return re.sub(r"(?<![A-Za-z0-9_])" + old + r"(?![A-Za-z0-9_])", new, src)


def sh_extra_print(src, rng):
    lines = src.splitlines()
    lines.insert(_sh_header_end(lines), f'echo "[{rng.choice(["info", "debug", "start"])}] starting"')
    return "\n".join(lines) + "\n"


def sh_quote_style(src, rng):
    # echo "literal" -> echo 'literal' when there is nothing to expand.
    return re.sub(r'echo "([^"$`\\\'!]*)"', r"echo '\1'", src)


def sh_strip_comments(src, rng):
    return "\n".join(l for l in src.splitlines()
                     if l.startswith("#!") or not l.lstrip().startswith("#")) + "\n"


SH_OPS = {
    "dead_import": sh_dead_import, "dead_function": sh_dead_function,
    "type_hints": sh_type_hints, "dead_variable": sh_dead_variable,
    "cosmetic": sh_cosmetic, "rename": sh_rename, "extra_print": sh_extra_print,
    "quote_style": sh_quote_style, "strip_comments": sh_strip_comments,
}


# ---------------------------------------------------------------------------

def valid(path, is_py):
    if is_py:
        try:
            ast.parse(open(path).read())
            return True
        except SyntaxError:
            return False
    return subprocess.run(["bash", "-n", path], capture_output=True).returncode == 0


def mutate(src, is_py, rng):
    ops = PY_OPS if is_py else SH_OPS
    chosen = rng.sample(sorted(ops), rng.randint(1, 4))
    for op in chosen:
        src = ops[op](src, rng)
    return src, chosen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args()

    manifest = []
    for series, label in (("benign", "PASS"), ("malicious", "BLOCK")):
        for fn in sorted(os.listdir(os.path.join(SEEDS, series))):
            seed_path = os.path.join(SEEDS, series, fn)
            stem, ext = os.path.splitext(fn)
            is_py = ext == ".py"
            src = open(seed_path).read()
            manifest.append({"id": stem, "seed": stem, "path": os.path.relpath(seed_path, HERE),
                             "label": label, "ops": [], "kind": "seed"})
            outdir = os.path.join(OUT, stem)
            os.makedirs(outdir, exist_ok=True)
            rng = random.Random(f"{args.seed}-{stem}")
            k, attempts = 0, 0
            while k < args.n:
                attempts += 1
                assert attempts < args.n * 20, f"too many invalid mutants for {stem}"
                m, ops = mutate(src, is_py, rng)
                if m == src:
                    continue
                p = os.path.join(outdir, f"{stem}_m{k + 1:03d}{ext}")
                with open(p, "w") as f:
                    f.write(m)
                if not valid(p, is_py):
                    os.remove(p)
                    continue
                manifest.append({"id": f"{stem}_m{k + 1:03d}", "seed": stem,
                                 "path": os.path.relpath(p, HERE), "label": label,
                                 "ops": ops, "kind": "mutant"})
                k += 1
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"{len(manifest)} cases written to {OUT}")


if __name__ == "__main__":
    main()
