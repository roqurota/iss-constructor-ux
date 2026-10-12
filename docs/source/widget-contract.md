# ISS CONSTRUCTOR V2\n\nWidget Contract Specification\n\nUnified contract for configurable functional modules in Constructor and Runtime\n\nEngineering baseline • Gallery • Image Viewer • Quiz • Form • Mini-game\n\n### 1. Purpose\n\nA Widget is a ready functional module with internal behavior and state that participates in the same project, runtime, action, trigger, asset, validation and lifecycle architecture as ordinary Elements. This specification prevents each Widget from becoming a one-off subsystem.\n\n- Widgets may have very different internal implementations.\n\n- Constructor sees every Widget through a common descriptor/contract.\n\n- Each widgetType defines its own relevant editable properties rather than exposing one universal property panel.\n\n- Widget internals do not need to be represented as ordinary Page Elements.\n\n- Widgets must not bypass the Runtime Action/Trigger architecture for project-visible behavior.\n\n- Initial V2 supports internal extensibility; a public third-party SDK is not part of the initial product.\n\n### 2. Element, Component and Widget\n\nA Component may contain Widgets. A Widget may internally render many controls without exposing those controls as independently editable project Elements.\n\n### 3. Canonical persisted Widget instance\n\ninterface WidgetElement extends ElementBase {
  type: "widget";
  widgetType: string;
  widgetSchemaVersion: number;
  props: Record<string, JsonValue>;
  stateDefaults?: Record<string, JsonValue>;
}\n\n- widgetType is a stable registry key, not a display label.\n\n- widgetSchemaVersion versions the persisted props contract for that widget type.\n\n- ElementBase supplies transform, visibility, opacity, z-order and common behavior integration.\n\n- props contains only configuration declared by the Widget Contract.\n\n- Transient runtime state is never serialized into props.\n\n### 4. Widget registry and contract\n\ninterface WidgetContract {
  widgetType: string;
  displayName: string;
  schemaVersion: number;

  propertySchema: WidgetPropertySchema;
  actions: WidgetActionDescriptor[];
  triggers: WidgetTriggerDescriptor[];

  resolveAssetDependencies(props): AssetDependency[];
  validate(instance, context): Problem[];
  createRuntime(context, props): WidgetRuntime;

  migrateProps?(fromVersion, props): MigratedWidgetProps;
}\n\nConstructor, validator, Runtime Compiler and Runtime Engine resolve Widget behavior through this registry rather than scattered widget-specific switch statements.\n\n### 5. Property contract\n\ninterface WidgetPropertyDescriptor {
  key: string;
  label: string;
  valueType:
    | "boolean" | "number" | "string" | "enum"
    | "color" | "asset" | "assetList"
    | "icon" | "length" | "json";
  defaultValue?: JsonValue;
  required?: boolean;
  min?: number;
  max?: number;
  enumValues?: string[];
  assetKinds?: AssetKind[];
  group?: string;
  helpText?: string;
}\n\nImage Viewer, Quiz and Form expose their own property groups. Constructor must not pretend that all Widgets have the same options.\n\n### 6. Widget Actions\n\ninterface WidgetActionDescriptor {
  actionType: string;
  label: string;
  targetRequired: boolean;
  parameterSchema?: ActionParameterSchema;
}\n\nWidget Actions register with the same Action Engine. Buttons, TCP/UDP triggers, Timelines and other runtime sources invoke them through ordinary Behavior Flows.\n\n### 7. Widget Triggers\n\ninterface WidgetTriggerDescriptor {
  triggerType: string;
  label: string;
  payloadSchema?: JsonSchema;
}\n\nWidget Triggers emit ordinary runtime events. They do not directly navigate Pages, send network messages or mutate global Variables unless their configured Behavior Flow invokes the corresponding Actions.\n\n### 8. Runtime lifecycle\n\ninterface WidgetRuntime {
  mount(context: WidgetRuntimeContext): void | Promise<void>;
  activate?(): void;
  deactivate?(): void;
  handleAction(action: WidgetActionInvocation): ActionResult | Promise<ActionResult>;
  getDebugState?(): JsonValue;
  dispose(): void;
}\n\n### 9. Runtime capabilities\n\ninterface WidgetRuntimeContext {
  screenId: ScreenId;
  pageId: PageId;
  elementId: ElementId;

  assets: RuntimeAssetResolver;
  actions: RuntimeActionDispatcher;
  events: RuntimeEventEmitter;
  variables: RuntimeVariableAccess;
  logger: RuntimeLogger;
  clock: RuntimeClock;
}\n\n- Widgets receive explicit capabilities rather than unrestricted access to RuntimeSession internals.\n\n- Project-visible consequences are requested through Action Dispatcher or emitted Triggers.\n\n- Widgets must not directly mutate another Page, Screen, Popup, Screen Media Player or Variable store.\n\n- Assets are resolved by assetId, never authoring sourcePath.\n\n### 10. State model\n\nA Widget never silently promotes internal state to Shared Variables. Cross-Page or cross-Screen sharing is explicit.\n\n### 11. Asset dependencies\n\ninterface AssetDependency {
  assetId: AssetId;
  usage: "required" | "optional";
  purpose?: string;
}\n\n- Build dependency discovery calls the Widget Contract.\n\n- Required missing assets cause validation/build errors.\n\n- Optional assets may use widget-defined fallback behavior.\n\n- Widgets cannot hide arbitrary filesystem dependencies outside Asset Registry.\n\n- Fonts/icons/media needed by a Widget must be declared or packaged as system/widget resources.\n\n### 12. Validation\n\nWidget validation participates in the unified Project Validation Engine and returns normal Problem objects. Widgets do not invent separate validation infrastructure.\n\n### 13. Widget schema migrations\n\nmigrateWidgetProps(
  widgetType,
  fromSchemaVersion,
  props
) -> { schemaVersion, props }\n\n- Project formatVersion and widgetSchemaVersion solve different problems.\n\n- Widget props may evolve without forcing unrelated project entities to change.\n\n- Migrations are explicit, sequential and testable.\n\n- Unknown newer widget schemas fail safely rather than being guessed.\n\n### 14. Rendering\n\n- The outer Widget obeys normal Element transform/visibility/opacity/layering semantics.\n\n- Specialized internal rendering does not alter project-level lifecycle, Actions or Triggers.\n\n- Fullscreen/global takeover is never implicit; use explicit project/system entities and Actions.\n\n### 15. Input\n\n- Pointer/touch handling is scoped to the Widget visual region unless the Widget contract explicitly defines otherwise.\n\n- Interaction Lock applies to Widget user input according to lock scope.\n\n- Project-level keyboard/mouse control enters through the common input architecture.\n\n- Widgets must not leave global listeners/timers active after dispose.\n\n- Multi-touch/gesture behavior is widget-specific and must be declared by that Widget.\n\n### 16. Styling and customization\n\nVisual flexibility is required, but exposing every internal node as a Page Element is not. Project color variables and packaged project fonts should be usable wherever the property type supports them.\n\n### 17. Gallery — initial contract\n\nwidgetType: "gallery"
props:
  items
  initialIndex
  loop
  fit
  transition
  previousControl
  nextControl
  pagination
