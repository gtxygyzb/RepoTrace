========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - store.go is depended on by 4 files (e.g. tracker.go, pipeline.go, registry.go, main.go); changing it ripples widely.
  - models.go is depended on by 2 files (e.g. store.go, registry.go); changing it ripples widely.
  - tracker.go is depended on by 2 files (e.g. pipeline.go, main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - store.go: implementation
  - models.go: implementation
  - tracker.go: implementation
  - pipeline.go: pipeline logic
  - registry.go: implementation
  - main.go: CLI entry point
Prior components this round may touch:
  - handlePipeline
  - executeStep
  - executeSteps
  - runPipeline
  - substituteParams
  - resolveParam

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================