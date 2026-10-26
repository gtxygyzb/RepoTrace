========================================================================
[RepoTrace] Repository guidance for the current request (round 6)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - cmd/flowr/parse.go is depended on by 2 files (e.g. cmd/flowr/validate.go, cmd/flowr/expand.go); changing it ripples widely.
  - cmd/flowr/util.go is depended on by 2 files (e.g. cmd/flowr/interpolate.go, cmd/flowr/expand.go); changing it ripples widely.
  - cmd/flowr/validate.go is depended on by 2 files (e.g. cmd/flowr/interpolate.go, cmd/flowr/expand.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - cmd/flowr/parse.go: implementation
  - cmd/flowr/util.go: implementation
  - cmd/flowr/validate.go: validation
  - cmd/flowr/interpolate.go: implementation
  - cmd/flowr/expand.go: implementation
  - cmd/flowr/main.go: CLI entry point
  - cmd/flowr/types.go: implementation
Prior components this round may touch:
  - validateWorkflow (round 1) — must validate new top-level locks block.
  - validateStep (round 1) — must validate per-step lock/locks fields and mutual exclusion.
  - parseStep (round 1) — must parse lock/locks fields.
  - parseWorkflow (round 1) — must parse top-level locks block.
  - scheduler in main.go (rounds 1-5) — must integrate lock acquisition/release, atomicity, sorting, and deadlock detection without regressing max-parallel, resource reservations, or lexicographic tie-breaking.
  - expandMatrix/expandForeach (rounds 1,5) — cells must carry lock requests using expanded cell names as holder identity.

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================