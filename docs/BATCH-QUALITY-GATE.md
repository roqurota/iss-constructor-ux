# Constructor / Player V2 — Batch Development Protocol

Approved settings: **20% of the acceptance items in the currently agreed stage per batch**, with **at most 5 fix-and-retest cycles**. This is a target for planning, not a promise that a partially finished requirement counts as delivered. A batch is accepted only when all its selected acceptance items pass.

## Workflow

1. Freeze a batch manifest: stage, acceptance item IDs, expected behavior, test coverage, and explicit exclusions. The 20% denominator is the *agreed stage*, not the entire V2 specification. Do not silently change the denominator or count incomplete items.
2. Implement the selected behavior in a development branch. Keep the agreed V2 architecture and existing tests intact.
3. Run functional Playwright regression and UX heuristics. Capture desktop and laptop screenshots, browser errors, and machine-readable `test-artifacts/ux-gate.json`.
4. Review screenshots **visually** against the accepted UI baseline and usability criteria (consistency, clear feedback, discoverability, error prevention, keyboard interaction, legibility). The CI screenshot capture does **not** perform this review or certify WCAG compliance. Record concrete findings with screenshot references.
5. Fix findings and repeat steps 3–4. A *cycle* is one completed implement → test → inspect → fix/retest attempt; maximum **5**. Never claim PASS from an unobserved CI run.
6. If any mandatory gate fails after five cycles, stop and report blockers and evidence. Never weaken assertions, suppress browser errors, or remove failed checks just to get a green badge.
7. Present a batch to the product owner only after functional CI is confirmed successful, UX heuristics pass, and the screenshot review is recorded. Include item IDs, before/after images, test links, exceptions and residual risks.

## Current implementation

- GitHub Actions `.github/workflows/canvas-smoke.yml` runs the functional smoke test and the separate UX heuristic check; the final step fails if either check fails.
- The job summary reports both results. Artifacts include functional screenshots, failure HTML when available, screenshots at 1440×900 and 1280×800, and `ux-gate.json`.
- Heuristics cover JavaScript errors, page loading, horizontal document overflow, visible control names, and minimum control size. These are deliberately limited automated checks, **not** a full usability or accessibility audit.
- Visual baseline comparison, human-equivalent screenshot inspection, autonomous code editing, and automatic five-cycle orchestration are **not yet implemented**. A separate authorized executor with repository/browser access is required to perform those steps without chat-by-chat confirmation.

## Batch review record

For each batch, record:
- Stage and frozen acceptance IDs / total accepted stage IDs (percentage).
- Commit SHA and CI run URL with actual outcome.
- Functional assertions, UX heuristic findings, and visual screenshots inspected.
- Cycle count (1–5), fixes applied, unresolved defects.
- Gate decision: **PASS**, **FAIL**, or **UNVERIFIED**. Never use PASS if a required gate lacks evidence.

## UX Test 09 status

Multiple button actions, link selection, Undo, Save, Reset and related regressions are in the prototype. Their latest end-to-end CI result has not yet been verified. UX Test 09 remains **UNVERIFIED**, not complete.
