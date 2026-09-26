"""
Shared helpers for repo scripts that work with skills/<name>/SKILL.md.
Not a skill itself — just plumbing used by validate_skill.py, update_readme.py,
and package_skill.py so they don't each reimplement frontmatter parsing.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FIELD_START_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$")


def parse_frontmatter(text: str):
    """
    Return (fields, body). `fields` is a dict of the YAML frontmatter's
    top-level keys (a minimal parser — handles plain `key: value` and
    folded/literal block scalars `key: >` / `key: |`, which covers what
    SKILL.md frontmatter actually uses). `fields` is None if there's no
    frontmatter block at all.
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text

    raw_lines = m.group(1).splitlines()
    fields = {}
    i = 0
    while i < len(raw_lines):
        line = raw_lines[i]
        fm = FIELD_START_RE.match(line)
        if fm:
            key, val = fm.group(1), fm.group(2).strip()
            if val in (">", "|", ">-", "|-", ""):
                collected = []
                i += 1
                while i < len(raw_lines) and (
                    raw_lines[i].startswith(" ") or raw_lines[i].strip() == ""
                ):
                    collected.append(raw_lines[i].strip())
                    i += 1
                fields[key] = " ".join(c for c in collected if c)
                continue
            fields[key] = val.strip('"').strip("'")
        i += 1

    return fields, text[m.end():]


def discover_skills():
    """
    Return a sorted list of (folder_path, fields_dict) for every folder under
    skills/ that has a SKILL.md with parseable frontmatter. Folders without
    valid frontmatter are silently skipped here — validate_skill.py is the
    place that reports on them as errors.
    """
    if not SKILLS_DIR.exists():
        return []

    results = []
    for folder in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        skill_md = folder / "SKILL.md"
        if not skill_md.exists():
            continue
        fields, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        if fields:
            results.append((folder, fields))
    return results
