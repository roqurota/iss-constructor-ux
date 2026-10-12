# Agent Orchestration Guide

## Roles
**Architecture/Lead Agent**
- selects the next dependency-ready IMP task;
- performs preflight;
- resolves engineering gaps;
- escalates only genuine Product Gaps.

**Coding Agent**
- receives one IMP task packet plus linked contracts;
- implements only allowed scope;
- adds/runs linked tests.

**Review Agent**
- independently reviews against ENG/TEST IDs;
- does not accept “works on my machine” as contract proof.

**Test Agent**
- runs targeted tests plus relevant regression set;
- records deterministic failures by TEST/ENG ID.

## Task state machine
`PLANNED → PREFLIGHT → READY → IMPLEMENTING → REVIEW → TEST → DONE`
Failure returns to `IMPLEMENTING`; architecture gap returns to `PREFLIGHT`; Product Gap pauses only affected task.

## Preflight gate
Before `READY`, Lead Agent MUST ensure:
1. dependencies DONE;
2. every executable behavior has ENG IDs;
3. mandatory ENG IDs have TEST IDs;
4. no unresolved architecture contradiction;
5. code ownership/scope is known.

Tasks with architecture-only requirements (currently some later compatibility/UX tasks) MUST be atomized during preflight before coding.

## Parallelism
Tasks in the same wave may run in parallel only when their dependency sets are satisfied and their allowed code scopes do not create high-conflict edits. Lead Agent owns conflict avoidance.

## Context minimization
Give agents:
- AGENTS.md;
- the single IMP task;
- exact linked requirement files;
- exact relevant architecture/data/runtime contracts;
- dependency public interfaces;
- relevant tests.
Do not load the whole historical corpus unless resolving traceability/compatibility.

## PO workload rule
A blocked task caused by missing code, missing test, uncertain algorithm, package design, performance technique or internal representation is NOT a Product Owner escalation.
