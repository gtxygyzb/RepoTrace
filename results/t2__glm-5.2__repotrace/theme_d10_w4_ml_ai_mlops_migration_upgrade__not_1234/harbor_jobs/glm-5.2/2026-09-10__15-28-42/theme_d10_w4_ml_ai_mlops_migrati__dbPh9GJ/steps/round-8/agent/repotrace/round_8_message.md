========================================================================
[RepoTrace] Repository guidance for the current request (round 8)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - commands_extra.go is depended on by 8 files (e.g. main.go, registry.go, inference.go, checkpoints.go); changing it ripples widely.
  - format.go is depended on by 7 files (e.g. commands_extra.go, registry.go, inference.go, ensemble.go); changing it ripples widely.
  - main.go is depended on by 7 files (e.g. commands_extra.go, registry.go, inference.go, checkpoints.go); changing it ripples widely.
  - registry.go is depended on by 6 files (e.g. main.go, commands_extra.go, ensemble.go, migration.go); changing it ripples widely.
  - inference.go is depended on by 3 files (e.g. main.go, commands_extra.go, ensemble.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - commands_extra.go: implementation
  - format.go: implementation
  - main.go: CLI entry point
  - registry.go: implementation
  - inference.go: implementation
  - checkpoints.go: implementation
  - commands.go: implementation
  - ensemble.go: implementation
Prior components this round may touch:
  - cmdEnsembleCreate (round 7) — gains --weights parsing and validation
  - saveEnsembleConfig/loadEnsembleConfig (round 7) — config struct gains weights and created fields
  - combineEnsembleOutputs (round 7) — average strategy now applies weighted averaging
  - parseFlags, printUsage, main (round 7) — must dispatch new 'ensemble info' subcommand and accept --weights

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================