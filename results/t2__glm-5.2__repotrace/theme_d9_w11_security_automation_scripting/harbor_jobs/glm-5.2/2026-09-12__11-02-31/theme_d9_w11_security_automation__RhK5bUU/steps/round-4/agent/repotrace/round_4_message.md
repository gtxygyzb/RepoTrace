========================================================================
[RepoTrace] Repository guidance for the current request (round 4)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - main.go is depended on by 6 files (e.g. enrich.go, summarize.go, respond.go, analyze.go); changing it ripples widely.
  - event.go is depended on by 5 files (e.g. threats.go, enrich.go, summarize.go, analyze.go); changing it ripples widely.
  - threats.go is depended on by 4 files (e.g. enrich.go, summarize.go, analyze.go, chain.go); changing it ripples widely.
  - enrich.go is depended on by 2 files (e.g. main.go, correlate.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - main.go: CLI entry point
  - event.go: implementation
  - threats.go: implementation
  - enrich.go: implementation
  - analyze.go: implementation
  - chain.go: implementation
  - correlate.go: implementation
  - filter.go: implementation
New in this round (to be created):
  - timeline.go
Prior components this round may touch:
  - main.go

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================