# Changelog

All notable changes to this repository and the skills it contains are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- Restructured the repository: skills now live under `skills/<name>/` instead of the repo root, to keep room for more skills without cluttering the top level.
- Added repository scaffolding: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `NOTICE`, issue/PR templates, and a CI workflow that validates skill structure on every push and pull request.
- Added `scripts/validate_skill.py`, a repo-level structural linter for skills (frontmatter presence, description length, name/folder match).

## [ai-requirements-analyst 1.0.0]

### Added
- Initial release of the `ai-requirements-analyst` skill: turns business ideas, notes, and existing requirements docs into structured, implementation-ready requirements (Discovery, Extraction, Analysis/Audit, Generation, MVP Definition, and Change Analysis modes).
- Reference material for the requirement ID scheme and field structures, output templates and modes, the requirements quality framework, and a worked example.
- `scripts/validate_ids.py` for catching duplicate or dangling requirement IDs in a finished document.
