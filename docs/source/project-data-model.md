# ISS CONSTRUCTOR V2\n\nProject Data Model / JSON Schema\n\nCanonical authoring model, runtime compilation boundaries, IDs, references, migrations and serialization\n\nStatus: Engineering baseline after Architecture A-001–A-036
Target: Windows 10/11 x64 • Electron + TypeScript • Constructor + Player + shared Runtime Engine\n\n### 1. Purpose and authority\n\nThis specification defines the canonical persistent data model for ISS Constructor V2. It translates the approved Product Specification and System Architecture decisions into stable entities, ownership rules, references, serialization contracts and Player-facing compilation boundaries.\n\n- The Working Project (.iss) is the canonical editable source model.\n\n- The Player never consumes .iss directly; Build compiles a reduced runtime model into project.json plus packaged assets and manifest.json.\n\n- ProjectDocument is the sole canonical authoring state. UI stores, selection state, open panels, zoom and runtime state are not serialized into the project unless explicitly listed here.\n\n- Independent/referenceable entities receive stable IDs. Owned value objects remain nested.\n\n- Names are human-readable labels and are never identity.\n\n- All schema evolution is forward-migrated through explicit sequential migrations.\n\n- No confirmed V1 behavior is removed merely because the V2 representation differs.\n\n### 2. Model layers\n\n### 3. Identity, references and ownership\n\n### 3.1 Stable IDs\n\nAll independently addressable entities use opaque stable string IDs. UUIDv7/ULID-style generation is recommended; the exact generator is an implementation detail.\n\ntype EntityId = string;
// Examples: "scr_01J...", "page_01J...", "asset_01J...", "cmp_01J..."\n\n- IDs never depend on display names, filesystem paths, array position or Screen resolution.\n\n- Rename preserves ID.\n\n- Move/reorder preserves ID.\n\n- Duplicate/import creates new IDs and remaps references internal to the duplicated/imported graph.\n\n- References outside the duplicated graph remain references to their original targets unless the operation explicitly clones those dependencies.\n\n### 3.2 Entity versus value object rule\n\n### 4. Root ProjectDocument\n\ninterface ProjectDocument {
  formatVersion: number;
  projectId: ProjectId;
  name: string;
  createdAt: string;
  modifiedAt: string;

  settings: ProjectSettings;
  screens: Record<ScreenId, ScreenDefinition>;
  screenOrder: ScreenId[];

  assets: Record<AssetId, AssetRecord>;
  assetFolders: Record<AssetFolderId, AssetFolder>;
  assetRootOrder: AssetNodeRef[];

  playlists: Record<PlaylistId, PlaylistDefinition>;
  variables: Record<VariableId, VariableDefinition>;
  components: Record<ComponentId, ComponentDefinition>;
  projectFonts: Record<ProjectFontId, ProjectFontDefinition>;

  network: NetworkAuthoringConfig;
  templates?: ProjectTemplateMetadata;
  admin: ContentAdminDefinition;
  metadata: AuthoringMetadata;
}\n\nRegistries are normalized maps keyed by stable ID. Separate order arrays are used where presentation/order is meaningful. Runtime compilation may transform this representation.\n\n### 5. ProjectSettings\n\ninterface ProjectSettings {
  defaultTypography: TypographyDefaults;
  defaultElementStyles: ElementStyleDefaults;
  colorVariables: Record<ColorVariableId, ColorVariable>;
  initialScreenIds?: ScreenId[];
  buildSettings: BuildSettings;
}\n\nOrientation is not stored as a separate project concept. Screen width and height define designed orientation/aspect ratio.\n\n### 6. ScreenDefinition\n\ninterface ScreenDefinition {
  id: ScreenId;
  name: string;
  width: number;
  height: number;

  pageIds: PageId[];
  pages: Record<PageId, PageDefinition>;
  initialPageId: PageId;

  persistentLayer: PersistentLayerDefinition;
  screensaver: ScreensaverDefinition;
  errorVisual: ErrorVisualDefinition;

  screenVariables?: VariableId[];
  screenMediaPlayer: ScreenMediaPlayerDefinition;
  inputBindings: InputBindingDefinition[];
  runtimeSettings: ScreenRuntimeSettings;
}\n\n- A Screen is a logical runtime context, not a physical monitor.\n\n- Screen→Display mapping is deliberately absent from ProjectDocument and lives in PlayerLocalConfig.\n\n- Every V2 Screen uses the normal Page model. There is no separate Screenless runtime mode.\n\n- The V1 Screenless scenario is covered by a normal Page whose background media may autoplay/loop with audio, while external triggers launch Screen Media Player content.\n\n### 7. PageDefinition and flow\n\ninterface PageDefinition {
  id: PageId;
  name: string;
  flowMode: "navigation" | "scroll";
  rootElementIds: ElementId[];
  elements: Record<ElementId, ElementDefinition>;

  background: PageBackgroundDefinition;
  popupIds: PopupId[];
  popups: Record<PopupId, PopupDefinition>;

  timeline?: PageTimelineDefinition;
  idle: PageIdleDefinition;
  enterBehavior?: BehaviorFlow;
  leaveBehavior?: BehaviorFlow;
  persistentLayerVisibility?: Record<ElementId, boolean>;
}\n\nPage pixel dimensions are inherited from its Screen and are not independently resizable. Long content is represented by Scrollable Containers or scroll-composed Pages, not by changing Page runtime dimensions.\n\n### 7.1 Page background media\n\ninterface PageBackgroundDefinition {
  kind: "color" | "image" | "video" | "playlist";
  color?: ColorValue;
  assetId?: AssetId;
  playlistId?: PlaylistId;
  fit?: MediaFit;
  autoplay?: boolean;
  loop?: boolean;
  muted?: boolean;
  volume?: number; // 0..1
}\n\nBackground video/media explicitly supports sound. This is a normative V2 capability and is part of the V1 Screenless compatibility replacement.\n\n### 8. Elements and Containers\n\ntype ElementDefinition =
  | TextElement
  | ImageElement
  | ButtonElement
  | VideoElement
  | ContainerElement
  | WidgetElement
  | ComponentInstanceElement
  | ShapeElement;

