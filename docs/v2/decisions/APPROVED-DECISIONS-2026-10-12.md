# ISS Constructor / Player V2 — approved product decisions

Approval: product owner, 2026-10-12. These records resolve C-04, C-06, C-07, C-11, C-25 from the documentation audit. Approval does NOT mean implementation or testing has passed. Preserve earlier requirement IDs and A-001…A-036 architecture.

## DR-V2-001 / C-04 — Timeline
APPROVED: keep Once per Visitor Session event policy and restoration of Completed Visual State on Page re-entry without replaying side-effect actions. Keep Architecture A-017/A-021 Page lifecycle: Page runtime is fresh on re-entry; Page-owned flows are cancelled on leave. Technical contract TBD: visitor-session lifetime/reset, precedence of repeat policies, visual snapshot ownership and side-effect suppression. Sources: PS-TIME-003/005/006, Architecture §§10,13. Acceptance: test repeat policies, re-entry, visitor-session boundary, visual restoration without duplicated side effects.

## DR-V2-002 / C-06 — Screen Media Content position
APPROVED: preserve playback position separately per displaced Content. Retain exactly one system fullscreen Screen Media Player per logical Screen; new Content replaces current Content, no second player and no implied automatic resume. Technical contract TBD: content identity, position retention/reset, seekability, end-of-content, explicit resume semantics. Sources: PS-MEDIA-011, Architecture §12.2/A-019. Acceptance: A→B→A resumes A at saved position only when explicitly requested, no second system player.

## DR-V2-003 / C-07 — Always Preload
APPROVED: retain author-configured Always Preload for selected assets as explicit opt-in within targeted preparation. Do not introduce global predictive HOT/WARM/COLD caching, mandatory eager preload of all used assets or LRU manager. Technical contract TBD: scope/timing, failure and readiness, priority and memory guardrails. Sources: PS-PRE-004, Architecture §20/A-033. Acceptance: selected assets follow explicit preparation; unselected assets are not indiscriminately preloaded.

## DR-V2-004 / C-11 — Developer Mode
APPROVED: mandatory physical-key Ctrl+Shift+D independent of keyboard layout, PLUS a separately configurable technician hotkey. Config cannot disable/replace the mandatory chord. Technical contract TBD: storage/scope, shortcut collisions, security/access. Sources: PS-DIAG-001, Architecture §25.2/A-028. Acceptance: both shortcuts work, mandatory shortcut survives changes, physical-key behavior verified.

## DR-V2-005 / C-25 — Baseline hardware
APPROVED IN PRINCIPLE: one baseline installation hardware profile for initial V2 acceptance. NO numerical hardware specification, soak duration, response-time limit, memory-growth threshold, visual/touch metric or pass/fail threshold has been approved. Technical/acceptance criteria are BLOCKED until explicitly agreed. Sources: PS-PRE-007/008, original TZ §15, Architecture §1, Widget Contract §27.

## Change control
These five product choices are approved. Their technical contracts and tests are NOT automatically approved. The other 11 RESOLVED and 10 MISSING CONTRACT audit findings remain unchanged. Never claim CI/Playwright/visual PASS without observed evidence. No silent deletion of V1/TZ/CASE requirements or reactivation of superseded NEW decisions.
