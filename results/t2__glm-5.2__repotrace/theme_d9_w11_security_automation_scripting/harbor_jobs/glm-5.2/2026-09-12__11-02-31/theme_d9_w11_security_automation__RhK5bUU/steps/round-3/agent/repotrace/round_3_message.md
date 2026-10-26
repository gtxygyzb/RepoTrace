========================================================================
[RepoTrace] Repository guidance for the current request (round 3)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - event.go is depended on by 5 files (e.g. threats.go, enrich.go, summarize.go, analyze.go); changing it ripples widely.
  - main.go is depended on by 5 files (e.g. enrich.go, summarize.go, respond.go, analyze.go); changing it ripples widely.
  - threats.go is depended on by 4 files (e.g. enrich.go, summarize.go, analyze.go, chain.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - event.go: implementation
  - main.go: CLI entry point
  - threats.go: implementation
  - analyze.go: implementation
  - chain.go: implementation
  - enrich.go: implementation
  - filter.go: implementation
  - respond.go: implementation
New in this round (to be created):
  - correlate.go
Prior components this round may touch:
  - runEnrich
  - computeIOCMatches
  - processIOC
  - enrichThreat
  - main (CLI dispatch)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================