interface ElementBase {
  id: ElementId;
  type: string;
  name: string;
  parentId?: ElementId;
  transform: Transform2D;
  visible: boolean;
  locked?: boolean;
  opacity: number;
  zIndex: number;
  style?: ElementStyle;
  behaviors?: ElementBehaviorBindings;
}\n\ninterface Transform2D {
  x: number;
  y: number;
  width: number;
  height: number;
  rotation?: number;
  scaleX?: number;
  scaleY?: number;
}\n\nContainers own child ordering through childIds. Parent/child references must be internally consistent and validated; cycles are invalid.\n\n### 9. Widgets\n\ninterface WidgetElement extends ElementBase {
  type: "widget";
  widgetType: string;
  widgetSchemaVersion: number;
  props: Record<string, JsonValue>;
  stateDefaults?: Record<string, JsonValue>;
}\n\nWidget props are validated by the registered Widget Contract for widgetType. Widgets expose their own relevant property set, actions and triggers; internal implementation details do not have to appear as ordinary project Elements.\n\n### 10. Components and revisions\n\ninterface ComponentDefinition {
  id: ComponentId;
  name: string;
  currentRevisionId: ComponentRevisionId;
  revisions: Record<ComponentRevisionId, ComponentRevision>;
}

interface ComponentRevision {
  id: ComponentRevisionId;
  revisionNumber: number;
  rootElementIds: ElementId[];
  elements: Record<ElementId, ElementDefinition>;
  exposedProperties: ExposedComponentProperty[];
  createdAt: string;
}

interface ComponentInstanceElement extends ElementBase {
  type: "componentInstance";
  componentId: ComponentId;
  revisionId: ComponentRevisionId;
  overrides: Record<string, JsonValue>;
}\n\n- Saving a changed Component Definition creates a new revision.\n\n- Existing instances remain pinned to their recorded revision until Review & Apply Updates.\n\n- Instance overrides win by default and are never silently overwritten.\n\n- Detach materializes the instance as ordinary local Elements with newly remapped IDs.\n\n- Nested Components are allowed, subject to cycle validation.\n\n### 11. Assets and virtual folders\n\ninterface AssetRecord {
  id: AssetId;
  name: string;
  kind: "image" | "video" | "audio" | "font" | "svg" | "animation" | "other";
  sourcePath: string;
  virtualFolderId?: AssetFolderId;
  metadata: AssetMetadata;
  missing?: boolean;
}

