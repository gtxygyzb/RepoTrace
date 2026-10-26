========================================================================
[RepoTrace] Repository guidance for the current request (round 14)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - csvio.go is depended on by 6 files (e.g. jsonutil.go, compare.go, profile.go, pipeline.go); changing it ripples widely.
  - compare.go is depended on by 2 files (e.g. pipeline.go, main.go); changing it ripples widely.
  - jsonutil.go is depended on by 2 files (e.g. compare.go, profile.go); changing it ripples widely.
  - profile.go is depended on by 2 files (e.g. pipeline.go, main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - csvio.go: implementation
  - compare.go: comparison
  - jsonutil.go: implementation
  - profile.go: implementation
  - pipeline.go: pipeline logic
  - stats.go: implementation
  - expr.go: implementation
  - main.go: CLI entry point
New in this round (to be created):
  - changelog.go
  - lineage.go
Prior components this round may touch:
  - main.go command dispatch
  - pipeline.go transform/step dispatch
  - lineage.go step recognition

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================