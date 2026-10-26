========================================================================
[RepoTrace] Repository guidance for the current request (round 1)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/types/types.go is depended on by 2 files (e.g. internal/logparser/logparser.go, internal/checkpoint/parser.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/types/types.go: implementation
  - cmd/mlforge/main.go: CLI entry point
  - internal/checkpoint/parser.go: implementation
  - internal/logparser/logparser.go: implementation

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================