interface AssetFolder {
  id: AssetFolderId;
  name: string;
  parentId?: AssetFolderId;
  childFolderIds: AssetFolderId[];
  assetIds: AssetId[];
}\n\n- Virtual folder operations do not move source files.\n\n- Element/media references use assetId, never sourcePath.\n\n- Missing source files preserve AssetRecord and references so the asset can be relinked.\n\n- Collect Project copies every registered asset and rewrites source paths to portable relative paths.\n\n- Build copies only runtime-required dependencies plus required fonts/system resources.\n\n### 12. Playlists / Content Sequences\n\ninterface PlaylistDefinition {
  id: PlaylistId;
  name: string;
  items: PlaylistItem[];
  loop: boolean;
}

interface PlaylistItem {
  id: PlaylistItemId;
  assetId: AssetId;
  imageDurationMs?: number;
  videoRange?: { startMs?: number; endMs?: number };
  volume?: number;
  muted?: boolean;
  playbackRate?: number;
  fit?: MediaFit;
  transition?: MediaTransitionDefinition;
  mediaTimeline?: MediaTimelineDefinition;
}\n\nA physical filesystem folder is not a Playlist. Import Folder as Playlist is a convenience operation that creates an independent ordered Playlist referencing assets.\n\n### 13. Screen Media Player\n\ninterface ScreenMediaPlayerDefinition {
  enterTransition?: MediaTransitionDefinition;
  exitTransition?: MediaTransitionDefinition;
  playbackControls: PlaybackControlsDefinition;
  defaultVolume?: number;
  defaultMuted?: boolean;
}\n\nThere is exactly one system fullscreen Screen Media Player per Screen. It is Screen-owned and can play a single Asset or Playlist. Ordinary Page video/audio Elements remain separate Page-owned media.\n\n### 14. Variables\n\ninterface VariableDefinition {
  id: VariableId;
  name: string;
  scope: "screen" | "shared";
  valueType: "boolean" | "number" | "string" | "json";
  defaultValue: JsonValue;
}\n\nPage-local transient state is runtime state and normally not represented as a persistent global VariableDefinition. Shared means shared between Screens of the same Player process, not automatically between separate computers.\n\n- Screen variables reset on Reset Screen / clean Player session.\n\n- Shared Player variables reset on clean Player session.\n\n- Disk persistence is not part of initial V2.\n\n- Cross-computer variable replication is not implicit.\n\n### 15. Triggers, Behavior Flows and Actions\n\ninterface BehaviorFlow {
  id?: BehaviorFlowId;
  steps: BehaviorStep[];
}

type BehaviorStep =
  | ActionStep
  | DelayStep
  | IfStep;

interface ActionStep {
  kind: "action";
  actionType: string;
  target?: ActionTarget;
  params?: Record<string, JsonValue>;
}

interface DelayStep {
  kind: "delay";
  durationMs: number;
}

interface IfStep {
  kind: "if";
  condition: ConditionExpression;
  then: BehaviorStep[];
  else?: BehaviorStep[];
}\n\nBehavior execution is ordered, nonblocking with respect to the global runtime, and cancellable by owner lifecycle. Delay pauses only its own flow.\n\n### 16. Trigger bindings\n\ninterface TriggerBinding {
  id: TriggerBindingId;
  trigger: TriggerDefinition;
  flow: BehaviorFlow;
}

type TriggerDefinition =
  | PointerTrigger
  | KeyboardTrigger
  | MouseTrigger
  | NetworkTrigger
  | TimelineTrigger
  | MediaEventTrigger
  | VariableChangedTrigger
  | LifecycleTrigger
  | IdleTrigger
  | WidgetTrigger;\n\nIncoming TCP/UDP commands are triggers, not special-case navigation commands. The same Action Engine executes behaviors regardless of trigger source.\n\n### 17. Network authoring model\n\ninterface NetworkAuthoringConfig {
  endpoints: Record<NetworkEndpointId, NetworkEndpoint>;
  listeners: NetworkListenerDefinition[];
  triggerBindings: NetworkTriggerBinding[];
}

interface NetworkEndpoint {
  id: NetworkEndpointId;
  name: string;
  transport: "tcp" | "udp";
  host: string;
  port: number;
  tcpFraming?: "newline" | "fixed" | "raw";
}\n\n- Incoming matching supports Exact, Starts With and Contains in initial V2.\n\n- Optional source IP/source-port filtering is persisted in the trigger definition.\n\n- Regex matching is deferred.\n\n- Multi-PC synchronization configuration is deployment-local Player configuration, not ordinary project network authoring data.\n\n### 18. Timelines\n\n### 18.1 Page Timeline\n\ninterface PageTimelineDefinition {
  autoPlay: boolean;
  events: PageTimelineEvent[];
}

