# Validation Engineering Requirements

- **ENG-VAL-010 MUST**: Use one Project Validation Engine across Open, Save, Build, Collect and manual validation contexts.
- **ENG-VAL-011 MUST**: Represent findings as structured Problems with severity Error/Warning/Info and target/context data.
- **ENG-VAL-012 MUST**: Separate structural/schema, referential/semantic and resource/build validation concerns.
- **ENG-VAL-013 MUST**: Error block Build; Warning and Info do not.
- **ENG-VAL-014 MUST**: Validation report problems without silently modifying project data.
- **ENG-VAL-015 MUST**: Run fast/debounced validation after relevant edits and full validation for Open/manual/Collect/Build as appropriate.
- **ENG-VAL-016 MUST**: Detect broken entity references and invalid ownership/cycles where the data model forbids them.
- **ENG-VAL-017 MUST**: Detect missing runtime-required assets during full Build validation.
- **ENG-VAL-018 MUST**: Validate Widget props/dependencies through Widget Contract.
- **ENG-VAL-019 MUST**: Validate Component dependency cycles and pinned revision references.
- **ENG-VAL-020 MUST**: Validate Screen initialPageId and other required runtime entry points.
- **ENG-VAL-021 MUST**: Quick Fix, if added, remain explicit user action and MUST NOT be a prerequisite for validation correctness.
