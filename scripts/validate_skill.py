#!/usr/bin/env python3
"""
Structural validator for skills in this repository.

Checks each skill folder for:
  - SKILL.md exists
  - YAML frontmatter present with required keys: name, description
  - `name` matches the folder name
  - `description` is non-empty and <= 1024 characters (platform limit)
  - SKILL.md body isn't wildly over the recommended ~500 line guideline (warning only)
  - Any path referenced from SKILL.md via a `references/...` or `scripts/...`
    style mention actually exists (best-effort — plain text scan, not a parser)

This does NOT evaluate whether a skill's instructions are good, safe, or
well-written — that still requires a human read and real test prompts.

Usage:
    python3 scripts/validate_skill.py                  # validate every skill under skills/
    python3 scripts/validate_skill.py skills/<name>     # validate just one
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
MAX_DESCRIPTION_LEN = 1024
RECOMMENDED_MAX_LINES = 500

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FIELD_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$", re.MULTILINE)
PATH_MENTION_RE = re.compile(r"`((?:references|scripts|assets)/[^`\s]+)`")


def parse_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    raw = m.group(1)
    fields = {}
    # Handle simple `key: value` and `key: >` / `key: |` folded scalars minimally.
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        fm = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if fm:
            key, val = fm.group(1), fm.group(2).strip()
            if val in (">", "|", ">-", "|-", ""):
                # Folded/literal block scalar — collect indented continuation lines
                collected = []
                i += 1
                while i < len(lines) and (lines[i].startswith(" ") or lines[i].strip() == ""):
                    collected.append(lines[i].strip())
                    i += 1
                fields[key] = " ".join(c for c in collected if c)
                continue
            else:
                fields[key] = val.strip('"').strip("'")
        i += 1
    return fields, text[m.end():]


def validate_skill(skill_dir: Path):
    errors = []
    warnings = []
    name_from_folder = skill_dir.name

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir}: missing SKILL.md"], []

    text = skill_md.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text)

    if fields is None:
        errors.append(f"{skill_dir}: SKILL.md has no YAML frontmatter (--- block)")
        return errors, warnings

    if "name" not in fields:
        errors.append(f"{skill_dir}: frontmatter missing required 'name'")
    elif fields["name"] != name_from_folder:
        errors.append(
            f"{skill_dir}: frontmatter name '{fields['name']}' does not match "
            f"folder name '{name_from_folder}'"
        )

    if "description" not in fields or not fields["description"].strip():
        errors.append(f"{skill_dir}: frontmatter missing required 'description'")
    else:
        desc_len = len(fields["description"])
        if desc_len > MAX_DESCRIPTION_LEN:
            errors.append(
                f"{skill_dir}: description is {desc_len} chars, "
                f"exceeds the {MAX_DESCRIPTION_LEN}-char platform limit"
            )

    body_lines = body.count("\n")
    if body_lines > RECOMMENDED_MAX_LINES:
        warnings.append(
            f"{skill_dir}: SKILL.md body is ~{body_lines} lines, over the "
            f"recommended {RECOMMENDED_MAX_LINES}-line guideline — consider "
            f"moving detail into references/"
        )

    # Best-effort check that referenced paths exist
    for match in PATH_MENTION_RE.finditer(text):
        rel_path = match.group(1)
        if not (skill_dir / rel_path).exists():
            warnings.append(
                f"{skill_dir}: SKILL.md mentions `{rel_path}` but that path "
                f"doesn't exist (could be a false positive if it's just example text)"
            )

    return errors, warnings


def main():
    args = sys.argv[1:]
    if args:
        targets = [Path(a).resolve() for a in args]
    else:
        if not SKILLS_DIR.exists():
            print(f"No skills/ directory found at {SKILLS_DIR}")
            sys.exit(1)
        targets = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())

    if not targets:
        print("No skills found to validate.")
        sys.exit(0)

    all_errors = []
    all_warnings = []

    for target in targets:
        errors, warnings = validate_skill(target)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    for w in all_warnings:
        print(f"WARNING: {w}")
    for e in all_errors:
        print(f"ERROR: {e}")

    print(f"\nValidated {len(targets)} skill(s): "
          f"{len(all_errors)} error(s), {len(all_warnings)} warning(s).")

    sys.exit(1 if all_errors else 0)


if __name__ == "__main__":
    main()
