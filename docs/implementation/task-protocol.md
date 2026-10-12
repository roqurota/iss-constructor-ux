# AI Implementation Task Protocol

## Purpose
Coding agents receive bounded implementation packets, not the entire documentation corpus by default.

## Task packet
Every implementation task MUST contain:
- Task ID.
- Exact ENG requirement IDs.
- Required architecture decisions/invariants.
- Required data-model/runtime contracts.
- Dependency tasks.
- Acceptance TEST IDs.
- Allowed code scope.
- Explicit non-goals.
- Completion report format.

## Size rule
Prefer one coherent subsystem slice that an agent can implement and test without redefining architecture. Split a task when it crosses unrelated ownership/lifecycle boundaries.

## Coding-agent completion report
Return:
1. `Implemented`: ENG IDs.
2. `Files changed`: exact paths.
3. `Tests`: TEST IDs + result.
4. `Validation/build`: commands + result.
5. `Architecture deviations`: `NONE` or explicit gap.
6. `Remaining`: only blockers/dependencies.

## Review-agent protocol
The reviewer receives the same task packet plus diff/test output and MUST independently verify:
- each ENG contract;
- lifecycle/cancellation;
- invalid/stale async behavior;
- no hidden parallel architecture;
- no unrelated refactor;
- compatibility implications;
- test adequacy.

Reviewer outcome: `PASS | PASS_WITH_NOTES | FAIL`.
A FAIL cites ENG/TEST IDs and concrete evidence.

## Product Owner protection
Coding/review agents MUST use AGENTS.md escalation policy. Engineering ambiguity is resolved by architecture/review unless observable product behavior is genuinely undefined.
