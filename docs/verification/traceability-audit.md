# Traceability and Lossless Consolidation Audit

## Source families that remain authoritative evidence
| Family | Count / range | Consolidation rule |
|---|---:|---|
| V1 reverse-engineered features | V1-F001..V1-F178 (178) | Every confirmed V1 capability remains a compatibility obligation unless explicitly Revised/Superseded. |
| Original technical specification | TZ-F001..TZ-F128 (128) | Preserved as source; revised items retain explicit disposition rather than disappearing. |
| Figma/reference application capabilities | CASE-F001..CASE-F048 (48) | Acceptance principle: referenced ISS patterns must be buildable without custom application code. |
| Historical product decisions | NEW-F001..NEW-F895 | Historical decision stream; superseded/revised decisions remain provenance, while final behavior is represented by canonical architecture/product contracts. |
| Architecture decisions | A-001..A-036 | Final architecture baseline; later reconciliations override stale prose. |

## Important explicit reconciliations
- V1-F130 Screenless Mode → **Revised/Covered**: no separate V2 mode. Normal Page background media can play audio; TCP/UDP can launch the Screen Media Player; exiting content reveals the underlying Page.
- V1 Screen→Display project persistence → **Revised**: deployment mapping lives in PlayerLocalConfig.
- V1 filesystem folder-as-sequence → **Revised/Covered** by first-class Playlist + quick folder import.
- V1 preloading F166..F172 → **Revised/Covered** by system essentials + on-demand/targeted media preparation; no global predictive cache required.
- Full multiple-theme switching from TZ → **Deferred/Partial**: live color variables/defaults/fonts/components/SVG remain active.
- Content Admin structural creation → **Deferred**; initial Admin mode edits exposed content/properties without arbitrary structure mutation.
- Admin update-without-build → **Revised**: deployed Player changes require a new Build/deployment.
- Dedicated iRidi adapter → **Revised**: generic TCP/UDP first; dedicated adapter deferred.
- Transparent cross-PC Shared Variables → **Not required / superseded**; Shared Variables are automatic only inside one Player.
- Components → **Revised** to versioned controlled propagation.
- Preload Manager wording in older Product Spec → **Superseded** by A-033.
- Older multi-PC wording limited to playback/screensaver → **Superseded/broadened** by A-029 distributed synchronized execution.
- Older multiple-designed Screen Media Players concept → **Superseded** by exactly one system Screen Media Player per Screen.

## Losslessness rule for future edits
No source requirement ID may disappear from provenance. A future traceability matrix must assign each source ID one of:
`Active | Covered | Revised | Superseded | Deferred | Explicitly Not Required`.

`Unknown` or a missing row is a release-blocking documentation defect.

## Current audit status
The previous product/architecture audit established:
- V1: 178/178 accounted; lost 0.
- TZ: 128/128 accounted with explicit revised/deferred areas.
- CASE: 48/48 accounted/buildable.
- Historical NEW decisions: 895/895 accounted in the prior decision audit.
- Architecture blockers: 0.
- Unresolved product decisions before engineering formalization: 0.

This v1 repository package preserves the approved source specifications as lossless text snapshots and adds canonical final-decision overlays. It does not delete the source documents or pretend that historical superseded requirements are active implementation requirements.
