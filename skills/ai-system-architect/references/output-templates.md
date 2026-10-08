# Output Templates

## Standard Output Package

When enough information exists to warrant a full document, these are the possible sections — **only include the ones you have real content for**; a document padded with empty or boilerplate sections undermines the whole point of a targeted architecture. State plainly when a section is skipped and why (usually: not enough information, or not applicable to this project).

```
01 Executive Architecture Summary
02 Business Context
03 Architecture Drivers
04 Requirements Summary (with a requirements-coverage table when upstream requirements exist)
05 Constraints
06 Assumptions
07 Quality Attributes
08 Scale Model
09 Architecture Principles
10 Architecture Options
11 Trade-off Analysis
12 Selected Architecture
13 System Context
14 Container Architecture
15 Component Architecture
16 Module Boundaries
17 Data Architecture
18 API Architecture
19 Integration Architecture
20 Event Architecture
21 Security Architecture
22 Authentication & Authorization
23 Infrastructure Architecture
24 Deployment Architecture
25 DevOps Architecture
26 Observability
27 Reliability & Disaster Recovery
28 Scalability
29 AI Architecture
30 Cost Considerations
31 Architecture Decisions
32 Architecture Risks
33 Architecture Debt
34 Diagrams
35 Implementation Blueprint
36 Phased Roadmap
37 Architecture Validation
38 Open Questions
39 Handoff to next stage   (only when the document feeds ai-workflow-architect; see chaining.md)
```

For a Quick Analysis, Discovery-style answer, or a short comparison, pick only the handful of sections that actually answer what was asked — most of this list exists for the rare case that genuinely needs a Full SRS-to-architecture handoff.

## Implementation blueprint

The architecture should conclude with a practical, project-specific phased plan — not a generic template. A representative shape:

```
Phase 1   Foundation
Phase 2   Authentication + core domain
Phase 3   Primary workflows
Phase 4   Integrations
Phase 5   AI features (if applicable)
Phase 6   Observability + hardening
Phase 7   Production readiness
```

Adjust phase count, order, and content to what this specific project actually needs — an MVP-mode output might collapse this to three phases; an enterprise migration might need substantially more granularity, especially around the transition architecture from `architecture-patterns.md`'s Evolution mode.

## Technology stack recommendation

When a concrete stack recommendation is warranted, structure it by layer:

```
Frontend / Backend / Database / Cache / Queue / Storage /
Authentication / Hosting / Monitoring / AI-LLM / Search / CI-CD
```

For each technology actually recommended (skip layers the project doesn't need):

```
Technology
Purpose
Why              tie back to a specific driver or constraint
Alternative      what else was considered
Trade-off        what's given up by choosing this one
```

A stack list with no "why" column is exactly the technology-before-requirements failure mode this whole skill exists to prevent — never produce one without the rationale attached.
