========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/mlck/checkpoint.go is depended on by 7 files (e.g. internal/compare/compare.go, internal/merge/merge.go, internal/drift/drift.go, internal/app/app.go); changing it ripples widely.
  - internal/compare/compare.go is depended on by 4 files (e.g. internal/merge/merge.go, internal/drift/drift.go, internal/app/app.go, internal/report/report.go); changing it ripples widely.
  - internal/drift/drift.go is depended on by 3 files (e.g. internal/compare/compare.go, internal/merge/merge.go, internal/app/app.go); changing it ripples widely.
  - internal/merge/merge.go is depended on by 3 files (e.g. internal/compare/compare.go, internal/drift/drift.go, internal/app/app.go); changing it ripples widely.
  - internal/app/app.go is depended on by 2 files (e.g. cmd/repro-verify/main.go, main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/mlck/checkpoint.go: implementation
  - internal/compare/compare.go: comparison
  - internal/drift/drift.go: implementation
  - internal/merge/merge.go: implementation
  - internal/app/app.go: implementation
  - internal/lineage/lineage.go: implementation
  - internal/manifest/manifest.go: implementation
  - internal/report/report.go: report generation
Prior components this round may touch:
  - internal/manifest/manifest.go TOML parser (parseTOML, parseTOMLValue, splitArrayElements) and manifest validation behavior
  - internal/app/app.go command dispatch and error reporting (Run, runCompareOutputs, runMergeCheckpoints, runDriftAnalysis)
  - compare-outputs, merge-checkpoints, and drift-analysis plain-stderr error output
  - verify-checkpoint and validate-manifest command-specific invalid-content JSON payloads (must be preserved)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================