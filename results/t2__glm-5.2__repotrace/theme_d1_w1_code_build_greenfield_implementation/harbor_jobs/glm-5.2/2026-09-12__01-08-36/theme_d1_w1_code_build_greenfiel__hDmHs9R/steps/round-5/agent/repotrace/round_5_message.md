========================================================================
[RepoTrace] Repository guidance for the current request (round 5)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - cmd/jobforge/spec.go is depended on by 4 files (e.g. cmd/jobforge/main.go, cmd/jobforge/graph.go, cmd/jobforge/run.go, cmd/jobforge/hash.go); changing it ripples widely.
  - cmd/jobforge/main.go is depended on by 2 files (e.g. cmd/jobforge/hash.go, cmd/jobforge/graph.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - cmd/jobforge/spec.go: implementation
  - cmd/jobforge/main.go: CLI entry point
  - cmd/jobforge/cycle.go: implementation
  - cmd/jobforge/graph.go: implementation
  - cmd/jobforge/hash.go: implementation
  - cmd/jobforge/run.go: experiment execution
New in this round (to be created):
  - cmd/jobforge/diff.go
Prior components this round may touch:
  - main
  - runValidate
  - loadSpec
  - listJobs walk order
  - runHash canonical form

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================