actions:
  gallery.next
  gallery.previous
  gallery.goTo
  gallery.reset
triggers:
  gallery.itemChanged
  gallery.firstItem
  gallery.lastItem
  gallery.finished\n\n- Gallery is not a Playlist and does not inherit Screen Media Player semantics.\n\n- Gallery content remains inside the Page.\n\n- Previous/current/next assets may be locally prepared as an implementation optimization.\n\n- Navigation control visuals are customizable through Gallery properties.\n\n### 18. Image Viewer — initial contract\n\nwidgetType: "imageViewer"
props:
  assetId
  fit
  minZoom
  maxZoom
  initialZoom
  panEnabled
  resetControl
actions:
  imageViewer.zoomIn
  imageViewer.zoomOut
  imageViewer.setZoom
  imageViewer.panTo
  imageViewer.reset
triggers:
  imageViewer.zoomChanged
  imageViewer.reset\n\n- Zoom/pan transform is internal Widget runtime state.\n\n- Transforming the outer Widget Element is separate from zooming the viewed image.\n\n- Reset returns to the configured initial view.\n\n### 19. Quiz — initial contract\n\nwidgetType: "quiz"
props:
  questions
  answerMode
  scoring
  stateStyles
  resultView
actions:
  quiz.selectAnswer
  quiz.submit
  quiz.next
  quiz.reset