interface PageTimelineEvent {
  id: TimelineEventId;
  atMs: number;
  policy: "everyPageEnter" | "oncePerScreenSession";
  flow: BehaviorFlow;
}\n\nPage Timeline time is relative to Page Enter. It has no required finite duration. Page Leave cancels its pending Page-owned work.\n\n### 18.2 Media Timeline\n\ninterface MediaTimelineDefinition {
  events: MediaTimelineEvent[];
}
interface MediaTimelineEvent {
  id: TimelineEventId;
  atSourceMs: number;
  flow: BehaviorFlow;
}\n\nMedia Timeline follows actual media playback time, including pause, seek and loop-range crossings.\n\n### 19. Popup model\n\ninterface PopupDefinition {
  id: PopupId;
  name: string;
  rootElementIds: ElementId[];
  elements: Record<ElementId, ElementDefinition>;
  modal: boolean;
  backdrop?: BackdropDefinition;
  openTransition?: TransitionDefinition;
  closeTransition?: TransitionDefinition;
  closeOnBackdrop?: boolean;
  behaviors?: PopupBehaviorBindings;
}\n\nPopups are Page-owned. Navigation away from the Page closes the popup stack. Reuse across Pages is achieved through Components rather than global Popup identity.\n\n### 20. Screensaver and Error Visual\n\ninterface ScreensaverDefinition {
  enabled: boolean;
  visual: SimpleSystemVisual;
  enterTransition?: TransitionDefinition;
  exitTransition?: TransitionDefinition;
  exitOnUserInput?: boolean;
}

interface ErrorVisualDefinition {
  customVisual?: SimpleSystemVisual;
  showShortCode?: boolean;
}

