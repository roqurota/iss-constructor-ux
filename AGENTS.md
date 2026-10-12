# AGENTS.md — ISS Constructor / Player V2 (migration-stage guardrails)

## Current state
The repository's V2 source-of-truth migration is IN PROGRESS. Read `docs/v2/SOURCE-OF-TRUTH-STATUS.md` first. The full historical engineering archive has been located and integrity-checked, but has not yet been fully imported into this Git branch. Do not assume missing files are absent from the project history.

## Approved product decisions
Read `docs/v2/decisions/APPROVED-DECISIONS-2026-10-12.md` before any relevant implementation. DR-V2-001…005 are approved at product-behavior level, not implemented or tested. C-25 numerical performance thresholds are NOT approved.

## Non-negotiable safety and verification
- Do not invent missing source requirements, old IDs, technical thresholds, or approvals.
- Do not erase uncommitted user work, reset hard, clean untracked files, or push directly to main.
- Treat existing HTML prototype as UX prototype, not proof of completed V2 architecture.
- Each implementation batch must identify exact requirement IDs, expected results, automated tests and visual evidence.
- Run tests and inspect results; screenshots merely saved to disk are NOT visually reviewed.
- Do not disable failing tests or weaken gates to manufacture PASS.
- Maximum five automated fix-and-retest cycles per bounded batch; stop with diagnostic report if still failing.
- No autonomous feature batches until source registry, traceability, contracts and acceptance manifest are reconciled.

## Intended canonical authority after full import
Later explicitly approved product decisions > reconciled atomic requirements / engineering contracts > architecture decisions > source specifications > implementation. Preserve superseded requirements for provenance, never silently reactivate them. Resolve material product-visible ambiguities with product-owner approval.
