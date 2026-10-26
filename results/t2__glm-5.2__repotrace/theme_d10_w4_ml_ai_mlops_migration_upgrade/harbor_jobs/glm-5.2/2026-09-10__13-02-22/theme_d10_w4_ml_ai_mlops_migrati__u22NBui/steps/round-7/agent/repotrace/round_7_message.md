========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/pipeline/steps.go is depended on by 6 files (e.g. internal/experiment/experiment.go, internal/api/handlers.go, internal/pipeline/engine.go, internal/api/templates.go); changing it ripples widely.
  - internal/registry/registry.go is depended on by 5 files (e.g. internal/experiment/experiment.go, internal/api/handlers.go, internal/serving/serving.go, internal/api/router.go); changing it ripples widely.
  - internal/api/handlers.go is depended on by 4 files (e.g. internal/serving/serving.go, internal/api/templates.go, internal/api/batch.go, main.go); changing it ripples widely.
  - internal/experiment/experiment.go is depended on by 4 files (e.g. internal/registry/registry.go, internal/api/handlers.go, internal/api/router.go, main.go); changing it ripples widely.
  - internal/pipeline/engine.go is depended on by 4 files (e.g. internal/api/handlers.go, internal/api/templates.go, internal/api/router.go, main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/pipeline/steps.go: implementation
  - internal/registry/registry.go: implementation
  - internal/api/handlers.go: implementation
  - internal/experiment/experiment.go: implementation
  - internal/pipeline/engine.go: implementation
  - internal/serving/serving.go: implementation
  - internal/api/templates.go: implementation
  - internal/api/batch.go: implementation
Prior components this round may touch:
  - DeleteRun (prior deletion endpoint returning only status message)
  - ValidatePipeline / Validate (prior pipeline validation lacking self-dependency check and using unquoted duplicate name format)
  - NewRouter (prior route registration must add new leaderboard, summary, reload, warmup routes)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================