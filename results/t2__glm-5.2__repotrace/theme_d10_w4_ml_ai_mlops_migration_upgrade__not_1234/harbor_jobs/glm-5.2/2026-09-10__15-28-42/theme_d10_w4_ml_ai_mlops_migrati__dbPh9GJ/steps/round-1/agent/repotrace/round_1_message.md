========================================================================
[RepoTrace] Repository guidance for the current request (round 1)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - format.go is depended on by 3 files (e.g. registry.go, commands.go, inference.go); changing it ripples widely.
  - registry.go is depended on by 3 files (e.g. main.go, commands.go, inference.go); changing it ripples widely.
  - main.go is depended on by 2 files (e.g. commands.go, inference.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - format.go: implementation
  - registry.go: implementation
  - main.go: CLI entry point
  - commands.go: implementation
  - inference.go: implementation

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================