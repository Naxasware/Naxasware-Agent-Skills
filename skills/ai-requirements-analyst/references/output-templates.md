# Modes and Output Templates

## The six analysis modes

These describe *what kind of input/task you're dealing with*, not a document format — pick the one that matches what's in front of you (a request can span more than one).

1. **Discovery** — user has only an idea. Output: problem statement, business objective, stakeholders, initial scope, assumptions, unknowns, discovery questions.
2. **Requirements Extraction** — user gave existing information (notes, a process description, a document). Extract actors, processes, requirements, business rules, constraints, dependencies, assumptions, gaps — don't re-ask for what's already there.
3. **Requirements Analysis / Audit** — user gave an existing requirements doc and wants it checked. Check completeness, consistency, ambiguity, contradictions, testability, feasibility, scope, and missing edge cases/roles/permissions/NFRs. See `quality-framework.md`.
4. **Requirements Generation** — produce a complete spec from whatever's available.
5. **MVP Definition** — sort functionality into must-have / should-have / future / out-of-scope, anchored to the business objective, not to what's easiest to build.
6. **Change Analysis** — user is changing an existing requirement. Identify what's affected: requirements, workflows, roles, business rules, data, integrations, acceptance criteria, and possible scope implications. Don't just describe the new requirement — trace its ripple effects through the rest of the spec.

## The eight output shapes

Match the shape to what the user actually needs, not to how impressive a longer document looks:

| Shape | When to use it |
|---|---|
| Quick Analysis | A short, structured answer — a few key points, not a full document |
| Discovery Report | Early-stage idea, mode 1 |
| Full SRS | Comprehensive spec, most/all of the Standard Output Package below |
| Developer Handoff | Implementation-focused; heavy on FR/BR/DR/AC, light on business narrative |
| Product Brief | Business/product-focused; heavy on objective, scope, MVP, light on field-level detail |
| Requirements Audit | Review of an existing spec — findings-oriented, mode 3 |
| MVP Specification | Focused on first release only |
| Change Impact Report | Mode 6 output — what changed and what it touches |

If the user hasn't said which shape they want, infer from their input and say what you picked ("Since this is just an idea, here's a Discovery Report — let me know if you want it developed into a full spec").

## Standard Output Package (for Full SRS / Requirements Generation)

Only include sections you have real content for. Clearly label sections that are skipped for lack of information rather than quietly dropping them — the user should be able to tell "not applicable" apart from "not covered yet."

```
01 Executive Summary
02 Problem Statement
03 Business Objectives
04 Scope
05 Out of Scope
06 Stakeholders
07 Actors & Roles
08 Current-State Process
09 Future-State Process
10 Functional Requirements
11 User Stories
12 Use Cases
13 Business Rules
14 Data Requirements
15 Permissions
16 Non-Functional Requirements
17 Integrations
18 AI Requirements
19 Automation Requirements
20 Edge Cases
21 Acceptance Criteria
22 Prioritization
23 Assumptions
24 Constraints
25 Dependencies
26 Open Questions
27 Traceability Matrix
28 MVP Recommendation
29 Requirements Quality Assessment
30 Next Steps
```

For a Quick Analysis, Discovery Report, or Developer Handoff, pick the subset that fits — you don't need all 30 sections for a one-page idea.

## Current-state / future-state process notation

When there's a real existing process to document:

```
AS-IS: Trigger → Step → Decision → Action → Outcome
TO-BE: Trigger → System/User Action → Validation → Business Rule → Decision → Automation → Outcome
```

For AS-IS, only claim an inefficiency (duplication, delay, error-prone step, bottleneck) if the user's description actually supports it — don't assume the old process was bad just because it's manual.

For TO-BE, clearly separate three things that are easy to blur together: what's *required* behavior, what's a *recommended* improvement, and what's *optional* automation the user could add later.
