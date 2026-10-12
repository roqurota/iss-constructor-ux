# ISS Constructor V2 — AI Engineering Source of Truth v1

This package is the repository-oriented engineering context for AI coding/review/test agents.

Start with `AGENTS.md`.

## Why this exists
The approved product and architecture work was originally captured in human-readable DOCX specifications. Those documents remain preserved as source snapshots under `docs/source/`. This package adds a concise canonical layer optimized for agents: authority rules, final architecture decisions, atomic MUST/MUST NOT contracts, traceability policy and verification rules.

## Important
This is a consolidation layer, not a product redesign. Where older prose conflicts with later approved architecture, the decision register states the canonical outcome.

## Next formalization work
Atomic requirement coverage will be expanded domain-by-domain (Build, networking/sync, media, Constructor, Player, widgets, validation) without requiring Product Owner review unless the escalation policy in `AGENTS.md` is triggered.

## v1 expanded formalization
This package now contains 196 machine-extracted ENG requirements and 194 planned verification rows in `docs/verification/requirements.json` and `acceptance-matrix.csv`.

## Traceability certification
354/354 V1/TZ/CASE capability IDs are now semantically represented and mapped. See `docs/verification/traceability-certification.md` for the distinction between engineering completeness and archival verbatim recovery.
