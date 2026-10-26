========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - commands_extra.go is depended on by 7 files (e.g. main.go, registry.go, inference.go, checkpoints.go); changing it ripples widely.
  - format.go is depended on by 6 files (e.g. commands_extra.go, registry.go, inference.go, migration.go); changing it ripples widely.
  - main.go is depended on by 6 files (e.g. commands_extra.go, registry.go, inference.go, checkpoints.go); changing it ripples widely.
  - registry.go is depended on by 5 files (e.g. main.go, commands_extra.go, migration.go, export_import.go); changing it ripples widely.
  - checkpoints.go is depended on by 2 files (e.g. main.go, registry.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - commands_extra.go: implementation
  - format.go: implementation
  - main.go: CLI entry point
  - registry.go: implementation
  - checkpoints.go: implementation
  - inference.go: implementation
  - commands.go: implementation
  - export_import.go: export
New in this round (to be created):
  - ensemble.go
Prior components this round may touch:
  - main
  - parseFlags
  - printUsage

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================