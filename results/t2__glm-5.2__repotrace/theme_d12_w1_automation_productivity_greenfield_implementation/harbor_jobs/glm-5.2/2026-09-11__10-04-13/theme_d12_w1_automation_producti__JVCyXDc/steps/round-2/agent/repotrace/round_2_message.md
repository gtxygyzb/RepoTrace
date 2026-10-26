========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
  - cmd/flowr/main.go: CLI entry point
New in this round (to be created):
  - go.mod
Prior components this round may touch:
  - main
  - parseWorkflow
  - runWorkflow/executeStep
  - DAG scheduler
  - report.json generation
  - events log

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================