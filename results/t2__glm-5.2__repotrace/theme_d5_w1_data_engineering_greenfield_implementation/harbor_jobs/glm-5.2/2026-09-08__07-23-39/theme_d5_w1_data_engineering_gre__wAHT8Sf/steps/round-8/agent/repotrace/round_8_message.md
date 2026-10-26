========================================================================
[RepoTrace] Repository guidance for the current request (round 8)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - helpers.go is depended on by 3 files (e.g. main.go, manifest.go, cli.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - helpers.go: implementation
  - main.go: CLI entry point
  - manifest.go: implementation
  - cli.go: implementation
  - types.go: implementation
Prior components this round may touch:
  - parseArgs (rounds 5/6/7)
  - run / ingest main flow
  - buildManifest / writeManifest pattern (round 5)
  - summary --output writing logic

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================