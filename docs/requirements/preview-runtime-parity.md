# Preview and Runtime Parity
- **ENG-PREV-001 MUST**: Constructor Preview use the same Runtime Engine source/packages as Player.
- **ENG-PREV-002 MUST**: Preview compile a project snapshot through Runtime Compiler semantics before starting RuntimeSession.
- **ENG-PREV-003 MUST**: Preview execute real Actions, media, timelines, Widgets and TCP/UDP semantics.
- **ENG-PREV-004 MUST**: All Screens Simulator create real logical ScreenRuntimeSessions rendered scaled for inspection; scaling MUST NOT change logical project resolution.
- **ENG-PREV-005 MUST**: Physical Displays preview use explicit local mapping and MUST NOT write deployment mapping into ProjectDocument.
- **ENG-PREV-006 MUST**: Developer overlay be outside project visual coordinate system.
- **ENG-PREV-007 MUST**: ESC may exit Developer Preview but production Player MUST NOT inherit this as default kiosk exit.
- **ENG-PREV-008 MUST**: Preview restart from a new snapshot rather than live-mutating active Runtime definition.
