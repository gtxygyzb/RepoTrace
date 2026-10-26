========================================================================
[RepoTrace] Repository guidance for the current request (round 3)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - commands_extra.go is depended on by 5 files (e.g. main.go, registry.go, inference.go, migration.go); changing it ripples widely.
  - format.go is depended on by 5 files (e.g. commands_extra.go, registry.go, inference.go, migration.go); changing it ripples widely.
  - main.go is depended on by 4 files (e.g. commands_extra.go, inference.go, migration.go, commands.go); changing it ripples widely.
  - registry.go is depended on by 4 files (e.g. commands_extra.go, main.go, migration.go, commands.go); changing it ripples widely.
  - inference.go is depended on by 2 files (e.g. commands_extra.go, main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - commands_extra.go: implementation
  - format.go: implementation
  - main.go: CLI entry point
  - registry.go: implementation
  - inference.go: implementation
  - commands.go: implementation
  - migration.go: implementation
Prior components this round may touch:
  - main.go main/parseFlags/printUsage command dispatch and usage from prior rounds
  - commands.go cmdExport behavior may be replaced or extended to emit JSON
  - format.go loadModelMeta/loadWeights/writeWeights/saveModelMeta/loadPipelineConfig and activation helpers must preserve v1/v2 format and pipeline fidelity
  - registry.go loadRegistry/saveRegistry/findEntry are used for import/clone registration and conflict checks
  - commands_extra.go resolveModel/modelDirExists/loadModelArtifacts are used for source model resolution and artifact loading
  - inference.go runInference/preprocess/postprocess must remain stable for export/import round-trip fidelity

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================