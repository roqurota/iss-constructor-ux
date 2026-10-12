# IMP-001 — Architecture-to-test binding and execution handoff

**2026-10-12 | Status: READY FOR LOCAL PREFLIGHT ONLY; NOT AUTHORIZED TO CODE.**

This supplements `IMP-001-PREFLIGHT-ACCEPTANCE.md`. Existing `docs/verification/requirements.json` contains ENG behavior requirements, but no verified atomic ENG records for all IMP-001 repository/process architecture obligations. **Do not invent ENG IDs or claim this file closes that gap.** Existing `AC-ARCH-01` and `AC-ARCH-04` are authoritative architecture acceptance IDs, not ENG IDs.

## Existing authoritative anchors
- System Architecture §§1–3: independent Constructor/Player Electron apps, common framework-independent Runtime Engine, domain packages independent of React/Constructor UI, narrow typed preload/IPC, `nodeIntegration=false`, `contextIsolation=true`.
- AC-ARCH-01: independent Constructor/Player compilation/deployment consuming one Runtime Engine source.
- AC-ARCH-04: Preview/Player runtime semantic equivalence (**future integration gate**, not provable from scaffolding).
- Existing ENG-PREV-001 and ENG-CONSTR-024: shared runtime semantics (**future integration gate**, not IMP-001 completion).
- `docs/implementation/tasks/IMP-001.md`: architecture-only task, requires atomizing MUSTs and assigning TEST IDs before coding.

## Proposed atomic architecture contract candidates — require registry reconciliation

| Provisional local ID | Architecture obligation | Task acceptance item | Proposed test ID (NOT yet canonical) | Verification |
| --- | --- | --- | --- | --- |
| ARCH-CAND-001 | independent apps in workspace | PREF-002,003 | TEST-IMP001-001 | clean install; independent app typecheck/build |
| ARCH-CAND-002 | shared packages with no React/Constructor UI dependencies | PREF-004,005 | TEST-IMP001-002 | forbidden-import negative fixture |
| ARCH-CAND-003 | one framework-independent Runtime Engine package | PREF-004,007 | TEST-IMP001-003 | dependency graph + same package import from both apps |
| ARCH-CAND-004 | Electron renderer isolation defaults | PREF-005,006 | TEST-IMP001-004 | inspect BrowserWindow construction, check both defaults |
| ARCH-CAND-005 | privileged APIs only through narrow typed preload/contextBridge | PREF-005,006 | TEST-IMP001-005 | static import/security boundary tests |
| ARCH-CAND-006 | prototype and existing CI/test behavior preserved | PREF-001,009 | TEST-IMP001-006 | diff + legacy Playwright suite and UX gate |
| ARCH-CAND-007 | deterministic tooling and explicit validation | PREF-002,008,010 | TEST-IMP001-007 | clean lockfile install/typecheck/build/lint/test and logs |

All candidate IDs are **proposal-only**. Canonical ENG and TEST IDs must be allocated using the existing registry's naming and deduplication policy after reviewing complete requirements/tests and exact repo tree.

## Local preflight required from Codex (READ-ONLY)
1. Inspect `git status --porcelain=v1`, current branch, `git remote -v`, existing files, CI, all `AGENTS.md` guidance. Do not modify anything.
2. Check whether `docs/v2-source-of-truth-20261012` remote branch exists and inspect the draft docs. Do not switch the user's current branch.
3. Determine exact workspace/package tooling already present on local branch (may differ from `main`).
4. Check for collisions with planned `apps/`, `packages/`, root package manifests and any uncommitted files.
5. Inspect canonical `docs/verification/requirements.json`, test registry and task protocol; recommend exact ENG/TEST IDs without writing them.
6. Output one concise report: `LOCAL_PREFLIGHT`, safe/unsafe paths, existing relevant files, candidate-to-existing ID mapping, executable commands, blockers.
7. Stop. No code changes, git commits, branch checkout, package installs or tests requiring file writes during this read-only pass.

## Next gate
After local preflight, review the proposed ID allocation and acceptance test manifest. Only then authorize isolated implementation worktree and at most five fix/retest cycles. Do not assume historical CI is green or visual evidence reviewed.
