========================================================================
[RepoTrace] Repository guidance for the current request (round 13)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - helpers.go is depended on by 6 files (e.g. main.go, schema.go, run_provenance.go, manifest.go); changing it ripples widely.
  - main.go is depended on by 2 files (e.g. schema.go, cli.go); changing it ripples widely.
  - schema.go is depended on by 2 files (e.g. run_provenance.go, cli.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - helpers.go: implementation
  - main.go: CLI entry point
  - schema.go: implementation
  - manifest.go: implementation
  - run_provenance.go: experiment execution
  - sharding_report.go: report generation
  - cli.go: implementation
  - types.go: implementation
Prior components this round may touch:
  - round 11 sharding-report first_ts/last_ts corpus (observed must equal it)
  - round 12 run-provenance flags enumeration (new key summary-time-range-policy)
  - default summary.time_range block in --output

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================