========================================================================
[RepoTrace] Repository guidance for the current request (round 8)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - event.go is depended on by 9 files (e.g. threats.go, enrich.go, snapshot.go, timeline.go); changing it ripples widely.
  - main.go is depended on by 9 files (e.g. enrich.go, snapshot.go, correlate.go, timeline.go); changing it ripples widely.
  - enrich.go is depended on by 5 files (e.g. main.go, snapshot.go, correlate.go, timeline.go); changing it ripples widely.
  - threats.go is depended on by 5 files (e.g. enrich.go, timeline.go, summarize.go, analyze.go); changing it ripples widely.
  - correlate.go is depended on by 2 files (e.g. main.go, snapshot.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - event.go: implementation
  - main.go: CLI entry point
  - enrich.go: implementation
  - threats.go: implementation
  - correlate.go: implementation
  - snapshot.go: implementation
  - timeline.go: implementation
  - aggregate.go: implementation
New in this round (to be created):
  - prioritize.go

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================