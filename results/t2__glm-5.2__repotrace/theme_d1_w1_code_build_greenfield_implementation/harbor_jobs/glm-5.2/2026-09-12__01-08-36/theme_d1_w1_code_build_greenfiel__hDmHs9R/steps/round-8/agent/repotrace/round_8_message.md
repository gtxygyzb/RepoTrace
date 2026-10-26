========================================================================
[RepoTrace] Repository guidance for the current request (round 8)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - cmd/jobforge/spec.go is depended on by 7 files (e.g. cmd/jobforge/main.go, cmd/jobforge/hash.go, cmd/jobforge/run.go, cmd/jobforge/schedule.go); changing it ripples widely.
  - cmd/jobforge/main.go is depended on by 4 files (e.g. cmd/jobforge/hash.go, cmd/jobforge/schedule.go, cmd/jobforge/graph.go, cmd/jobforge/critical.go); changing it ripples widely.
  - cmd/jobforge/hash.go is depended on by 2 files (e.g. cmd/jobforge/main.go, cmd/jobforge/diff.go); changing it ripples widely.
  - cmd/jobforge/run.go is depended on by 2 files (e.g. cmd/jobforge/main.go, cmd/jobforge/schedule.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - cmd/jobforge/spec.go: implementation
  - cmd/jobforge/main.go: CLI entry point
  - cmd/jobforge/hash.go: implementation
  - cmd/jobforge/run.go: experiment execution
  - cmd/jobforge/critical.go: implementation
  - cmd/jobforge/cycle.go: implementation
  - cmd/jobforge/diff.go: implementation
  - cmd/jobforge/graph.go: implementation
New in this round (to be created):
  - cmd/jobforge/ancestors.go
Prior components this round may touch:
  - plan --format text output (breaking change to prior text rendering)
  - main dispatch table (new ancestors subcommand registration)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================