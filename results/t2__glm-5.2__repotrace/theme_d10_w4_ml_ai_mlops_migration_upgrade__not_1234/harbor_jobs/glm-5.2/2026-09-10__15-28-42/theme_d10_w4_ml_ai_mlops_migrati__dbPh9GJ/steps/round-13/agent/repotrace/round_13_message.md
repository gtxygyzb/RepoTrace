========================================================================
[RepoTrace] Repository guidance for the current request (round 13)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - commands_extra.go is depended on by 9 files (e.g. main.go, registry.go, checkpoints.go, inference.go); changing it ripples widely.
  - format.go is depended on by 8 files (e.g. commands_extra.go, registry.go, inference.go, export_import.go); changing it ripples widely.
  - main.go is depended on by 8 files (e.g. commands_extra.go, registry.go, checkpoints.go, inference.go); changing it ripples widely.
  - registry.go is depended on by 6 files (e.g. commands_extra.go, main.go, export_import.go, ensemble.go); changing it ripples widely.
  - inference.go is depended on by 4 files (e.g. commands_extra.go, main.go, validate_input.go, ensemble.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - commands_extra.go: implementation
  - format.go: implementation
  - main.go: CLI entry point
  - registry.go: implementation
  - inference.go: implementation
  - checkpoints.go: implementation
  - export_import.go: export
  - validate_input.go: validation
Prior components this round may touch:
  - loadWeights
  - writeWeights
  - saveModelMeta
  - loadModelMeta
  - cmdPrune
  - cmdExport

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================