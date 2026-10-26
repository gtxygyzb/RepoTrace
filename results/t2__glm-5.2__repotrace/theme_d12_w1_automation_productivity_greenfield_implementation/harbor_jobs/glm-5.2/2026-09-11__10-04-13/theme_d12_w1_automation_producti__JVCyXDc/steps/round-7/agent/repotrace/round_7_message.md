========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
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
  - R1 --run-id validator and default run-id generation in main
  - R1 FLOWR_RUN_ID builtin environment injection/interpolation
  - F17 --resume run-id distinctness check
  - F25 flowr diff run-id argument validation and error precedence
  - flowr replay prior-run-id validation
  - R1 parseStep/validateStep for new step tags

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================