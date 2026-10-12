# ISS V2 source-of-truth migration status

Status: **IN PROGRESS — not yet ready for autonomous feature implementation**.

## Verified in recovered engineering archive
Archive: ISS_AI_Engineering_Source_of_Truth_FULL_BACKLOG.zip (108 files with 108 matching SHA-256 manifest records, inspected 2026-10-12).
- Source specifications: Product, Architecture, Runtime State Model, Widget Contract, Project Data Model, original TZ.
- Requirements, architecture decision register, verification and implementation documents.
- Archive's self-reported traceability: V1 178/178, TZ 128/128, CASE 48/48 = 354/354 semantically mapped. Historical verbatim TZ atomization NOT recovered; reconstructed labels must not be represented as verbatim.
- Archive's self-reported backlog: 60 tasks / 10 waves, 298 atomic ENG requirements, 295 mandatory, 295 mapped to backlog tasks.
- These figures are document assertions and integrity checks, NOT proof that application features are implemented or tested.
- NEW-F001…NEW-F895 full historical decision register has NOT been independently verified.

## Published decision overlay
See `docs/v2/decisions/APPROVED-DECISIONS-2026-10-12.md`. Later approved product decisions take precedence over conflicting older wording; source documents remain traceable.

## Remaining steps
1. Import recovered archive source/requirements/verification/backlog content into repository in a controlled branch, preserving paths and manifest.
2. Reconcile historical and newer decisions, especially NEW registry, and validate requirement→decision→test mappings.
3. Draft and review technical contracts for ten MISSING CONTRACT issues and the five newly approved choices; C-25 numeric operational thresholds require product-owner approval.
4. Add repository-root AGENTS.md with binding source precedence, branch safety, no invented requirements, test evidence and max five fix/retest cycles.
5. Only then authorize bounded implementation batches. Local uncommitted work must be preserved.

Do not treat this status document as a replacement for the actual source archive.
