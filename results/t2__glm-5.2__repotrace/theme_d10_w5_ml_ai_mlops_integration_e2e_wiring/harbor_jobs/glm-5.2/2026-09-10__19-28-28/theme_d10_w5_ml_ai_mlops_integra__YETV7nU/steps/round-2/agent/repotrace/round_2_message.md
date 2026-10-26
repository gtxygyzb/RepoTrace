========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - config.go is depended on by 7 files (e.g. evaluate.go, pipeline.go, train.go, register.go); changing it ripples widely.
  - data.go is depended on by 6 files (e.g. config.go, evaluate.go, pipeline.go, train.go); changing it ripples widely.
  - evaluate.go is depended on by 2 files (e.g. pipeline.go, register.go); changing it ripples widely.
  - pipeline.go is depended on by 2 files (e.g. evaluate.go, main.go); changing it ripples widely.
  - register.go is depended on by 2 files (e.g. pipeline.go, main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - config.go: implementation
  - data.go: implementation
  - evaluate.go: implementation
  - pipeline.go: pipeline logic
  - register.go: implementation
  - train.go: implementation
  - split.go: implementation
  - transform.go: implementation
Prior components this round may touch:
  - Run
  - executeStage
  - saveArtifacts
  - loadArtifacts
  - artifactID
  - cmdRun

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================