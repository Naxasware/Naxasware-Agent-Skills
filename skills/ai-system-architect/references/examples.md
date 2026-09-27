# Worked Example: Fleet Management for Six Vehicles

A compact walkthrough showing how a small input becomes a right-sized architecture — this is deliberately a short document, because the input doesn't justify a Full SRS-to-architecture handoff. It illustrates proportionality as much as it illustrates the method.

## Input

> "We need a fleet management system for six company vehicles. We want to track maintenance schedules, mileage, and which employee has which vehicle. Small internal team, maybe 15-20 employees will use it."

## 1. Business context

- **Problem:** vehicle assignments, mileage, and maintenance are presumably tracked informally today (not stated — flagged as an assumption).
- **Objective:** avoid missed maintenance and give visibility into who has which vehicle.
- **Users:** ~15-20 employees (stated), likely one or two fleet administrators (assumed — not stated who manages assignments).
- **Scope:** 6 vehicles, mileage tracking, maintenance schedules, assignment tracking.
- **Out of scope (assumed, flag as open question):** fuel cards, GPS tracking, cost accounting — not mentioned, worth confirming they're genuinely out.

## 2. Architecture drivers

```
AD-001  Small, fixed fleet size (6 vehicles) — scale is not a driver here
AD-002  Small user base (15-20) — no concurrency or throughput concerns
AD-003  Internal-only tool — no public-facing security surface
AD-004  Small team (assumed, based on "we" and internal framing) — favors low
        operational overhead over distributed-systems capability
```

No driver here points toward microservices, event streaming, or a specialized database — this is a strong signal for a simple architecture, not a gap in the analysis.

## 3. Selected architecture (ADR-001)

```
Decision: Single-service web application (traditional monolith) with a
relational database.
Context: 6 vehicles, ~20 users, internal tool, small team.
Alternatives: Modular monolith, microservices.
Reason: No driver identifies a need for independent scaling, independent
deployment, or team-boundary separation. A single deployable unit
minimizes operational overhead for a project this size.
Trade-off: Less structural enforcement of module boundaries than a
modular monolith would give — acceptable given the scope is unlikely to
grow substantially (flag as an assumption to revisit if scope expands).
```

## 4. Component sketch

```
Component: Web Application
Responsibilities: vehicle records, assignment tracking, maintenance
  schedule tracking, basic reminders
Owned data: vehicles, assignments, maintenance_records, employees
APIs: internal REST endpoints, no external API surface (AD-003)
Failure behavior: single point of failure, acceptable at this scale —
  flagged as an explicit trade-off, not hidden
```

## 5. Data architecture (sketch)

```
Vehicle          id, plate, model, current_mileage
Employee         id, name
Assignment       vehicle_id, employee_id, start_date, end_date (nullable)
MaintenanceEvent vehicle_id, type, due_mileage OR due_date, completed_at
```

## 6. What's flagged rather than decided

```
Q-001  Who administers assignments — is there a distinct admin role, or
       does every user have equal access?
Q-002  Are reminders needed (email/notification) or is a dashboard view
       sufficient?
A-001  Assumed no integration with a fuel-card or telematics system —
       confirm before finalizing scope.
```

## Why this stays short

A 38-section Standard Output Package would be almost entirely empty sections for a project this size — no meaningful integration architecture, no AI architecture, no multi-region concerns. The right-sized output here is: business context, drivers, one ADR, a component sketch, a data sketch, and open questions — nothing padded in to look more thorough than the input supports.
