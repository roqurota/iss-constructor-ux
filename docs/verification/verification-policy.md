# Verification Policy

## Requirement-to-test rule
Every atomic requirement marked MUST that changes executable behavior requires automated verification unless technically impossible. If impossible, document the reason and define a deterministic manual/integration acceptance procedure.

## Test naming
Prefer IDs such as:
- `TEST-RT-001`
- `TEST-MEDIA-006`
- `TEST-BUILD-003`
and reference the corresponding `ENG-*` requirement in the test name/metadata/comment.

## Review-agent checklist
A review agent MUST check:
1. requirement IDs addressed;
2. no unrelated architecture changes;
3. lifecycle ownership/cancellation;
4. stale async completion safety;
5. validation/error behavior;
6. Preview/Player semantic parity where relevant;
7. V1 compatibility implications;
8. tests for changed MUST contracts.

## Definition of done for an implementation task
- implementation complete;
- affected automated tests pass;
- new MUST behavior has tests;
- validation/build checks pass where relevant;
- no unexplained architecture deviation;
- agent reports requirement IDs, code files and test IDs.
