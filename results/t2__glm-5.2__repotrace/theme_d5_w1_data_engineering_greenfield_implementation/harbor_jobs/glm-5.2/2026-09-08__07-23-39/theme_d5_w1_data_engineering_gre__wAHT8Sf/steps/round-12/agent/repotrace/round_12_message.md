========================================================================
[RepoTrace] Repository guidance for the current request (round 12)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - helpers.go is depended on by 5 files (e.g. main.go, schema.go, manifest.go, sharding_report.go); changing it ripples widely.
  - main.go is depended on by 2 files (e.g. schema.go, cli.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - helpers.go: implementation
  - main.go: CLI entry point
  - manifest.go: implementation
  - schema.go: implementation
  - sharding_report.go: report generation
  - cli.go: implementation
  - types.go: implementation
New in this round (to be created):
  - run_provenance.go
Prior components this round may touch:
  - cli.go parseArgs/run flag parsing
  - main.go ingest/shard enumeration
  - types.go sidecar type definitions
  - helpers.go parentDirExists/atomicWriteFile/sha256Hex usage

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================