# ISS V2 — Implementation backlog readiness audit (2026-10-12)

**Status:** PLANNING AUDIT ONLY. No feature code changed, no tests executed. Based on `docs/implementation/backlog.json`, `backlog-coverage.json`, `implementation-readiness.json`, Product Spec, architecture, and approved DR-V2-001…005. This is additive; do not replace historical artifacts.

## Numeric audit
- 60 tasks across 10 waves, all `PLANNED` in backlog.json.
- 298 atomic ENG requirements, 295 mandatory, 295 assigned to backlog tasks according to `backlog-coverage.json`. These are aggregate coverage assertions, not proof of executable tests.
- **11 tasks show requirements=0 and linked_tests=0 in backlog.json:** IMP-001, IMP-018, IMP-020, IMP-026, IMP-033, IMP-045, IMP-056, IMP-057, IMP-058, IMP-059, IMP-060. Zero is a mapping/metadata gap, not evidence that no source requirement exists.
- **Four tasks have fewer linked tests than requirements:** IMP-006 (9/8), IMP-023 (9/8), IMP-027 (4/3), IMP-051 (8/7). Counts alone cannot identify the missing exact test IDs; inspect atomic mappings.
- `implementation-readiness.json` declares `product_owner_decisions_required:0`; this is an earlier snapshot, not a current contract-readiness verdict.

## Approved decision → task mapping

| Decision | Primary task(s) | Dependency / gate | Next required contract |
| --- | --- | --- | --- |
| DR-V2-001 Timeline repeat / completed visuals | IMP-020 (0/0), IMP-015 (17/17), IMP-018 (0/0) | IMP-013 and IMP-015 before IMP-020 | visitor session, visual snapshot, repeat policy and side-effect suppression |
| DR-V2-002 per-Content position | IMP-022 (11/11), IMP-026 (0/0), IMP-024 (5/5) | IMP-015, IMP-017, IMP-014, IMP-006 before IMP-022 | position key/lifetime, explicit resume, seekable and end behavior |
| DR-V2-003 Always Preload | IMP-027 (4/3), IMP-006 (9/8), IMP-037 (19/19) | IMP-022 and IMP-023 before IMP-027 | schema/compile hint, targeted preparation and readiness/error |
| DR-V2-004 developer hotkeys | IMP-046 (9/9), IMP-048 (1/1) | IMP-043, IMP-042, IMP-044 before IMP-046 | immutable physical shortcut, additional shortcut config/conflicts |
| DR-V2-005 baseline profile | IMP-060 (0/0), IMP-056 (0/0), IMP-047 (5/5) | requires approved measurable baseline | hardware/workload/duration/pass-fail numerical values **NOT APPROVED** |

Mappings above are **planning inferences**, not verified exact ENG-ID assignments.

## Priority review: tasks with zero direct counts

| Task | Why zero-count matters | Proposed resolution |
| --- | --- | --- |
| IMP-001 | foundation work may be engineering infrastructure rather than product behavior | define explicit infrastructure exit criteria, not invented product IDs |
| IMP-018 | Page navigation/transition is product-visible | map PS-FLOW/PS-TRANS and relevant ENG IDs to tests |
| IMP-020 | Timeline is product-visible and DR-V2-001 applies | add timeline behavior contract and executable cases |
| IMP-026 | media controls are product-visible | map PS-MEDIA-004/011 and relevant ENG IDs |
| IMP-033 | Form Widget is product-visible | map Widget Contract and CASE evidence |
| IMP-045 | same-PC multi-display coordination is system behavior | map architecture invariants and integration tests |
| IMP-056 | kiosk/startup behavior is deployment behavior | define Windows installation and recovery tests |
| IMP-057 | V1 compatibility suite is a verification work package | map all 178 V1 IDs to dispositions and actual test IDs |
| IMP-058 | CASE acceptance suite is a verification work package | map 48 CASE IDs and fixture/test IDs |
| IMP-059 | TZ acceptance suite is a verification work package | map 128 TZ IDs with provenance |
| IMP-060 | soak/chaos acceptance suite is a verification work package | await approved C-25 numeric profile; define methodology first |

## Suggested staged authorization

**Stage A — source and contracts (now):** verify exact atomic requirement mappings and provenance, resolve 11 zero-count and four 1-test shortfall records, reconcile NEW history, formalize 10 missing contracts and DR-V2-001…005. Do not change historical source IDs.

**Stage B — narrow infrastructure pilot (conditional):** IMP-001 only, in an isolated implementation branch, after explicitly defining its acceptance checklist and comparing existing prototype structure. No product feature claim. Use real build/test results and human/agent-reviewed screenshots if UI is affected.

**Stage C — first bounded product batch (conditional):** IMP-002 Project Model types and IDs; depends on IMP-001. Require schema/invariant tests, source-ID links and review of existing project files. Avoid starting Page Timeline or Media Player before their contracts are approved.

**Stage D — wave-based delivery:** incremental dependency-aware batches, max five fix/retest cycles per batch, verified functional and visual evidence. Never treat zero-count tasks as automatically optional.

## Release gates
1. Requirements provenance and traceability (source family, exact ID, status).
2. Engineering contracts and open policy closure.
3. Acceptance manifest (test IDs, fixtures, expected outcomes).
4. Actual execution and artifact review.
5. Product-owner acceptance of product-visible behavior; C-25 numbers must be approved before performance certification.

**Do not merge PR #1 into main yet.** This document is a backlog audit, not a CI result.
