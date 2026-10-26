========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - cmd/jobforge/spec.go is depended on by 2 files (e.g. cmd/jobforge/run.go, cmd/jobforge/main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - cmd/jobforge/spec.go: implementation
  - cmd/jobforge/cycle.go: implementation
  - cmd/jobforge/run.go: experiment execution
  - cmd/jobforge/main.go: CLI entry point
Prior components this round may touch:
  - main CLI dispatch and argument parsing in cmd/jobforge/main.go
  - runPlan and runRun subcommand handlers
  - shared validation pipeline: loadSpec, detectCycle, findCyclePath, computeLevels, printValidationError, and existing error codes

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================