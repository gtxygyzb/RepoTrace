========================================================================
[RepoTrace] Repository guidance for the current request (round 4)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - cmd/jobforge/spec.go is depended on by 3 files (e.g. cmd/jobforge/main.go, cmd/jobforge/graph.go, cmd/jobforge/run.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - cmd/jobforge/spec.go: implementation
  - cmd/jobforge/cycle.go: implementation
  - cmd/jobforge/graph.go: implementation
  - cmd/jobforge/main.go: CLI entry point
  - cmd/jobforge/run.go: experiment execution
New in this round (to be created):
  - cmd/jobforge/hash.go
Prior components this round may touch:
  - renderDot (DOT attribute separator changed from comma to space)
  - main (subcommand dispatch must add hash routing)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================