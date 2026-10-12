# Canonical Decision Register

This register captures final architecture decisions that override stale or earlier wording.

| ID | Canonical decision |
|---|---|
| A-001 | Windows 10/11 x64 initial target. |
| A-002 | Electron + TypeScript; Constructor React; shared framework-independent TS domain/runtime packages. |
| A-003 | DOM/CSS/SVG base renderer; Canvas/WebGL/WebGPU only inside specialized Widgets. |
| A-004 | Constructor and Player are separate apps sharing Runtime Engine source. |
| A-005 | `.iss` working project; Collect makes portable editable project; Build makes Player artifact. |
| A-006 | Main owns OS/filesystem/network/windows; renderers own UI/runtime visuals; typed preload IPC. |
| A-007 | ProjectDocument canonical; Project Operations API; Editor UI and Runtime state separate. |
| A-008 | Hybrid normalized model with stable opaque IDs. |
| A-009 | Versioned project format and sequential forward migrations. |
| A-010 | Atomic save + separate crash-recovery snapshot. |
| A-011 | Unified validation engine; Errors block Build. |
| A-012 | Immutable runtime definition + transient RuntimeSession. |
| A-013 | Trigger → Behavior Flow → Action architecture; Delay and If control steps. |
| A-014 | Initial Action Registry covers navigation, popup, media, variables, animation/state, interaction, network, timeline and runtime. |
| A-015 | Runtime must tolerate rapid/repeated/chaotic input without global stability locks. |
| A-016 | Arrival-order event processing; no global busy queue; later state-set wins; Reset invalidates owned pending work. |
| A-017 | Page Enter/Active/Leave lifecycle; Page-owned work dies on Leave. |
| A-018 | Page-local, Screen Session and Shared Player state scopes. |
| A-019 | Exactly one system fullscreen Screen Media Player per Screen; ordinary Page media remains separate. |
| A-020 | Playlist is first-class ordered project entity, not filesystem folder. |
| A-021 | Page Timeline and Media Timeline are distinct. |
| A-022 | Popup is Page-owned runtime entity; reusable via Components. |
| A-023 | Screensaver is Screen-level visual/input overlay; does not Page Leave/Enter. |
| A-024 | Same-PC multi-display coordinated by logical Screen IDs and RuntimeCoordinator. |
| A-025 | TCP/UDP integrate through unified Trigger/Action architecture. |
| A-026 | Build is autonomous immutable runtime snapshot with dependency discovery and manifest. |
| A-027 | Preview is full Developer Runtime using same Runtime Engine and real TCP/UDP. |
| A-028 | Player display mapping/build selection are local deployment config; dynamic mapping apply; resilient missing display behavior. |
| A-029 | Multi-PC is installation-level Master/Client synchronized execution using prepare/readiness/shared future execution time where required. |
| A-030 | System Error/Fallback Visual exists; localized failures degrade locally. |
| A-031 | Components are versioned with controlled update propagation and preserved instance overrides. |
| A-032 | Widgets have a common contract but widget-specific customization and internal implementation. |
| A-033 | Simple On-Demand + Targeted Preload; no global predictive cache in initial V2. |
| A-034 | Fault isolation at content/widget, Screen renderer and whole-Player levels. |
| A-035 | Application updates are manual; Player local configuration survives reinstall. |
| A-036 | Architecture/compatibility audit closed; no separate Screenless mode. Audible Page background media + external Screen Media Player covers V1 use case. |
