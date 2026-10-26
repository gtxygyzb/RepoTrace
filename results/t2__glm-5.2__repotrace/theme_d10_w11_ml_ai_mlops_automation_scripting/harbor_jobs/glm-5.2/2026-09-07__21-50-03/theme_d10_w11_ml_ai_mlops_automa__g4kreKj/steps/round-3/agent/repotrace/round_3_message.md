========================================================================
[RepoTrace] Repository guidance for the current request (round 3)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
  - main.go: CLI entry point
  - stages/evaluate_model.sh: implementation
  - stages/export_model.sh: export
  - stages/extract_features.sh: implementation
  - stages/retry_stage.sh: implementation
  - stages/train_model.sh: implementation
  - stages/validate_data.sh: validation
Prior components this round may touch:
  - reportPipeline
  - collectExperimentMetrics

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================