# AI Workflow Architect

Design reliable, scalable, secure, and implementation-ready AI workflows from business requirements.

This skill turns a business process or automation idea into a workflow architecture: what triggers it, how data moves, which steps are plain logic, which use an LLM, where an agent is genuinely justified, which tools and integrations are involved, where humans approve, and how failures, retries, security, observability, scale and cost are handled — finishing in an implementation blueprint with traceable requirements, tasks and tests.

It designs the architecture *behind* the automation. It does not generate platform-specific workflow exports, and it does not assume any particular platform, model vendor or MCP server.

## What's inside

```
ai-workflow-architect/
├── SKILL.md          — the instructions an agent follows (start here)
├── references/       — detail loaded only when needed (methodology, reliability, patterns,
│                       AI, agents, tools, MCP, security, observability, testing, cost,
│                       diagrams, ADR/risk templates, output schema)
├── examples/         — six worked architectures (Quick, Standard, Full); invented scenarios
├── scripts/          — optional Python 3 (standard library only) validators and report generator
└── README.md
```

## Using it

**Claude / Claude Code:** install the packaged `.skill` file or copy this folder into your skills directory.

**Other agents:** load `SKILL.md`, then `references/` and `examples/` as the instructions point to them. Nothing in the method requires Claude-specific tools, and the analysis works without running any script.

## Optional scripts

```bash
python3 scripts/validate_workflow.py architecture.md --depth standard   # sections, step coverage, traceability, secrets
python3 scripts/validate_ids.py architecture.md                         # duplicate / dangling / malformed IDs
python3 scripts/validate_diagrams.py architecture.md                    # Mermaid/PlantUML lint + ID consistency
python3 scripts/generate_report.py architecture.md -o report.md         # summary report
```

All of `examples/*.md` pass these checks at the depth stated in each file.

## Principles in one breath

Business process before tools; deterministic logic before AI; AI before agents, and agents only with a stated justification; every external action has failure handling, a timeout and duplicate protection; risky actions get human approval; unknowns stay unknown and assumptions stay labeled; complexity must be justified.
