#!/usr/bin/env python3
"""
Check workflow-architecture documents for ID problems.

Finds duplicate definitions, dangling references (an ID used but never
defined) and malformed IDs (fewer than three digits) for these prefixes:
BO WR WD STEP DEC TOOL TASK TEST WADR WRISK A Q.

How an ID counts as *defined*: it is the first thing in a heading, list item
or table row (the first cell), outside code fences, and not under a heading
containing "Traceab", "Coverage" or "Cross-ref" (those sections only
reference). Everything else is a reference. A line containing
`<!-- ref -->` is treated as reference-only.

Usage:
    python3 validate_ids.py architecture.md [more.md ...] [--orphans]

    --orphans   also warn about defined IDs that nothing references
                (WR, WD, TOOL, DEC, TASK, STEP, WADR, WRISK)

Exit code 1 if any error was found. Standard library only.
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

PREFIXES = ["BO", "WR", "WD", "STEP", "DEC", "TOOL", "TASK", "TEST", "WADR", "WRISK", "A", "Q"]
_ALT = "|".join(sorted(PREFIXES, key=len, reverse=True))
ID_RE = re.compile(r"(?<![A-Za-z0-9_-])(" + _ALT + r")-(\d+)(?![A-Za-z0-9_])")
LEAD_RE = re.compile(
    r"^(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|\|\s*|>\s*)*(?:\*\*|__|`)?\s*(" + _ALT + r")-(\d+)(?![A-Za-z0-9_])"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
REF_ONLY_HEADING_RE = re.compile(r"traceab|coverage|cross-?ref", re.I)
ORPHAN_PREFIXES = {"WR", "WD", "TOOL", "DEC", "TASK", "STEP", "WADR", "WRISK"}


class Scan:
    """Result of scanning one document."""

    def __init__(self):
        self.defs = defaultdict(list)       # id -> [line numbers]
        self.def_text = {}                  # id -> text of first defining line
        self.refs = defaultdict(list)       # id -> [line numbers] (non-defining uses)
        self.malformed = []                 # (line, token)
        self.line_ids = {}                  # line no -> [ids] for non-fence lines
        self.fence_ids = defaultdict(list)  # id -> [line numbers] inside code fences


def norm(prefix, digits):
    return f"{prefix}-{digits}"


def scan(text):
    s = Scan()
    in_fence = False
    heading = ""
    for no, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        hm = HEADING_RE.match(stripped) if not in_fence else None
        if hm:
            heading = hm.group(2)

        found = [(m.group(1), m.group(2)) for m in ID_RE.finditer(line)]
        for p, d in found:
            if len(d) < 3:
                s.malformed.append((no, norm(p, d)))
        found = [norm(p, d) for p, d in found if len(d) >= 3]
        if not found:
            continue

        if in_fence:
            for i in found:
                s.fence_ids[i].append(no)
            continue

        s.line_ids[no] = found
        defined = None
        if not REF_ONLY_HEADING_RE.search(heading) and "<!-- ref" not in line:
            lm = LEAD_RE.match(stripped)
            if lm and len(lm.group(2)) >= 3:
                defined = norm(lm.group(1), lm.group(2))
        used = list(found)
        if defined:
            s.defs[defined].append(no)
            s.def_text.setdefault(defined, stripped)
            used.remove(defined)  # drop one occurrence: the definition itself
        for i in used:
            s.refs[i].append(no)
    return s


def check(s, orphans=False):
    errors, warnings = [], []
    for i, lines in sorted(s.defs.items()):
        if len(lines) > 1:
            errors.append(f"{i} is defined {len(lines)} times (lines {', '.join(map(str, lines))})")
    for no, tok in s.malformed:
        errors.append(f"line {no}: malformed ID '{tok}' (use at least three digits, e.g. {tok.split('-')[0]}-001)")
    for i, lines in sorted(s.refs.items()):
        if i not in s.defs:
            errors.append(f"{i} is referenced but never defined (line {lines[0]})")
    for i, lines in sorted(s.fence_ids.items()):
        if i not in s.defs:
            errors.append(f"{i} appears in a code block (line {lines[0]}) but is never defined")
    if orphans:
        used = set(s.refs) | set(s.fence_ids)
        for i in sorted(s.defs):
            if i.split("-")[0] in ORPHAN_PREFIXES and i not in used:
                warnings.append(f"{i} is defined but never referenced")
    return errors, warnings


def main(argv):
    orphans = "--orphans" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    total_err = 0
    for p in paths:
        path = Path(p)
        if not path.exists():
            print(f"ERROR: {p}: file not found")
            total_err += 1
            continue
        errors, warnings = check(scan(path.read_text(encoding="utf-8")), orphans)
        for w in warnings:
            print(f"WARNING: {p}: {w}")
        for e in errors:
            print(f"ERROR: {p}: {e}")
        total_err += len(errors)
        print(f"{p}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
