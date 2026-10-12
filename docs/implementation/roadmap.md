# Full Dependency-Aware Implementation Roadmap

Total planned implementation tasks: **60**.

## Wave 1
- **IMP-001** Monorepo and shared TypeScript foundations
- **IMP-002** Canonical Project Model types and IDs — depends on IMP-001
- **IMP-003** Project persistence, atomic save and migration — depends on IMP-002
- **IMP-004** Project Operations, copy/duplicate and history — depends on IMP-002
- **IMP-005** Validation Engine core — depends on IMP-002
- **IMP-006** Virtual Asset Library core — depends on IMP-002

## Wave 2
- **IMP-007** SVG structured import — depends on IMP-006, IMP-004
- **IMP-008** Constructor application shell and project lifecycle — depends on IMP-003, IMP-004, IMP-005
- **IMP-009** Designer Canvas viewport and grid — depends on IMP-008
- **IMP-010** Element editing tools — depends on IMP-009, IMP-004
- **IMP-011** Asset Library Constructor UI and relink — depends on IMP-006, IMP-008
- **IMP-012** Collect Project — depends on IMP-003, IMP-006
- **IMP-013** Action registry and Behavior Flow engine — depends on IMP-002

## Wave 3
- **IMP-014** Core Action handlers — depends on IMP-013
- **IMP-015** Screen/Page RuntimeSession lifecycle — depends on IMP-013, IMP-002
- **IMP-016** Runtime variables and interaction locks — depends on IMP-015, IMP-014
- **IMP-017** Base DOM/CSS/SVG runtime renderer — depends on IMP-015
- **IMP-018** Page navigation and visual transitions — depends on IMP-015, IMP-017, IMP-014
- **IMP-019** Popup runtime — depends on IMP-015, IMP-017, IMP-014
- **IMP-020** Page Timeline engine — depends on IMP-015, IMP-013
- **IMP-021** Screen persistent layer and scroll flow — depends on IMP-017, IMP-015

## Wave 4
- **IMP-022** Screen Media Player core — depends on IMP-015, IMP-017, IMP-014, IMP-006
- **IMP-023** Playlist engine — depends on IMP-022
- **IMP-024** Media Timeline and playback ranges — depends on IMP-022, IMP-013
- **IMP-025** Page background media with audio — depends on IMP-017, IMP-022
- **IMP-026** Playback controls and preserved input control — depends on IMP-022, IMP-014
- **IMP-027** Targeted media preparation and preload — depends on IMP-022, IMP-023
- **IMP-028** Component definitions, revisions and instances — depends on IMP-004, IMP-010
- **IMP-029** Widget registry and common runtime contract — depends on IMP-013, IMP-017, IMP-006

## Wave 5
- **IMP-030** Gallery Widget — depends on IMP-029
- **IMP-031** Image Viewer Widget — depends on IMP-029
- **IMP-032** Quiz Widget — depends on IMP-029, IMP-016
- **IMP-033** Form Widget — depends on IMP-029, IMP-016
- **IMP-034** Mini-game Widget framework — depends on IMP-029
- **IMP-035** Screensaver and idle engine — depends on IMP-015, IMP-022, IMP-019
- **IMP-036** Error/Fallback Visual and local degradation — depends on IMP-017, IMP-005
- **IMP-037** Runtime Compiler — depends on IMP-002, IMP-005, IMP-006, IMP-028, IMP-029
- **IMP-038** Build materialization, manifest and atomic publish — depends on IMP-037

## Wave 6
- **IMP-039** Constructor Preview runtime — depends on IMP-037, IMP-017, IMP-022
- **IMP-040** Preview physical display mode — depends on IMP-039
- **IMP-041** TCP/UDP Network Service — depends on IMP-013
- **IMP-042** Network diagnostics and manual send — depends on IMP-041
- **IMP-043** Player application shell and Build loading — depends on IMP-038, IMP-017, IMP-022
- **IMP-044** Physical display discovery and mapping — depends on IMP-043
- **IMP-045** Same-PC multi-display RuntimeCoordinator — depends on IMP-044, IMP-015

## Wave 7
- **IMP-046** Player Developer Mode and diagnostics — depends on IMP-043, IMP-042, IMP-044
- **IMP-047** Renderer fault recovery and watchdog integration — depends on IMP-043, IMP-044
- **IMP-048** Player local config persistence and reinstall survival — depends on IMP-043
- **IMP-049** Content Admin Mode — depends on IMP-008, IMP-011, IMP-028
- **IMP-050** Project visual system and project fonts — depends on IMP-006, IMP-010, IMP-017

## Wave 8
- **IMP-051** Multi-PC node connection, identity and clock sync — depends on IMP-041, IMP-043
- **IMP-052** Distributed PREPARE/READY/EXECUTE coordinator — depends on IMP-051, IMP-045, IMP-022
- **IMP-053** Multi-PC disconnect/reconnect fault tolerance — depends on IMP-052
- **IMP-054** Constructor Problems panel and validation UX — depends on IMP-005, IMP-008
- **IMP-055** Runtime/Build validation integration hardening — depends on IMP-038, IMP-029, IMP-028

## Wave 9
- **IMP-056** Kiosk startup and Windows deployment behavior — depends on IMP-043, IMP-047, IMP-048
- **IMP-057** V1 compatibility acceptance suite — depends on IMP-026, IMP-044, IMP-046, IMP-055
- **IMP-058** Reference CASE acceptance suite — depends on IMP-030, IMP-031, IMP-032, IMP-034, IMP-039
- **IMP-059** Original TZ acceptance suite — depends on IMP-049, IMP-050, IMP-056, IMP-055

## Wave 10
- **IMP-060** Soak, chaos and museum stability suite — depends on IMP-047, IMP-053, IMP-057, IMP-058, IMP-059

## Release gate
V2 is not release-ready until compatibility/acceptance/stability waves pass and all intentional Deferred items remain explicitly documented rather than silently omitted.
