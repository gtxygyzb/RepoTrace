========================================================================
[RepoTrace] Repository guidance for the current request (round 4)
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
  - parseWorkflow (parse.go) — must parse top-level secrets block and per-step artifacts
  - validateWorkflow / validateStep (validate.go) — must validate secrets and artifacts, and reject undeclared ${secret.NAME} references
  - interpolateFirstPass (interpolate.go) — must resolve ${secret.NAME} as a separate namespace in the first pass, without fall-through
  - resolveStepOutputs / outputValueToString (interpolate.go) — output.json read-back must apply textual redaction before downstream ${step.NAME.output.KEY} resolution
  - computeCacheKey (main.go, R2) — must hash the redacted form of secret values
  - expandMatrix / expandForeach (expand.go) — must carry artifacts onto expanded cells

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================