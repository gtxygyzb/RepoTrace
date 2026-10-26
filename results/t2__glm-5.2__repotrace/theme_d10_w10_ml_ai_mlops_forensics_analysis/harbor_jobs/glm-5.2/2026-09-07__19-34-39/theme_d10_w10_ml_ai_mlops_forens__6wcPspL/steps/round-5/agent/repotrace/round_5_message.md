========================================================================
[RepoTrace] Repository guidance for the current request (round 5)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/types/types.go is depended on by 7 files (e.g. internal/checkpoint/parser.go, internal/forensics/forensics.go, internal/forensics/detect.go, internal/logparser/logparser.go); changing it ripples widely.
  - internal/checkpoint/parser.go is depended on by 5 files (e.g. internal/forensics/forensics.go, internal/forensics/detect.go, internal/forensics/lineage.go, internal/forensics/diff.go); changing it ripples widely.
  - internal/forensics/forensics.go is depended on by 5 files (e.g. internal/forensics/detect.go, internal/forensics/lineage.go, internal/forensics/query.go, internal/forensics/report.go); changing it ripples widely.
  - internal/forensics/detect.go is depended on by 3 files (e.g. internal/forensics/lineage.go, internal/forensics/report.go, cmd/mlforge/main.go); changing it ripples widely.
  - internal/forensics/lineage.go is depended on by 2 files (e.g. internal/forensics/report.go, cmd/mlforge/main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/types/types.go: implementation
  - internal/checkpoint/parser.go: implementation
  - internal/forensics/forensics.go: implementation
  - internal/forensics/detect.go: implementation
  - internal/forensics/lineage.go: implementation
  - internal/forensics/diff.go: implementation
  - internal/forensics/query.go: implementation
  - internal/forensics/report.go: report generation
New in this round (to be created):
  - /app/docs/analysis_rules.md
Prior components this round may touch:
  - round 1 query wiring in cmd/mlforge/main.go (BuildQuery invocation and error reporting)
  - existing parseQuery/parseCondition/tokenizeQuery implementation in internal/forensics/query.go

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================