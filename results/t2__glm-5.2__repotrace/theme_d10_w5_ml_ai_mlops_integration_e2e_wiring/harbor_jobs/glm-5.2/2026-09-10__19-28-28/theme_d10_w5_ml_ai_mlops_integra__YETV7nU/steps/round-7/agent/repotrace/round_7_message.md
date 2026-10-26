========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - config.go is depended on by 11 files (e.g. main.go, pipeline.go, evaluate.go, register.go); changing it ripples widely.
  - data.go is depended on by 7 files (e.g. config.go, pipeline.go, evaluate.go, train.go); changing it ripples widely.
  - pipeline.go is depended on by 4 files (e.g. main.go, evaluate.go, cv.go, plan.go); changing it ripples widely.
  - cache.go is depended on by 3 files (e.g. pipeline.go, cv.go, plan.go); changing it ripples widely.
  - evaluate.go is depended on by 3 files (e.g. pipeline.go, register.go, cv.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - config.go: implementation
  - data.go: implementation
  - pipeline.go: pipeline logic
  - cache.go: implementation
  - evaluate.go: implementation
  - register.go: implementation
  - cv.go: implementation
  - main.go: CLI entry point
Prior components this round may touch:
  - computeCacheKey (round 2 caching)
  - Run continue-on-failure cascade logic (round 4 stage skipping)
  - buildRunRecord/saveRunRecord (round 6 history)
  - cmdDiff/diffConfigs (round 6 diff)
  - Validate (round 1 config validation)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================