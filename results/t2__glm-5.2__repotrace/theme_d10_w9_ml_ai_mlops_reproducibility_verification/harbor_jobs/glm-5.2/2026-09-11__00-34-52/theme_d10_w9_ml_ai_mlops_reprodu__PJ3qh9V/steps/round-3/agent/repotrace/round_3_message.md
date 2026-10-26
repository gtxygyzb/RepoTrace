========================================================================
[RepoTrace] Repository guidance for the current request (round 3)
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
  - Generate (internal/report/report.go) - comparison and lineage sections from round 1
  - quickLineageCheck (internal/report/report.go) - simplified lineage check to be removed/replaced
  - Analyze (internal/drift/drift.go) - non-deterministic map iteration from round 1
  - runGenerateReport (internal/app/app.go) - report handler from rounds 1-2
  - runDriftAnalysis (internal/app/app.go) - drift handler from rounds 1-2

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================