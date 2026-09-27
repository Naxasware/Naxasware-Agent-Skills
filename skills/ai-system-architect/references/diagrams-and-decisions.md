# Diagrams, Decisions, Risks, and Validation

## Diagrams

Generate diagram specifications in a text-based format — Mermaid is preferred for anything going into a file (renders natively in most Markdown viewers and in published artifacts); ASCII or plain structured text is fine for an in-chat answer. Useful diagram types, only as many as the project needs:

- **Context diagram** — users → system → external systems
- **Container diagram** — frontend → API → services → database
- **Component diagram** — internal component relationships
- **Data flow diagram**
- **Deployment diagram**
- **Sequence diagram** — for a specific important interaction
- **AI architecture diagram** — when AI is in scope
- **Network / trust boundary diagram** — when security boundaries are non-trivial

Every diagram should have a clear single purpose, meaningful labels (not generic "Service A / Service B"), and should avoid unnecessary detail that isn't load-bearing for its purpose. Show direction, external systems, and important boundaries where relevant. Most importantly: **the diagram and the written architecture must not contradict each other** — if a component appears in one, it needs to appear in the other, or the document has silently forked into two different architectures.

## Architecture Decision Records

Full template (see `architecture-patterns.md` for the condensed version and a worked example):

```
ADR-XXX
Title
Status              Proposed / Accepted / Rejected / Deprecated / Superseded
Context
Problem
Options Considered
Decision
Rationale
Trade-offs
Consequences
Related Requirements
```

Write an ADR for decisions that are architecturally significant and non-obvious — not for every small implementation detail, which would dilute the record and make the important decisions harder to find.

## Architecture risks

```
RISK-XXX
Risk
Cause
Impact
Likelihood         qualitative (Low/Medium/High) unless the user has real data for a number
Severity
Mitigation
Contingency
Owner              if known; otherwise leave open
```

Don't invent a precise likelihood percentage without a basis — a qualitative rating that's honest about its own uncertainty is more useful than a fabricated number that looks more rigorous than it is.

## Architecture debt

Distinguish three categories clearly, since they call for different responses:

- **Current problem** — actively causing pain now
- **Future risk** — not a problem yet, but will become one under a foreseeable condition (e.g. "will not survive 10x traffic")
- **Optional improvement** — would be nice, not blocking anything

Sources to look for: shortcuts taken under time pressure, temporary architecture that was never revisited, missing abstractions, weak module boundaries, scaling limitations, security debt, and operational debt (things nobody is actually monitoring).

## Architecture validation

Before finalizing, check the architecture against each of these — and say explicitly where it falls short rather than only listing strengths:

- **Functional fit** — does it satisfy the stated functional requirements?
- **Quality fit** — does it address the quality attributes that were actually flagged as important?
- **Security** — are the security concerns that matter for this project's data addressed?
- **Data** — is ownership of every major entity clear?
- **Integration** — are all external dependencies defined with a failure mode?
- **Failure** — what happens when each major component goes down?
- **Scale** — can it handle the estimated growth, or does it have a known ceiling?
- **Cost** — is it compatible with any stated budget constraint?
- **Team** — can the team that exists actually build and operate this, not a hypothetical ideal team?
- **Complexity** — is there any piece of architecture that isn't earning its cost?

## Qualitative fitness — never a fabricated numeric score

Do not produce a generic numeric "architecture score" (e.g. "82/100") unless the user has explicitly defined their own measurable scoring framework — an unearned number reads as more rigorous than it is and invites false confidence. Instead, produce a qualitative assessment per dimension:

```
Requirement coverage      Strong / Partial / Unknown
Security coverage         Strong / Partial / Unknown
Scalability               Strong / Partial / Unknown
Operational readiness     Strong / Partial / Unknown
```
