========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/registry/registry.go is depended on by 5 files (e.g. internal/experiment/experiment.go, internal/api/handlers.go, internal/serving/serving.go, internal/api/router.go); changing it ripples widely.
  - internal/experiment/experiment.go is depended on by 4 files (e.g. internal/registry/registry.go, internal/api/handlers.go, internal/api/router.go, main.go); changing it ripples widely.
  - internal/pipeline/steps.go is depended on by 4 files (e.g. internal/experiment/experiment.go, internal/api/handlers.go, internal/api/router.go, main.go); changing it ripples widely.
  - internal/pipeline/engine.go is depended on by 3 files (e.g. internal/api/handlers.go, internal/api/router.go, main.go); changing it ripples widely.
  - internal/serving/serving.go is depended on by 3 files (e.g. internal/api/handlers.go, internal/api/router.go, main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/registry/registry.go: implementation
  - internal/experiment/experiment.go: implementation
  - internal/pipeline/steps.go: implementation
  - internal/pipeline/engine.go: implementation
  - internal/serving/serving.go: implementation
  - internal/api/handlers.go: implementation
  - internal/api/router.go: implementation
  - main.go: CLI entry point
Prior components this round may touch:
  - ExecuteTransform (normalize zero-range behavior change)
  - ExecuteAggregate (new 'range' operation)
  - AggregateMetric (run_ids field added to response)
  - ExecutePipeline / NewEngine / Execute (template execution reuses engine; variable context system hinted)
  - NewRouter (new routes for version compare, templates, batch inference)
  - Infer / serving subsystem (batch inference wraps individual inference)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================