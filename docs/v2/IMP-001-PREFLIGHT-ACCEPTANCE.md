# IMP-001 — Preflight and acceptance manifest (draft, 2026-10-12)

**Task:** IMP-001 Monorepo and shared TypeScript foundations (Wave 1, no dependencies).  
**Status:** PREFLIGHT SPECIFIED; **NOT IMPLEMENTED / NOT TESTED**.  
**Authority:** `docs/implementation/tasks/IMP-001.md`, System Architecture §§1–3 and `docs/implementation/task-protocol.md`. This is a task-level acceptance supplement, not a new product requirement.

## Verified current-repo baseline
- `main` currently has `index.html` (single-file Russian-language UX prototype; HTML title "ISS Constructor — UX Test 08"), Python Playwright tests under `tests/`, `.github/workflows/canvas-smoke.yml`, and `quality-gate.json`.
- No root `package.json` exists on `main`; no evidence of an existing TypeScript workspace was found at that canonical path. This does **not** prove absence of all TypeScript code at other paths or on uncommitted local branches.
- The UX gate saves screenshots but explicitly reports `human_visual_review: not performed`; CI only enforces functional Playwright and UX heuristics, not human/agent visual review.
- Historical `docs/implementation/backlog.json` lists IMP-001 with 0 requirement and 0 linked-test counts; the task file explicitly requires architecture MUST atomization before coding.

## Acceptance items (new *provisional task-local* IDs; NOT source ENG/TEST registry IDs)
- **PREF-001:** Establish baseline file inventory and compare branch vs main; preserve prototype and existing test workflows. Confirm local uncommitted state before editing.
- **PREF-002:** Create workspace root with package-manager/workspace definition and TypeScript compiler configuration. Pin tool versions; document exact install/build/test commands.
- **PREF-003:** Establish `apps/constructor` and `apps/player` package boundaries for independently buildable Electron apps, without claiming feature behavior.
- **PREF-004:** Establish `packages/project-model`, `runtime-engine`, `actions`, `media`, `widgets`, `network`, `build`, `validation`, `shared` (or documented compatible equivalent), with one explicit dependency-direction rule.
- **PREF-005:** Domain/runtime packages must not import React, Constructor UI or Electron privileged APIs. Privileged OS/FS/network calls belong to Main/background services and typed narrow preload/contextBridge surfaces.
- **PREF-006:** Renderer Electron defaults must explicitly set `nodeIntegration:false`, `contextIsolation:true` in both apps. No remote/untrusted content execution added as part of scaffold.
- **PREF-007:** Constructor and Player share a single framework-independent Runtime Engine package rather than copying implementations.
- **PREF-008:** Add deterministic static boundary checks and workspace build/typecheck/smoke checks. Record commands, logs and exit status. Do not report PASS before execution.
- **PREF-009:** Preserve legacy `index.html`, `tests/`, quality-gate policy and existing CI semantics. If CI needs additive jobs, keep legacy checks runnable and don't weaken gates.
- **PREF-010:** Document architecture deviations and remaining blockers; produce a completion report with changed files, evidence and explicit NOT VERIFIED where applicable.

## Preconditions before authorizing coding
1. Convert architecture MUSTs relevant to IMP-001 into stable atomic ENG IDs and linked TEST IDs in canonical registries. Do not fabricate V1/TZ/CASE/NEW IDs. Task-local PREF IDs alone do not satisfy the source traceability policy.
2. Review the exact existing repo tree and local worktree state to avoid collisions with uncommitted changes. Use a separate implementation branch/worktree.
3. Freeze task scope: scaffolding only. No Project Model semantics (IMP-002), Runtime state machines, media, timeline, UI redesign, Player deployment, or migration of legacy prototype.
4. Choose and document package manager/build/test tool versions through an engineering decision, based on repo/tool compatibility; no product-owner approval needed unless user-visible behavior changes.
5. Define test fixtures and commands for each accepted architecture invariant. CI green for legacy prototype alone is not IMP-001 PASS.

## Candidate evidence checklist (must be executed)
- Clean package install and deterministic dependency lockfile resolution.
- Workspace typecheck/build for both apps and shared packages.
- Automated dependency-boundary rule failure fixture (intentional forbidden import is rejected).
- Electron process configuration static/runtime verification.
- Existing Python Playwright functional and UX tests run and retain their behavior.
- No changes to user local uncommitted files.
- Review agent independent verdict `PASS|PASS_WITH_NOTES|FAIL` plus concrete evidence.
- Visual review required only if user-facing UI is changed; IMP-001 should not change UI.

## Gate outcome
**NOT READY TO CODE** until ENG/TEST IDs and existing-tree/local-state review are complete. This file is a precise bounded implementation acceptance plan, not an instruction to launch agents.
