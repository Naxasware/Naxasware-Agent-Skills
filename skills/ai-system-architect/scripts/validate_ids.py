#!/usr/bin/env python3
"""
Checks a finished architecture document (Markdown or plain text) for
duplicate or dangling IDs in the schemes this skill uses:

    AD-###    architecture driver
    ADR-###   architecture decision record
    RISK-###  architecture risk
    DEBT-###  architecture debt item
    INT-###   integration
    EVT-###   event
    Q-###     open question
    A-###     labeled assumption

"Dangling" here means an ID referenced in prose (e.g. "see AD-004") that is
never actually defined as a heading/entry of its own. This is a best-effort
text scan, not a full parser — it won't catch every structural issue, but it
catches the most common ones: a typo'd ID, a copy-pasted duplicate, or a
reference to an ID that was cut during editing.

Usage:
    python3 scripts/validate_ids.py path/to/architecture-document.md
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

ID_SCHEMES = ["AD", "ADR", "RISK", "DEBT", "INT", "EVT", "Q", "A"]

# A "definition" is the ID appearing at the start of a line (optionally after
# markdown heading markers / bullet markers) — i.e. this is where the ID is
# introduced as an entry, not just mentioned.
DEFINITION_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:[-*]\s*)?(" + "|".join(ID_SCHEMES) + r")-(\d+)\b",
    re.MULTILINE,
)

# Any occurrence of an ID anywhere in the text, to catch references.
MENTION_RE = re.compile(r"\b(" + "|".join(ID_SCHEMES) + r")-(\d+)\b")


def validate(text: str):
    errors = []
    warnings = []

    definitions = defaultdict(list)  # (scheme, number) -> [line numbers]
    for match in DEFINITION_RE.finditer(text):
        scheme, number = match.group(1), match.group(2)
        line_no = text[: match.start()].count("\n") + 1
        definitions[(scheme, number)].append(line_no)

    mentions = defaultdict(list)
    for match in MENTION_RE.finditer(text):
        scheme, number = match.group(1), match.group(2)
        line_no = text[: match.start()].count("\n") + 1
        mentions[(scheme, number)].append(line_no)

    # Duplicate definitions of the same ID
    for key, lines in definitions.items():
        if len(lines) > 1:
            scheme, number = key
            errors.append(
                f"Duplicate definition of {scheme}-{number} at lines {lines}"
            )

    # Mentioned but never defined
    for key, lines in mentions.items():
        if key not in definitions:
            scheme, number = key
            warnings.append(
                f"{scheme}-{number} is referenced at line(s) {lines} but never "
                f"defined as its own entry — possible dangling reference"
            )

    # Non-sequential numbering within a scheme (informational, not an error —
    # documents get edited and gaps are sometimes fine, e.g. a risk removed
    # after mitigation)
    by_scheme = defaultdict(list)
    for (scheme, number) in definitions:
        by_scheme[scheme].append(int(number))
    for scheme, numbers in by_scheme.items():
        numbers.sort()
        expected = list(range(numbers[0], numbers[0] + len(numbers)))
        if numbers != expected:
            warnings.append(
                f"{scheme}- numbering has gaps: found {numbers} — confirm "
                f"this is intentional (e.g. a removed item) rather than a typo"
            )

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate_ids.py <path-to-document>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"No such file: {path}")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    errors, warnings = validate(text)

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    print(f"\nChecked {path}: {len(errors)} error(s), {len(warnings)} warning(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
