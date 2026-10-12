# AGENTS.md — ISS Constructor V2

## Mission
Implement ISS Constructor V2 from the repository contracts. The documentation is optimized for coding, review and test agents. Do not reinterpret product intent from memory or invent parallel architecture.

## Authority order
1. `docs/requirements/` atomic requirements and invariants.
2. `docs/architecture/` canonical engineering contracts.
3. `docs/verification/` acceptance and traceability rules.
4. `docs/source/` lossless snapshots of approved source specifications.
5. Implementation code.

When two sources conflict, a later explicit architecture reconciliation listed in `docs/architecture/decision-register.md` overrides older prose. Never silently resolve a conflict by changing observable product behavior.

## Agent workflow
1. Identify requirement IDs for the task.
2. Read only the linked architecture/source context plus dependencies.
3. Implement the smallest coherent change.
4. Add/update tests for every MUST behavior touched.
5. Run validation/tests.
6. Report requirement IDs implemented, files changed, tests run, and any unresolved gap.
7. Do not refactor unrelated architecture merely for convenience.

## Product Owner escalation policy
Do NOT escalate implementation details, naming, class/module boundaries, algorithms, internal data representation, ordinary error handling, test implementation, or performance optimization that preserves specified semantics.

Escalate only when ALL are true:
1. Existing requirements/decisions do not determine observable behavior.
2. Two or more reasonable behaviors exist.
3. The choice materially changes UX, V1 compatibility, deployment workflow, project capability, or operator behavior.

Before escalation:
- search requirements, architecture, decision register and source snapshots;
- derive from existing invariants where possible;
- minimize the decision surface;
- present options and one recommended default;
- explain the observable consequence only.

Use this format:
`PRODUCT GAP: <ID/topic> / Existing contracts: ... / Undefined behavior: ... / Options: A,B / Recommended: ... / Why PO decision is required: ...`

## Hard architectural rules
- ProjectDocument is the only editable authoring source of truth.
- Runtime state never writes back into ProjectDocument.
- Player consumes Build (`project.json` + packaged assets), never `.iss`.
- Preview and Player share Runtime Engine semantics.
- Runtime Actions target logical Screens, never physical Displays.
- Display mapping and Multi-PC topology are deployment-local.
- All project-visible inputs use Trigger → Behavior Flow → Action Engine.
- Exactly one system fullscreen Screen Media Player exists per Screen.
- Page-owned work is invalidated on Page Leave.
- Screensaver visibility does not cause Page Leave/Enter.
- No separate Screenless Mode exists in V2.
- Page background video/media supports audio; this covers the V1 Screenless use case.
- Component updates are versioned and controlled; never silently propagate over instance overrides.
- Widgets obey the Widget Contract; do not create a parallel subsystem.
- Build is snapshot-based, validated and atomically published.
- Multi-PC synchronization is installation/runtime coordination, not a per-Action checkbox.
- A missing/unavailable target must fail safely and must not crash unrelated Screens.

## Change control
If implementation reveals an architecture gap, stop only the affected decision. Do not block unrelated work. Never convert an engineering uncertainty into a Product Owner question unless the escalation policy is satisfied.

## Traceability certification gate
Read `docs/verification/traceability-state.json` before claiming historical coverage is fully reconstructed.
If `traceability_complete` is false, do not invent source wording or dispositions to make the audit look complete.
A missing historical source text is a documentation-recovery issue, not automatically a Product Owner escalation.

## Semantic traceability certification
`docs/verification/traceability-state.json` distinguishes engineering semantic completeness from archival verbatim recovery.
The 354 V1/TZ/CASE source IDs are semantically covered. Reconstructed TZ labels are engineering provenance, not verbatim quotations.
Do not reopen Product Owner decisions merely because archival wording is unavailable.

## Implementation task execution
Use `docs/implementation/task-protocol.md`. Prefer bounded `IMP-*` task packets over loading the full corpus. A coding task is complete only when its ENG contracts and linked TEST contracts are satisfied.

## Full backlog
Use `docs/implementation/backlog.json` and `orchestration-guide.md` for task selection. Never start an IMP task before its preflight gate and dependencies are satisfied.
