# ISS V2 — Engineering contract gap register (2026-10-12)

**Status:** Draft engineering handoff; NOT an approved amendment to original specifications, NOT implementation evidence. This is an additive companion to `SOURCE-RECONCILIATION-AUDIT-2026-10-12.md` and DR-V2-001…005.

## Source/approval distinctions
- **APPROVED** = product owner decision of 2026-10-12.
- **EXISTING** = older source/architecture requirement; still must reconcile with later decisions.
- **PROPOSED** = implementation contract suggestion requiring engineering review and, where product-visible, owner approval.
- **OPEN** = missing definition; do not silently default.
- **TEST PLAN** = acceptance case to implement; not a passed test.

### EC-001 — Timeline visitor-session repeat and completed visuals (DR-V2-001)
**APPROVED:** `Once per Visitor Session`, `Every Entry`, `Once per Runtime Session` as applicable (PS-TIME-003); Page re-entry Replay or Completed Visual State restore without re-running side effects (PS-TIME-004/005/006). **EXISTING:** Page runtime always fresh on entry; Page Leave cancels Page-owned work (A-017; Runtime State Model). **PROPOSED:** keep repeat flags and completed-visual snapshot outside PageRuntime in an appropriate surviving Screen/visitor-session store; apply restored visual state as a pure projection, never replay action handlers. Do not infer global persistent state or general Repeat/Wait Until language. **OPEN:** what starts/ends Visitor Session; which visual properties are restorable; whether navigation/reset/screensaver affects visitor boundary; flag/snapshot invalidation and priority among policies. **TEST PLAN:** enter→complete→leave→return restores visuals, emits no duplicate TCP/UDP or other side effects; fresh visitor resets only visitor-scoped flags; Screen reset behaves per approved scope.

### EC-002 — Screen Media Player displaced Content position (DR-V2-002)
**APPROVED:** preserve per-Content position when displaced; exactly one Screen-owned system player; no automatic resume implied. **EXISTING:** A-019 and Runtime State Model Screen Media Player replacement/cancellation; PS-MEDIA-011 uses older multiple designed players wording superseded by architecture. **PROPOSED:** keyed position map in Screen session, with generation token to reject stale seek/readiness; explicit resume action uses saved position. **OPEN:** Content identity/key; position lifetime on Reset Screen, Build reload, Player restart; near-end and live/nonseekable behavior; playlist/item/range interaction; whether optional automatic resume is supported/configured. **TEST PLAN:** A→B→A preserves position when explicitly resumed; no two system players; stale A preparation cannot steal playback; reset and unseekable cases after contract approved.

### EC-003 — Manual Always Preload (DR-V2-003)
**APPROVED:** author-selectable Always Preload asset flag, within on-demand + targeted preparation; no global predictive cache. **EXISTING:** PS-PRE-004; Architecture §20/A-033; Project Data Model §35 currently describes hint as future. **PROPOSED:** typed opt-in property in asset authoring model and compiled runtime asset metadata, with bounded targeted preparation and observable readiness/error status. **OPEN:** precise flag schema and propagation, startup timing, readiness requirement, error timeout, priority, resource caps and when preloaded data can be evicted. **TEST PLAN:** flagged asset prepared on approved trigger; nonflagged assets not globally loaded; failures visible to technician and do not crash unrelated Screen.

### EC-004 — Developer Mode hotkeys (DR-V2-004)
**APPROVED:** immutable physical-key Ctrl+Shift+D plus optional configurable technician hotkey. **EXISTING:** Architecture §25.2; PS-DIAG-001. **PROPOSED:** store additional hotkey in PlayerLocalConfig (not .iss), validate conflicts, keep mandatory chord registered independently. **OPEN:** allowed shortcut grammar, reserved combinations, conflict policy, keyboard focus, technician access restrictions. **TEST PLAN:** mandatory physical chord works under two keyboard layouts; custom chord works; malformed/custom collision cannot remove mandatory chord.

### EC-005 — One baseline installation profile (DR-V2-005)
**APPROVED:** exactly one initial baseline hardware profile for operational acceptance. **NOT APPROVED:** CPU/GPU/RAM, number/resolution of displays, test workload, soak duration, memory growth, response/latency budgets, acceptance thresholds. **OPEN:** all numeric criteria and reproducible measurement methodology. **TEST PLAN:** cannot be declared PASS until these are explicitly agreed.

## Remaining ten MISSING CONTRACT audit entries
| Audit ID | Area | Minimum engineering output | Status |
| --- | --- | --- | --- |
| C-10 | Runtime state ownership/serialization | typed state boundaries, lifecycle and reset invariants | OPEN |
| C-12 | Wait Until / trigger re-entry | action-flow state machine, cancellation, queue/parallel policy; reconcile PS-ACT-003/005 vs runtime deferral | OPEN; potential product-visible conflict |
| C-14 | Timeline/seek semantics | event crossing/re-fire/loop and clock contract | OPEN |
| C-19 | Asset/media preparation | readiness, cancellation, failure and priority contract | OPEN |
| C-20 | Widget and forms behavior | schema, validation, submission, error contracts | OPEN |
| C-21 | Components and instance propagation | update/version/override/structural conflict contract | OPEN |
| C-22 | Build/persistence | snapshot/atomicity/dependency and migration contract | OPEN |
| C-23 | Player deployment/local config | configuration lifecycle, display mapping, recovery contract | OPEN |
| C-24 | Preview/Player parity | shared runtime equivalence and evidence contract | OPEN |
| C-26 | Operational acceptance | measurable workload, hardware profile and pass/fail thresholds | OPEN; overlaps EC-005 |

**Caution:** The ten topic labels above are a working interpretation of prior audit findings, not independently certified verbatim titles from `decision-review.md`. Reconcile against that original audit before converting to authoritative tracking IDs.

## Explicit gating rules
1. No existing source text is overwritten by this document.
2. Add test IDs and ENG mappings only after confirming exact source rows; do not invent V1/TZ/CASE/NEW identifiers.
3. Distinguish **source coverage**, **engineering task assignment**, **test specification**, **test execution**, and **visual review** as separate gates.
4. No product-visible open policy is silently closed by a suggested default.
5. Do not merge draft PR #1 or launch broad autonomous feature implementation until the reconciliation gate is signed off.
