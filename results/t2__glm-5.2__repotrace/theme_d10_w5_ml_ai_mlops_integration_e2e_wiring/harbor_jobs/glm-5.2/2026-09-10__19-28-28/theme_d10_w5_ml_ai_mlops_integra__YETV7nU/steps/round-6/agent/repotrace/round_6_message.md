========================================================================
[RepoTrace] Repository guidance for the current request (round 6)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - config.go is depended on by 10 files (e.g. evaluate.go, pipeline.go, cache.go, train.go); changing it ripples widely.
  - data.go is depended on by 7 files (e.g. config.go, evaluate.go, pipeline.go, train.go); changing it ripples widely.
  - pipeline.go is depended on by 4 files (e.g. evaluate.go, cv.go, plan.go, main.go); changing it ripples widely.
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
  - train.go: implementation
New in this round (to be created):
  - history.go
  - diff.go
Prior components this round may touch:
  - cmdRun
  - Run
  - RunCV
  - parseRunArgs
  - main
  - loadConfig

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================