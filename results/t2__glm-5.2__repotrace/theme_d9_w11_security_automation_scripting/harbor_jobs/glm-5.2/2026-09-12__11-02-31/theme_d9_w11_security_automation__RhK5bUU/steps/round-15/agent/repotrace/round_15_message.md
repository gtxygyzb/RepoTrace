========================================================================
[RepoTrace] Repository guidance for the current request (round 15)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - main.go is depended on by 14 files (e.g. enrich.go, anomaly.go, timeline.go, snapshot.go); changing it ripples widely.
  - event.go is depended on by 12 files (e.g. threats.go, enrich.go, timeline.go, snapshot.go); changing it ripples widely.
  - enrich.go is depended on by 7 files (e.g. main.go, timeline.go, snapshot.go, prioritize.go); changing it ripples widely.
  - threats.go is depended on by 5 files (e.g. enrich.go, timeline.go, summarize.go, analyze.go); changing it ripples widely.
  - anomaly.go is depended on by 3 files (e.g. main.go, forecast.go, compliance.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - main.go: CLI entry point
  - event.go: implementation
  - enrich.go: implementation
  - threats.go: implementation
  - anomaly.go: implementation
  - timeline.go: implementation
  - correlate.go: implementation
  - prioritize.go: implementation
New in this round (to be created):
  - rate.go
Prior components this round may touch:
  - forecast.go
  - main.go

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================