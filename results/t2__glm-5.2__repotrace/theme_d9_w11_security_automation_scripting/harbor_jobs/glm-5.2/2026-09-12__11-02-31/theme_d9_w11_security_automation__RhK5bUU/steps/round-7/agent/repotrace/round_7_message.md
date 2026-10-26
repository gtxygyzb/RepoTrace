========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - main.go is depended on by 9 files (e.g. enrich.go, correlate.go, timeline.go, snapshot.go); changing it ripples widely.
  - event.go is depended on by 8 files (e.g. threats.go, enrich.go, timeline.go, snapshot.go); changing it ripples widely.
  - enrich.go is depended on by 5 files (e.g. main.go, correlate.go, timeline.go, snapshot.go); changing it ripples widely.
  - threats.go is depended on by 5 files (e.g. enrich.go, timeline.go, summarize.go, analyze.go); changing it ripples widely.
  - correlate.go is depended on by 2 files (e.g. main.go, snapshot.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - main.go: CLI entry point
  - event.go: implementation
  - enrich.go: implementation
  - threats.go: implementation
  - correlate.go: implementation
  - timeline.go: implementation
  - alert.go: implementation
  - analyze.go: implementation
New in this round (to be created):
  - aggregate.go
Prior components this round may touch:
  - timeline.go (timelineEscalationIndex from round 4)
  - main.go (subcommand registration)
  - snapshot.go (output consumed as input by aggregate)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================