triggers:
  quiz.answerSelected
  quiz.correct
  quiz.incorrect
  quiz.completed
  quiz.scoreChanged\n\n- Question progression is internal Widget state.\n\n- Project-visible consequences use Triggers + Behavior Flows.\n\n- Score may remain internal or be explicitly written/bound to a Screen/Shared Variable.\n\n- Quiz must support the reference-case pattern selection → feedback → progression without custom application code.\n\n### 20. Form — initial contract\n\nwidgetType: "form"
props:
  fields
  validationRules
  visualStates
actions:
  form.setField
  form.clearField
  form.submit
  form.reset
triggers:
  form.fieldChanged
  form.valid
  form.invalid
  form.submitted\n\n- Initial V2 is local/offline-first; Form does not imply a cloud backend.\n\n- Values remain Widget runtime state unless explicitly mapped to approved project data/Variables.\n\n- Persistent visitor records are not silently created by using a Form Widget.\n\n- Storage/privacy requirements, if later needed, require a separate explicit design.\n\n### 21. Mini-game family\n\nMini-game is a Widget family rather than one universal gameplay schema. Each game type registers its own contract while obeying the common Widget boundary.\n\n- Canvas/WebGL may be used internally.\n\n- Lifecycle/dispose behavior must be deterministic.\n\n- Project-visible start/reset/result/score events are exposed as registered Actions/Triggers where relevant.\n\n- All asset dependencies are declared.\n\n- A game must not directly navigate Pages or send TCP/UDP; it emits Triggers whose Behavior Flows may do so.\n\n- Repeated Enter/Leave/Reset must not leak render loops, timers or listeners.\n\n### 22. Widget errors and fallback\n\n### 23. Constructor integration\n\n- Add Widget creates a WidgetElement with contract defaults.\n\n- Properties panel is generated from the Widget's property schema plus any widget-specific editor needed for complex data.\n\n- Actions panel lists registered Widget Actions when the Widget is selected as a target.\n\n- Trigger/Behavior editor lists registered Widget Triggers.\n\n- Problems panel receives Widget validation results.\n\n- Duplicate/Copy/Paste remaps Widget Element identity while preserving valid external asset/variable references.\n\n- Component definitions may include Widget instances.\n\n### 24. Runtime Compiler integration\n\nWidgetElement
  → resolve WidgetContract(widgetType)
  → validate schema version/props
  → discover asset dependencies
  → compile runtime props
  → include runtime widget descriptor in project.json\n\n- Authoring-only editor metadata is excluded.\n\n- Runtime Compiler may normalize props for efficient runtime use.\n\n- Compiled representation must preserve the same Widget semantics.\n\n- Unknown widgetType is a Build Error.\n\n### 25. Preview and diagnostics\n\n- Full Preview uses the same Widget runtime implementation as Player.\n\n- Developer overlay may request getDebugState() where supported.\n\n- Debug state must be read-only and safe to inspect.\n\n- Action/Event Trace shows Widget Actions and Triggers like any other runtime events.\n\n- Widget diagnostics include widgetType, elementId, PageId and relevant error context.\n\n### 26. Performance and preparation\n\n- No global Widget cache architecture is mandated.\n\n- Widgets may implement small local preparation strategies appropriate to their content.\n\n- Gallery may prepare adjacent items; Image Viewer may decode its current image; Mini-game may prepare declared assets on mount.\n\n- Widget preparation must be cancellable/ignorable when Page lifecycle invalidates the Widget.\n\n- Heavy synchronous initialization should not freeze the renderer event loop.\n\n### 27. Accessibility / kiosk interaction baseline\n\n- Widgets should expose clear enabled/disabled/selected visual states where relevant.\n\n- Touch targets and text sizing remain designer-configurable, but Widget defaults should be kiosk-appropriate.\n\n- Keyboard navigation support may be implemented where meaningful and must coexist with preserved V1 project-level keyboard/mouse control.\n\n- Browser focus artifacts must not become unintended visitor UI.\n\n### 28. Security boundary\n\n- Widget props are data, not executable arbitrary JavaScript.\n\n- Initial V2 does not permit project authors to inject arbitrary runtime code into Widgets.\n\n- Widgets do not receive unrestricted Node.js/filesystem/network access in renderer context.\n\n- External communication uses approved Runtime Actions/services.\n\n- This keeps Build projects portable and reduces the risk of a project escaping its runtime sandbox.\n\n### 29. Widget authoring extension process\n\nAdding an internal new Widget type should require a predictable package of implementation artifacts.\n\nA future public SDK may wrap this same internal contract, but public compatibility/security/versioning commitments are explicitly deferred.\n\n### 30. Widget invariants\n\nW-INV-01  Every Widget has a stable widgetType and widgetSchemaVersion.\n\nW-INV-02  Every persisted Widget configuration is data, not arbitrary executable code.\n\nW-INV-03  Every project-visible Widget operation uses registered Actions/Triggers.\n\nW-INV-04  Widget runtime state is Page-owned unless explicitly exported through project Variables.\n\nW-INV-05  Page Leave invalidates Widget-owned async work.\n\nW-INV-06  Widget asset dependencies are visible to Build dependency discovery.\n\nW-INV-07  Widget errors should be locally contained where technically possible.\n\nW-INV-08  Widgets do not directly own physical Displays, Screen Media Player or network sockets.\n\nW-INV-09  Widget-specific customization may differ substantially between Widget types.\n\nW-INV-10  Widget internals need not be exposed as ordinary Page Elements.\n\nW-INV-11  Preview and Player use the same Widget runtime semantics.\n\nW-INV-12  New internal Widgets conform to this contract rather than adding parallel architecture.\n\n### 31. Required test families\n\n### 32. Initial V2 Widget set\n\nThis table defines architectural expectation, not final implementation sprint priority.\n\n### 33. Status\n\nThis Widget Contract Specification is the canonical V2 baseline for functional modules following Architecture A-032 and the approved Project Data Model / Runtime State Model. Implementation details may evolve while preserving the contract boundaries and invariants above.\n\n\n### Extracted table 1\n\n| Concept | Definition | Examples |\n\n| --- | --- | --- |\n\n| Element | Primitive visual/runtime building block | Text, Image, Button, Video, Container |\n\n| Component | Designer-built reusable composition | Exhibit Card, Header, branded navigation block |\n\n| Widget | Functional module with internal state/logic and declared customization contract | Gallery, Image Viewer, Quiz, Form, Mini-game |\n\n\n### Extracted table 2\n\n| Gallery property group | Representative settings |\n\n| --- | --- |\n\n| Content | Assets, order, initial item |\n\n| Viewport | Fit/fill/stretch, crop/viewport behavior |\n\n| Navigation | Previous/Next visibility, position, size, icon/image, states |\n\n| Pagination | Show/hide, position, indicator style |\n\n| Playback | Loop, optional auto-advance |\n\n| Transition | Item transition type and duration |\n\n\n### Extracted table 3\n\n| Widget | Representative Actions |\n\n| --- | --- |\n\n| Gallery | Next, Previous, GoTo, Reset |\n\n| Image Viewer | ZoomIn, ZoomOut, SetZoom, PanTo, ResetView |\n\n| Quiz | SelectAnswer, Submit, NextQuestion, Reset |\n\n| Form | SetField, ClearField, Submit, Reset |\n\n| Mini-game | Start, Reset and widget-specific commands |\n\n\n### Extracted table 4\n\n| Widget | Representative Triggers |\n\n| --- | --- |\n\n| Gallery | On Item Changed, On First Item, On Last Item, On Finished |\n\n| Image Viewer | On Zoom Changed, On Reset |\n\n| Quiz | On Answer Selected, On Correct, On Incorrect, On Completed, On Score Changed |\n\n| Form | On Field Changed, On Valid, On Invalid, On Submitted |\n\n| Mini-game | On Started, On State Changed, On Score Changed, On Finished |\n\n\n### Extracted table 5\n\n| Lifecycle | Requirement |\n\n| --- | --- |\n\n| Page Enter / mount | Create fresh Page-owned Widget runtime from persisted props/state defaults. |\n\n| Active | Accept user input and registered Widget Actions. |\n\n| Page Leave | Cancel Widget-owned pending work and dispose runtime. |\n\n| Reset Screen | Dispose/recreate through normal Page lifecycle. |\n\n| Widget error | Contain where possible to Widget boundary; Page should continue. |\n\n| Async completion after disposal | Ignore using owner/generation-token semantics. |\n\n\n### Extracted table 6\n\n| State type | Example | Lifetime |\n\n| --- | --- | --- |\n\n| Persisted props | Gallery items, loop, transition | Project/Build |\n\n| State defaults | Initial selected item, initial quiz mode | Project/Build |\n\n| Internal runtime state | Gallery index, zoom matrix, selected answer | Current Page activation |\n\n| Explicit Project Variable | Language, shared score/result if configured | Screen/Shared runtime scope |\n\n\n### Extracted table 7\n\n| Severity | Examples |\n\n| --- | --- |\n\n| Error | Required asset missing; invalid required question set; broken variable binding; impossible numeric range |\n\n| Warning | Gallery has one item while navigation controls are enabled; optional configuration inconsistency |\n\n| Info | Non-blocking optimization or authoring suggestion |\n\n\n### Extracted table 8\n\n| Renderer | Typical use |\n\n| --- | --- |\n\n| DOM/CSS | Forms, galleries, quizzes, ordinary UI |\n\n| SVG | Vector controls, diagrams, masks |\n\n| Canvas | High-frequency custom drawing and some games |\n\n| WebGL/WebGPU | Specialized demanding mini-games/visual modules where justified |\n\n\n### Extracted table 9\n\n| Surface | Examples |\n\n| --- | --- |\n\n| Container | Background, border, radius, clipping |\n\n| Typography | Project font, size, color, alignment |\n\n| Controls | Position, size, icon/image, colors and visual states |\n\n| Content viewport | Fit/fill, crop, spacing |\n\n| State visuals | Normal, Selected, Correct, Incorrect, Disabled as relevant |\n\n| Transitions | Widget-specific type/duration |\n\n\n### Extracted table 10\n\n| Failure | Required behavior |\n\n| --- | --- |\n\n| Invalid props before Build | Validation Error blocks Build when required for correct runtime. |\n\n| Optional asset unavailable | Localized widget fallback and log. |\n\n| Widget runtime exception | Contain at Widget boundary where technically possible; show Widget unavailable placeholder; Page continues. |\n\n| Repeated internal error | Avoid uncontrolled restart/logging loops. |\n\n| Critical renderer crash | Handled by Screen-level recovery, outside Widget contract. |\n\n\n### Extracted table 11\n\n| Required artifact | Purpose |\n\n| --- | --- |\n\n| WidgetContract descriptor | Identity, properties, Actions, Triggers, schema version |\n\n| Constructor editor integration | Add palette entry and property/editor UI |\n\n| Runtime implementation | Actual behavior/rendering |\n\n| Validator | Project/Build correctness |\n\n| Asset dependency resolver | Build packaging |\n\n| Props migrations | Future compatibility when schema changes |\n\n| Tests | Lifecycle, actions/triggers, invalid input, rapid reset/leave, runtime fallback |\n\n\n### Extracted table 12\n\n| Family | Examples |\n\n| --- | --- |\n\n| Schema | Defaults, invalid props, widgetSchemaVersion migration |\n\n| Lifecycle | Mount, Page Leave, re-enter, Reset Screen, dispose |\n\n| Actions | All registered Actions with valid/invalid parameters |\n\n| Triggers | Correct payload and no duplicate unintended emission |\n\n| Rapid interaction | Repeated next/reset/submit/zoom without corrupted state |\n\n| Async invalidation | Late asset/decode/result after Page Leave ignored |\n\n| Assets | Missing required vs optional assets, Build dependency inclusion |\n\n| Components | Widget inside Component instance/revision/update/detach |\n\n| Preview parity | Same behavior in Constructor Preview and Player |\n\n| Fault isolation | Widget failure does not intentionally kill Page/Screen |\n\n| Soak | Long museum runtime without listener/timer/render-loop leakage |\n\n\n### Extracted table 13\n\n| Widget | Initial V2 status |\n\n| --- | --- |\n\n| Gallery | Required |\n\n| Image Viewer | Required |\n\n| Quiz | Required to cover reference-case interaction patterns |\n\n| Form | Framework/initial functional Widget; exact field set may evolve |\n\n| Mini-game framework | Required architectural capability; individual games are project/product additions |\n\n| Pagination | May be standalone Widget or embedded capability depending final UX; architecture supports both |\n\n| Audio Widget | May be ordinary media Element or Widget depending control requirements; must use common media/action architecture |\n