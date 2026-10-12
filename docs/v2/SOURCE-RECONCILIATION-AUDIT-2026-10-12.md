# ISS V2 — Source reconciliation audit (2026-10-12)

**Status: DOCUMENTATION GATE NOT PASSED.** This is a source-level review, not implementation verification. Inspected recovered archive files on the GitHub branch and the approved DR-V2-001…005 overlay. Original specifications have not been modified.

## Confirmed
- GitHub compare with main reports **113 added/changed files** including the recovered archive and four previously created migration documents; source archive contains 108 files.
- Recovered archive includes Project Data Model, Runtime State Model, Product/Architecture/Widget source specifications, 60 implementation task documents, and engineering verification artifacts.
- `traceability-state.json` declares 354 source IDs: V1 178, TZ 128, CASE 48, missing 0; the TZ historical verbatim labels are explicitly **not** recovered.
- `backlog-coverage.json` declares 60 tasks in 10 waves, 298 atomic ENG requirements, 295 mandatory and all 295 directly assigned to backlog tasks. Assignment is **not** test execution or feature implementation.
- The historical NEW-F001…NEW-F895 register is **not present as an independently verified complete ID-by-ID decision artifact** in the inspected package. `traceability-audit.md` claims an earlier audit accounted for 895/895 but does not itself supply the 895 records.

## Conflicts and stale status statements

### R-01 — Historical traceability certification contradicts checkpoint
`docs/verification/traceability-checkpoint.md` explicitly states `TRACEABILITY_COMPLETE = false`, with TZ and CASE original approved atomic wording missing and rows pending source recovery. Later `traceability-certification.md` asserts 354/354 semantically mapped, and `traceability-state.json` sets semantic completion true while acknowledging TZ verbatim recovery false. These may reflect different certification standards, but the repository does **not** state one canonical gate for archival verbatim recovery versus semantic engineering coverage. **Action:** define separate gates and provenance, do not silently erase the checkpoint.

### R-02 — C-07 / DR-V2-003 missing in canonical data model
`docs/source/project-data-model.md` §35 says an explicit preload hint **may be added in the future**. The product owner has now **approved** author-set Always Preload. Add an explicit authoring property/asset association and compile/readiness contract through a reviewed additive schema amendment. Do not implement a predictive cache.

### R-03 — C-04 / DR-V2-001 conflicts with older Runtime State Model deferral
`docs/source/runtime-state-model.md` §28 defers general-purpose Repeat/Wait Until/Cancel Flow language. The approved decision retains Once per Visitor Session timeline policy and Completed Visual State restore; this does **not** authorize a general-purpose Repeat Flow language. The runtime model only documents Screen Session once flags and fresh Page runtime. **Action:** add distinct visitor-session lifecycle/visual snapshot contracts without breaking Page Leave cancellation.

### R-04 — C-06 / DR-V2-002 not formalized in media state
Runtime State Model Screen Media Player table describes replacement but not per-Content position retention. **Action:** define position map ownership, reset and explicit resume behavior, with seekability tests. No automatic resume inferred.

### R-05 — C-11 / DR-V2-004 not reflected in technician configuration contract
The fixed physical Ctrl+Shift+D chord remains mandatory. An additional configurable technician hotkey now needs schema, shortcut conflict policy and tests; the mandatory chord must not be removable.

### R-06 — C-25 / DR-V2-005 remains a numeric acceptance blocker
One baseline installation hardware profile approved **in principle**. Hardware specification, soak duration, response-time limits, resource growth and pass/fail numbers are NOT approved. Any operational-performance PASS would be unsupported.

### R-07 — Historical readiness indicators are stale
`implementation-readiness.json` states `product_owner_decisions_required: 0`; `traceability-certification.md` states Product Owner decisions required 0. Both predate the five 2026-10-12 decisions and their unresolved engineering contracts; preserve these files as historical snapshots and provide a current readiness gate overlay. This does **not** imply five product choices are still open.

### R-08 — C-12 / Flow control scope discrepancy
`docs/requirements/actions-triggers.md` lists initial Delay and If/Condition but omits Product PS-ACT-003 Wait Until and PS-ACT-005 re-entry policies. The Runtime State Model defers general-purpose Wait Until in §28. Prior decision review classified this MISSING CONTRACT, not an approved removal. **Action:** explicitly distinguish initial supported control steps, required preserved product capability, deferral/status and product-visible scope before implementation.

### R-09 — Machine-readable coverage is not runtime acceptance
`docs/verification/verification-policy.md` requires executable tests for MUST behavior. Existing `backlog-coverage.json` counts task assignments, not passing tests. A separate executable acceptance/evidence gate is required for each batch.

## Open workstreams
1. **Source provenance:** audit ID-by-ID V1/TZ/CASE and NEW-F001…NEW-F895; classify historical verbatim vs reconstructed semantics; reconcile checkpoint/certification status.
2. **Decision integration:** implement additive contracts for DR-V2-001…005 in data/runtime/engineering requirements and acceptance mappings; no unapproved numerical thresholds.
3. **Ten previously identified missing contracts:** C-10, C-12, C-14, C-19, C-20, C-21, C-22, C-23, C-24, C-26; distinguish technical decisions from missing source evidence.
4. **Quality gate:** requirement→contract→test→evidence mapping, actual automated and visual review, max five fix/retest cycles for bounded batches. Current prototype/CI screenshots do not establish V2 feature acceptance.

## Recommendation
Keep PR #1 as draft and main untouched. Do not start broad autonomous implementation. The next deliverable should be an additive `docs/v2/ENGINEERING-CONTRACT-GAPS.md` with testable schemas and unresolved numeric/profile questions, followed by a narrowly scoped pilot batch once source provenance is reconciled.
