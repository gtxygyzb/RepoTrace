========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
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
  - audit-log feature (round 3 late cutoff rendering)
  - manifest (round 5 state/audit_log/audit_digest entries)
  - state schema (round 2 pending_purchases)
  - dedup-policy feature (round 6)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================