interface SimpleSystemVisual {
  background?: ColorValue;
  imageAssetId?: AssetId;
  videoAssetId?: AssetId;
  textItems?: SimpleTextOverlay[];
  loop?: boolean;
  muted?: boolean;
  volume?: number;
}\n\nScreensaver and Error Visual are intentionally simpler than Pages. A built-in neutral Error Visual exists even when no custom one is configured.\n\n### 21. Content Admin exposure model\n\ninterface ContentAdminDefinition {
  exposedProperties: AdminExposureRule[];
}
interface AdminExposureRule {
  entityId: EntityId;
  propertyPath: string;
  label?: string;
  allowedOperation: "editValue" | "replaceAsset" | "reorderItems";
}\n\nAdmin exposure is allow-list based. Initial V2 does not grant structural creation/deletion of Screens, Pages, arbitrary cards/blocks, Actions, Variables or Timelines.\n\n### 22. Authoring-only metadata\n\ninterface AuthoringMetadata {
  designerLayout?: Record<EntityId, DesignerFramePosition>;
  notes?: Record<EntityId, string>;
  provenance?: Record<EntityId, RequirementProvenance[]>;
}\n\nDesigner Canvas frame positions are authoring metadata. They help arrange Page/Popup/Screensaver frames in Constructor and do not define runtime pixel coordinates.\n\n### 23. PlayerLocalConfig — deliberately outside .iss\n\ninterface PlayerLocalConfig {
  selectedBuildPath?: string;
  projectId?: ProjectId;

  displayMappings: DisplayMapping[];
  startup: PlayerStartupSettings;
  developer: DeveloperSettings;

  installationMode: "singlePc" | "multiPc";
  node?: MultiPcNodeConfig;
}\n\n- Display mapping is deployment-specific and must not travel with the project.\n\n- Reinstalling/updating Player should preserve compatible PlayerLocalConfig.\n\n- A missing physical Display never silently remaps a Screen.\n\n- Multi-PC node identity, Master address and required/optional node configuration belong to installation configuration.\n\n### 24. Multi-PC data boundary\n\nThe project schema defines actions and runtime targets. It does not add a per-action 'Synchronized' flag. When Player runs in Multi-PC installation mode, the Runtime Coordinator decides whether a cross-node/multi-node operation requires distributed preparation and timestamped execution.\n\nDistributed operation (conceptual wire model):
{
  operationId,
  targetNodeIds,
  action,
  phase: "PREPARE" | "READY" | "EXECUTE",
  executeAtMasterTime?
}\n\nThe exact network wire protocol, heartbeat and clock-resync format belong to the separate Network/Sync engineering specification, not ProjectDocument.\n\n### 25. Build compilation model\n\nProjectDocument (.iss)
  -> snapshot
  -> full validation
  -> runtime dependency discovery
  -> Runtime Compiler
  -> asset materialization
  -> project.json
  -> manifest.json
  -> atomic publish\n\n### 26. RuntimeProject (project.json)\n\ninterface RuntimeProject {
  runtimeFormatVersion: number;
  projectId: ProjectId;
  buildId: BuildId;

  screens: RuntimeScreen[];
  assets: Record<AssetId, RuntimeAsset>;
  playlists: Record<PlaylistId, RuntimePlaylist>;
  variables: RuntimeVariableDefinition[];
  network: RuntimeNetworkDefinition;
}\n\nRuntimeProject may be structurally different from ProjectDocument. The Runtime Compiler is the only supported transformation boundary; Player code must not depend on authoring-only fields.\n\n### 27. Build manifest\n\ninterface BuildManifest {
  buildId: BuildId;
  projectId: ProjectId;
  runtimeFormatVersion: number;
  createdAt: string;
  assets: BuildManifestAsset[];
}
interface BuildManifestAsset {
  assetId: AssetId;
  path: string;
  kind: string;
  sizeBytes: number;
  hash: string;
}\n\nThe manifest supports validation, diagnostics and integrity checks. A failed Build never replaces the last successfully published Build.\n\n### 28. Serialization rules\n\n- JSON must be deterministic enough for diagnostics and meaningful diffs; stable ordering is recommended for emitted registries/order arrays.\n\n- Unknown required entity types or newer formatVersion cause safe refusal rather than best-effort corruption.\n\n- Optional fields have explicit defaults in the schema/migration layer; runtime code should not scatter ad-hoc fallback semantics.\n\n- NaN, Infinity, functions, DOM objects, class instances and binary blobs are forbidden in ProjectDocument JSON.\n\n- Dates serialize as ISO-8601 strings.\n\n- Paths in Working Project may be absolute source paths; paths in RuntimeProject are Build-relative.\n\n- Transient computed caches are never serialized as source of truth.\n\n### 29. Schema validation\n\nValidation is layered and uses the same canonical validation engine for Open, Save, Collect and Build.\n\n### 30. Format version and migrations\n\ninterface ProjectFileEnvelope {
  formatVersion: number;
  project: ProjectDocumentPayload;
}\n\nmigrateV3toV4(input) -> V4
migrateV4toV5(input) -> V5
migrateV5toV6(input) -> Current\n\n- Migrations are sequential and forward-only.\n\n- The loaded in-memory ProjectDocument is always current-format.\n\n- Opening an older project does not immediately overwrite the original file.\n\n- First Save after migration creates a migration backup before writing the current format.\n\n- An older Constructor refuses a newer unsupported format safely.\n\n- formatVersion is independent of application version.\n\n### 31. Copy / Duplicate / Import remapping\n\nEvery graph-copy operation must explicitly compute an ID remap before insertion.\n\n1. Discover owned graph
2. Allocate new IDs for cloned entities
3. Clone data
4. Rewrite internal references through idMap
5. Preserve references to dependencies outside graph
6. Validate cloned graph
7. Commit as one undoable Project Operation\n\nThis rule applies to Pages, Containers, Popups, Components, imported structured SVG trees and any future reusable graph entity.\n\n### 32. Undo/Redo transaction boundary\n\nProject mutations occur only through Project Operations. Each user-level operation should produce one reversible history transaction where practical. Build, Collect, Preview and validation consume snapshots and do not mutate ProjectDocument as a side effect.\n\n### 33. Runtime lifecycle implications\n\n### 34. Error and missing-resource semantics\n\n- Missing used source asset is a Build Error.\n\n- Unused missing source asset does not block Build.\n\n- If a packaged runtime asset is later deleted/corrupted, Player degrades locally where possible and logs the failure.\n\n- A failed playlist item may be skipped according to media policy.\n\n- A critical Screen render/runtime failure uses Error Visual for that Screen only.\n\n- Raw stack traces and technical errors are never visitor-facing.\n\n### 35. Targeted media preparation\n\nThe data model intentionally does not encode a global predictive HOT/WARM/COLD cache. Initial V2 uses simple on-demand loading plus targeted preparation.\n\n- Startup/system essentials are prepared as needed.\n\n- Screen Media Player prepares requested media before playback.\n\n- Playlist may prepare current + next item.\n\n- Widgets may implement small local preparation windows.\n\n- Multi-PC synchronized media uses PREPARE → READY → timestamped EXECUTE/START.\n\n- A future explicit preload hint may be added without changing the identity/reference architecture.\n\n### 36. Compatibility dispositions encoded by this model\n\n### 37. Canonical minimal .iss example\n\n{
  "formatVersion": 1,
  "projectId": "prj_demo",
  "name": "Museum Demo",
  "createdAt": "2026-10-06T20:00:00Z",
  "modifiedAt": "2026-10-06T20:00:00Z",
  "settings": { "...": "..." },
  "screens": {
    "scr_main": {
      "id": "scr_main",
      "name": "Main Screen",
      "width": 1920,
      "height": 1080,
      "pageIds": ["page_idle"],
      "initialPageId": "page_idle",
      "pages": {
        "page_idle": {
          "id": "page_idle",
          "name": "Idle",
          "flowMode": "navigation",
          "rootElementIds": [],
          "elements": {},
          "background": {
            "kind": "video",
            "assetId": "asset_idle_video",
            "autoplay": true,
            "loop": true,
            "muted": false,
            "volume": 1.0
          },
          "popupIds": [],
          "popups": {},
          "idle": { "enabled": false }
        }
      }
    }
  },
  "assets": {
    "asset_idle_video": {
      "id": "asset_idle_video",
      "name": "Idle Loop",
      "kind": "video",
      "sourcePath": "D:/MuseumAssets/idle.mp4",
      "metadata": {}
    }
  }
}\n\n### 38. Engineering invariants\n\nINV-01  ProjectDocument is the only editable source of project truth.\n\nINV-02  Runtime state never writes itself back into ProjectDocument.\n\nINV-03  Player never opens .iss.\n\nINV-04  No runtime entity targets a physical monitor directly; actions target logical Screens.\n\nINV-05  No project element references an asset by filesystem path.\n\nINV-06  No separate Screenless mode exists in V2.\n\nINV-07  Page background video/media may play audio.\n\nINV-08  Exactly one system Screen Media Player exists per Screen.\n\nINV-09  Display mapping and Multi-PC node topology are deployment-local.\n\nINV-10  Component updates never silently mutate existing instances.\n\nINV-11  Build is snapshot-based and atomic.\n\nINV-12  Preview and Player consume the same Runtime Engine semantics.\n\nINV-13  All input sources converge on Trigger → Behavior Flow → Action Engine.\n\nINV-14  Lifecycle ownership determines cancellation and cleanup.\n\nINV-15  A schema migration is explicit, sequential and testable.\n\n### 39. Documents derived next\n\n- Machine-readable JSON Schema / TypeScript domain types.\n\n- Runtime State Model and state-machine specification.\n\n- Widget Contract specification.\n\n- Build Specification with exact dependency/materialization algorithm.\n\n- Network & Multi-PC Synchronization Protocol specification.\n\n- V1 Compatibility Matrix with V1-F001…V1-F178 → V2 model/action/test mapping.\n\n- Test & Acceptance Plan.\n\n### 40. Status\n\nThis document is the canonical V2 data-model baseline following architecture decisions A-001–A-036. Low-level field additions are allowed during implementation when they preserve these ownership, identity, lifecycle and compatibility invariants. Any change that alters a product-visible behavior or one of the invariants above requires an explicit architecture revision.\n\n\n### Extracted table 1\n\n| Layer | Artifact / state | Purpose | Persistent? |\n\n| --- | --- | --- | --- |\n\n| Authoring | ProjectDocument (.iss) | Full editable project, including authoring metadata and virtual asset registry | Yes |\n\n| Editor UI | EditorState | Selection, canvas pan/zoom, panels, temporary tools | No |\n\n| Build | RuntimeProject (project.json) | Compiled Player-facing definition with only runtime dependencies | Yes, in Build |\n\n| Deployment | PlayerLocalConfig | Build path, Screen→Display mapping, node role/network setup, technician settings | Yes, outside project |\n\n| Runtime | RuntimeSession / SharedRuntimeState | Current pages, media, variables, timelines, idle, locks, popup stack | No by default |\n\n| Recovery | RecoverySnapshot | Unsaved ProjectDocument recovery after abnormal Constructor termination | Temporary |\n\n\n### Extracted table 2\n\n| Use stable entity ID when… | Use nested value object when… |\n\n| --- | --- |\n\n| Other objects/actions may target it | It exists only as configuration of its owner |\n\n| It has independent lifecycle | It cannot sensibly exist outside its owner |\n\n| It is reusable or referenceable | It is replaced together with its owner |\n\n| It needs diagnostics/provenance | No external reference is required |\n\n\n### Extracted table 3\n\n| Initial widget family | Representative persisted configuration |\n\n| --- | --- |\n\n| Gallery | items, order, viewport, controls, pagination, loop, transition |\n\n| Image Viewer | asset, viewport, min/max zoom, pan/reset controls |\n\n| Quiz | questions, answers, visual states, scoring/result settings |\n\n| Form | fields, validation, submit/reset behavior, bindings |\n\n| Mini-game | widget-specific serialized contract; implementation may use Canvas/WebGL |\n\n\n### Extracted table 4\n\n| Action family | Initial action types |\n\n| --- | --- |\n\n| Navigation | Navigate Page, Next, Previous, Go Back, Go Home |\n\n| Popup | Open, Close, Close All |\n\n| Media | Load/Set, Play, Pause, Stop, Restart, Seek, Next/Previous Item, Volume, Mute |\n\n| Variables | Set, Add, Subtract, Toggle, Reset |\n\n| Animation/State | Play/Stop/Restart Animation, Show/Hide, Set/Reset State |\n\n| Interaction | Lock, Unlock |\n\n| Network | Send TCP, Send UDP |\n\n| Timeline | Start, Pause, Resume, Stop, Restart |\n\n| Runtime | Reset Screen, Go Initial, Reset Idle Timer, Start/Stop Screensaver |\n\n\n### Extracted table 5\n\n| Authoring data | Runtime output |\n\n| --- | --- |\n\n| sourcePath | Removed/replaced by packaged relative asset path |\n\n| Designer Canvas frame positions | Removed |\n\n| Unused assets | Excluded from Build |\n\n| Component revision authoring history | Flattened/compiled to runtime representation as appropriate |\n\n| Admin exposure metadata | Excluded unless runtime explicitly needs it |\n\n| Runtime-relevant Screens/Pages/Elements/Actions | Included |\n\n| Project fonts used by runtime | Packaged and referenced |\n\n| Player display mapping | Never included |\n\n\n### Extracted table 6\n\n| Layer | Examples |\n\n| --- | --- |\n\n| Structural/schema | required fields, enum values, number ranges, correct entity shape |\n\n| Referential | missing pageId/assetId/componentId, parent-child mismatch, cyclic containment |\n\n| Semantic | initialPageId belongs to Screen, illegal target scope, invalid timeline range |\n\n| Resource | missing source asset, unreadable font/media, unsupported build dependency |\n\n| Deployment/runtime | runtime-format compatibility and Build integrity |\n\n\n### Extracted table 7\n\n| Owner | Runtime lifetime |\n\n| --- | --- |\n\n| Page-local state / Page flow | Created on Page Enter; cancelled/discarded on Leave |\n\n| Screen variables | Screen RuntimeSession |\n\n| Shared variables | Player Runtime session |\n\n| Screen Media Player | Screen RuntimeSession |\n\n| Screensaver | Screen-owned overlay; does not cause Page Leave/Enter |\n\n| Popup | Page-owned; destroyed on close/navigation |\n\n| Once-per-session timeline flags | Screen RuntimeSession |\n\n| Persistent disk state | Not part of initial V2 |\n\n\n### Extracted table 8\n\n| Legacy / brief concept | V2 data-model disposition |\n\n| --- | --- |\n\n| V1 Screenless Mode | Revised/Covered: normal Screen + Page background media with audio + Screen Media Player |\n\n| V1 Screen→physical Display saved in project | Revised: PlayerLocalConfig |\n\n| V1 filesystem Content folder as sequence | Revised: first-class Playlist; folder import is convenience |\n\n| Original full theme switching | Deferred; color variables/default styles/fonts/components retained |\n\n| Original separate Content Admin app | Revised: restricted mode of Constructor |\n\n| Original Admin structural card/block creation | Deferred/revised out of initial V2 |\n\n| Dedicated iRidi subsystem | Revised: generic TCP/UDP unless deployment proves adapter necessary |\n\n| Implicit cross-PC shared variables | Not required; distributed synchronized actions are explicit installation behavior |\n