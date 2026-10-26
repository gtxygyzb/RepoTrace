========================================================================
[RepoTrace] Repository guidance for the current request (round 10)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - helpers.go is depended on by 4 files (e.g. main.go, schema.go, manifest.go, cli.go); changing it ripples widely.
  - main.go is depended on by 2 files (e.g. schema.go, cli.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - helpers.go: implementation
  - main.go: CLI entry point
  - manifest.go: implementation
  - schema.go: implementation
  - cli.go: implementation
  - types.go: implementation
Prior components this round may touch:
  - ingest
  - parseArgs
  - run
  - loadState
  - sortedCarriedSessions
  - sortedOpenSessions

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================