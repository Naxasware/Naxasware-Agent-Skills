# Contributing

Thanks for considering a contribution. This repo holds Agent Skills — self-contained instruction packages — so most contributions fall into one of: proposing a new skill, improving an existing one, or fixing a bug/inconsistency.

## Proposing a new skill

Before writing anything, open an issue using the **New skill proposal** template (or start a discussion) covering:

1. What should this skill enable an agent to do?
2. When should it trigger — what phrases or contexts?
3. What's the expected output (a document? a file? an in-chat answer?)
4. Does it need bundled scripts/references, or is it instructions-only?

This avoids overlapping work and gets early feedback on scope before you invest time in a full draft.

## Skill structure and conventions

Every skill lives at `skills/<skill-name>/` and must contain at least a `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name          # matches the folder name, lowercase, hyphen-separated
description: >
  What the skill does AND when to use it. This is the primary triggering
  mechanism for agents deciding whether to consult the skill, so be specific
  and err toward over-triggering rather than under-triggering. Include
  concrete phrases a real user might say. Maximum 1024 characters.
---
```

Guidelines, in rough order of importance:

- **The description is the trigger.** Agents decide whether to open a skill based on `name` + `description` alone before reading the body. List concrete trigger phrases and contexts, not just an abstract capability statement.
- **Progressive disclosure.** Keep `SKILL.md` itself under ~500 lines. Anything longer, more specialized, or only occasionally needed (detailed schemas, worked examples, per-framework variants) belongs in `references/` with a clear pointer from `SKILL.md` about when to read it.
- **Explain the why, not just the rule.** Prefer explaining the reasoning behind an instruction over a bare imperative — agents follow reasoned guidance more robustly than rigid ALWAYS/NEVER lists, and it's easier for the next contributor to know when an exception is reasonable.
- **Scripts are for determinism.** If a skill's instructions would have every invocation reinvent the same helper code (a validator, a converter, a report generator), bundle it in `scripts/` instead and have `SKILL.md` call it.
- **No secrets, no unsafe execution.** Skills should not embed credentials, call out to unapproved endpoints, or ask an agent to do anything that would surprise a user reading the skill's own description.

## Before opening a PR

Run the repo-level validator against your skill:

```bash
python3 scripts/validate_skill.py skills/<skill-name>
```

This checks frontmatter presence, description length, name/folder match, and basic structural issues. It doesn't (and can't) judge whether the skill's actual instructions are good — that still needs a human read and, ideally, a couple of test prompts run against it.

## Pull requests

- One skill (or one focused change) per PR where possible.
- Fill in the PR template, including the test prompts you ran and what the output looked like.
- CI runs `validate_skill.py` against any changed skill automatically.

## Code of Conduct

Participation in this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
