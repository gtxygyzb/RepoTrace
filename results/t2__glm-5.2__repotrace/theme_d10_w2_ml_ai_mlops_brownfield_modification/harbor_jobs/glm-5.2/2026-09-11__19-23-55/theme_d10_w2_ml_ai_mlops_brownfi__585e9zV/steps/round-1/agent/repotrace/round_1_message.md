========================================================================
[RepoTrace] Repository guidance for the current request (round 1)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - store.go is depended on by 3 files (e.g. tracker.go, registry.go, main.go); changing it ripples widely.
  - models.go is depended on by 2 files (e.g. store.go, registry.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - store.go: implementation
  - models.go: implementation
  - registry.go: implementation
  - tracker.go: implementation
  - main.go: CLI entry point
New in this round (to be created):
  - pipeline.go
Prior components this round may touch:
  - main.go (CLI dispatch must add pipeline subcommand)
  - tracker.go (Create/LogMetric/Complete used by train steps)
  - store.go (experiment persistence path may be exercised by pipeline-created experiments)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================