#!/usr/bin/env python3
"""
Package one or all skills into `.skill` files (zip archives, with the skill's
folder as the top-level entry) under dist/.

Usage:
    python3 scripts/package_skill.py                  # package every skill under skills/
    python3 scripts/package_skill.py skills/<name>     # package just one
"""

import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_utils import discover_skills, REPO_ROOT  # noqa: E402

DIST = REPO_ROOT / "dist"


def package(folder: Path) -> Path:
    DIST.mkdir(exist_ok=True)
    out_path = DIST / f"{folder.name}.skill"
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(folder.rglob("*")):
            if file.is_file():
                zf.write(file, arcname=str(file.relative_to(folder.parent)))
    print(f"Packaged {folder.name} -> {out_path.relative_to(REPO_ROOT)}")
    return out_path


def main():
    args = sys.argv[1:]
    if args:
        targets = [Path(a).resolve() for a in args]
        for t in targets:
            if not (t / "SKILL.md").exists():
                print(f"{t} has no SKILL.md — not a valid skill folder.")
                sys.exit(1)
    else:
        targets = [folder for folder, _ in discover_skills()]

    if not targets:
        print("No skills found to package.")
        sys.exit(0)

    for t in targets:
        package(t)


if __name__ == "__main__":
    main()
