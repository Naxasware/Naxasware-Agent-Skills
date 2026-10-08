# Changelog

All notable changes to this repository and the skills it contains are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- Added the requirements → architecture → workflow chain: three skills that hand off through a Chain header, a Handoff block and shared, byte-identical `idscan.py` / `validate_chain.py` scripts (see each skill's `references/chaining.md`).
- Restructured the repository: skills now live under `skills/<name>/` instead of the repo root, to keep room for more skills without cluttering the top level.
- Added repository scaffolding: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `NOTICE`, issue/PR templates, and a CI workflow that validates skill structure on every push and pull request.
- Added `scripts/validate_skill.py`, a repo-level structural linter for skills (frontmatter presence, description length, name/folder match).

## [ai-requirements-analyst 1.1.0]

### Added
- Chain mode (stage 1 of 3): Chain header, Handoff block (must-cover IDs, locked decisions, blocking questions, next A/Q numbers), and `references/chaining.md`, the shared guide for running requirements → architecture → workflow.
- `validate_ids.py` now reports every functional requirement that has no acceptance criterion (`AC-<FR number>-<n>`), and acceptance criteria that match no requirement.
- Shared `scripts/idscan.py` (one definition grammar for table rows, bullets, bold and plain lines; range citations) and `scripts/validate_chain.py` (hand-off checks across the three documents).
- Guidance: a "PRD" request maps to a Full SRS; numeric planning assumptions must state their basis or be written as Unknown.

### Changed
- `validate_ids.py` accepts table-row and bullet definitions (previously reported as "never defined").

## [ai-system-architect 1.0.0]

### Added
- Initial release of the `ai-system-architect` skill (drivers, quality attributes, options and trade-offs, selected architecture, components, data/API/integration/security/AI architecture, ADRs, risks, validation, blueprint).
- Chain mode (stage 2 of 3): Chain header, requirements-coverage table, Handoff block; `COMP-###` component IDs; A/Q numbering continues from upstream.
- `scripts/validate_ids.py` (accepts bold, table, bullet and plain definitions; `--upstream` or the Chain header verifies cited requirement IDs), shared `scripts/idscan.py`, `scripts/validate_chain.py`, and `references/chaining.md`.

## [ai-workflow-architect 1.0.0]

### Added
- Initial release of the `ai-workflow-architect` skill (complexity ladder, reliability, human-in-the-loop, AI/agent/tool/MCP architecture, security, observability, testing, cost, ADRs, diagrams, implementation blueprint) with six worked examples.
- Validators: `validate_workflow.py` (sections by depth, step tables, human and external-wait timeouts, traceability, unlabeled money/percentage/volume figures anywhere, secrets, agent specs), `validate_ids.py`, `validate_diagrams.py`, `generate_report.py` (depth read from the document).
- Chain mode (stage 3 of 3): Chain header, `Depth:` line, upstream-coverage table, `validate_chain.py`, shared `idscan.py`, and `references/chaining.md`; `--upstream` or the Chain header lets the validators verify cited upstream IDs.
- Reliability guidance for waiting on an external party (wait limit, reminder, expiry path, late reply, matching).

## [ai-requirements-analyst 1.0.0]

### Added
- Initial release of the `ai-requirements-analyst` skill: turns business ideas, notes, and existing requirements docs into structured, implementation-ready requirements (Discovery, Extraction, Analysis/Audit, Generation, MVP Definition, and Change Analysis modes).
- Reference material for the requirement ID scheme and field structures, output templates and modes, the requirements quality framework, and a worked example.
- `scripts/validate_ids.py` for catching duplicate or dangling requirement IDs in a finished document.
