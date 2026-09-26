# Security Policy

## Scope

This repository contains Agent Skills — markdown instructions and helper scripts consumed by AI agents (Claude and compatible tools). Security concerns here typically look different from a normal codebase, and include:

- A skill's instructions could cause an agent to take an unsafe or unintended action (e.g. exfiltrate data, call an unapproved endpoint, execute unsafe code).
- A bundled script (anything under a skill's `scripts/`) contains a vulnerability, or behaves unexpectedly outside its intended sandboxed use.
- Prompt-injection-style content embedded in a skill's reference material.

## Reporting a Vulnerability

Please **do not** open a public issue for a security concern. Instead, report it privately:

- Open a [private security advisory](https://github.com/Naxasware/Naxasware-Agent-Skills/security/advisories/new) on this repository, or
- Contact the maintainers directly through the Naxasware organization.

Please include:

- Which skill (or repo-level script) is affected
- The specific behavior or instruction you're concerned about
- A minimal reproduction (a prompt, or the exact instruction text) if possible

We'll acknowledge reports as soon as we can and aim to follow up with a fix or a clear explanation within a reasonable timeframe. Please give us a chance to address a report before any public disclosure.

## Supported Versions

This repository does not currently maintain multiple parallel versions — skills are updated in place on `main`, with changes tracked in [CHANGELOG.md](CHANGELOG.md). Security fixes land on `main`.
