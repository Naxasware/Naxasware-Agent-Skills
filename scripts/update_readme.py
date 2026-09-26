#!/usr/bin/env python3
"""
Regenerate the skill catalog table in README.md from each skill's SKILL.md
frontmatter, so the README can never silently drift out of sync with what's
actually in skills/.

Relies on two markers already present in README.md:

    <!-- SKILLS_TABLE_START -->
    ...generated table goes here...
    <!-- SKILLS_TABLE_END -->

Usage:
    python3 scripts/update_readme.py            # rewrite README.md in place
    python3 scripts/update_readme.py --check    # exit 1 if README.md would change, without writing (used in CI)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_utils import discover_skills, REPO_ROOT  # noqa: E402

START = "<!-- SKILLS_TABLE_START -->"
END = "<!-- SKILLS_TABLE_END -->"
README = REPO_ROOT / "README.md"
MAX_DESC_LEN = 220


def build_table() -> str:
    skills = discover_skills()
    if not skills:
        return "_No skills yet — see [CONTRIBUTING.md](CONTRIBUTING.md) to add one._"

    lines = ["| Skill | Description |", "|---|---|"]
    for folder, fields in skills:
        name = fields.get("name", folder.name)
        desc = fields.get("description", "").strip()
        if len(desc) > MAX_DESC_LEN:
            # Truncate at a word boundary — the full description lives in the
            # skill's own SKILL.md; the README table is a catalog, not the source.
            desc = desc[: MAX_DESC_LEN - 3].rsplit(" ", 1)[0] + "..."
        desc = desc.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| [`{name}`](skills/{folder.name}) | {desc} |")
    return "\n".join(lines)


def main():
    check_only = "--check" in sys.argv[1:]

    if not README.exists():
        print("README.md not found.")
        sys.exit(1)

    content = README.read_text(encoding="utf-8")
    if START not in content or END not in content:
        print(
            f"README.md is missing the {START} / {END} markers — "
            "can't safely regenerate the table. Add them around the skill "
            "table manually once, then this script can take over."
        )
        sys.exit(1)

    before, rest = content.split(START, 1)
    _, after = rest.split(END, 1)
    new_content = f"{before}{START}\n{build_table()}\n{END}{after}"

    if new_content == content:
        print("Skill table is already up to date.")
        sys.exit(0)

    if check_only:
        print(
            "README.md skill table is out of date. Run "
            "`python3 scripts/update_readme.py` and commit the result."
        )
        sys.exit(1)

    README.write_text(new_content, encoding="utf-8")
    print("Updated README.md skill table.")


if __name__ == "__main__":
    main()
