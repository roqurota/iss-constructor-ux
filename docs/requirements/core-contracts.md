# Atomic Engineering Baseline

These are cross-cutting MUST/MUST NOT contracts extracted from the approved architecture. Domain files may add more specific requirements.

## Project and persistence
- **ENG-PROJ-001 MUST**: Treat `ProjectDocument` as the sole editable project source of truth.
- **ENG-PROJ-002 MUST NOT**: Persist Editor UI state or Runtime state into `ProjectDocument` unless a future explicit requirement adds such persistence.
- **ENG-PROJ-003 MUST**: Use stable opaque IDs for independently referenceable entities; display names are not identity.
- **ENG-PROJ-004 MUST**: Save `.iss` atomically using temporary output, validation and replacement.
- **ENG-PROJ-005 MUST**: Perform explicit sequential forward migrations; older apps MUST refuse unsupported newer formats safely.

## Runtime
- **ENG-RT-001 MUST**: Route project-visible events through Trigger → Behavior Flow → Action Engine.
- **ENG-RT-002 MUST**: Process accepted events in observed arrival order without a global busy lock.
- **ENG-RT-003 MUST**: A Delay pauses only its owning Behavior Flow.
- **ENG-RT-004 MUST**: Page Leave cancels Page-owned flows/delays/timelines/media/animations, closes Page popups and destroys Page-local state.
- **ENG-RT-005 MUST NOT**: Page Leave reset Screen or Shared Variables.
- **ENG-RT-006 MUST**: Ignore stale asynchronous completion from invalidated Page/media/runtime generations.
- **ENG-RT-007 MUST**: Reset Screen creates a clean initial Screen state and invalidates pending work owned by the previous Screen session.

## Media
- **ENG-MEDIA-001 MUST**: Provide exactly one system fullscreen Screen Media Player per Screen.
- **ENG-MEDIA-002 MUST**: Keep Page media Elements separate from the system Screen Media Player.
- **ENG-MEDIA-003 MUST**: Page background video/media support autoplay, loop, volume, mute/unmute and audible playback.
- **ENG-MEDIA-004 MUST NOT**: Implement a separate V2 Screenless runtime mode.
- **ENG-MEDIA-005 MUST**: A new Play Content request supersedes stale pending preparation for older requested content on the same Screen Media Player.
- **ENG-MEDIA-006 MUST**: Media Timeline follow actual media playback time and pause with media playback.

## Screens, displays and deployment
- **ENG-DISP-001 MUST**: Runtime behavior targets logical Screen IDs, never physical Display IDs.
- **ENG-DISP-002 MUST**: Store Screen→Display mapping in PlayerLocalConfig, not ProjectDocument or Build.
- **ENG-DISP-003 MUST**: Never silently remap a missing physical display.
- **ENG-DISP-004 MUST**: Failure/unavailability of one Screen output MUST NOT intentionally stop healthy Screens.

## Build
- **ENG-BUILD-001 MUST**: Player consumes Build only and MUST NOT open `.iss`.
- **ENG-BUILD-002 MUST**: Build operate from a ProjectDocument snapshot.
- **ENG-BUILD-003 MUST**: Full validation occur before publish; required used missing assets are Build Errors.
- **ENG-BUILD-004 MUST**: Package only runtime-required asset dependencies.
- **ENG-BUILD-005 MUST**: Publish Build atomically and preserve the previous valid Build on failure.
- **ENG-BUILD-006 MUST**: Generate runtime `project.json` and `manifest.json`; authoring source paths MUST NOT be runtime dependencies.

## Widgets and Components
- **ENG-WIDGET-001 MUST**: Every Widget declare stable `widgetType` and `widgetSchemaVersion`.
- **ENG-WIDGET-002 MUST**: Widget project-visible behavior integrate through registered Actions/Triggers.
- **ENG-WIDGET-003 MUST**: Widget asset dependencies be discoverable by Build.
- **ENG-WIDGET-004 MUST**: Dispose/cancel Widget-owned work on Page Leave.
- **ENG-WIDGET-005 MUST NOT**: Permit project-authored arbitrary executable JavaScript as Widget props.
- **ENG-COMP-001 MUST**: Component instances remain pinned to a revision until controlled update is applied.
- **ENG-COMP-002 MUST**: Instance overrides win by default during component update review.
- **ENG-COMP-003 MUST NOT**: Silently propagate component changes over existing instance overrides.

## Networking and synchronization
- **ENG-NET-001 MUST**: Treat incoming TCP/UDP as Trigger sources and outgoing messages as Actions.
- **ENG-NET-002 MUST**: Unknown/unmatched network input fail safely and be diagnosable.
- **ENG-SYNC-001 MUST**: Treat Multi-PC topology as deployment-local installation configuration.
- **ENG-SYNC-002 MUST NOT**: Add a per-Action `synchronized` authoring checkbox as the synchronization model.
- **ENG-SYNC-003 MUST**: Synchronized distributed operations support preparation/readiness and a common future execution time when preparation/timing is required.
- **ENG-SYNC-004 MUST**: A disconnected Client after installation startup MUST NOT freeze unrelated healthy nodes indefinitely.
