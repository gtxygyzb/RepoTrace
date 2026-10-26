========================================================================
[RepoTrace] Repository guidance for the current request (round 5)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - cmd/flowr/parse.go is depended on by 2 files (e.g. cmd/flowr/validate.go, cmd/flowr/expand.go); changing it ripples widely.
  - cmd/flowr/util.go is depended on by 2 files (e.g. cmd/flowr/interpolate.go, cmd/flowr/expand.go); changing it ripples widely.
  - cmd/flowr/validate.go is depended on by 2 files (e.g. cmd/flowr/interpolate.go, cmd/flowr/expand.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - cmd/flowr/parse.go: implementation
  - cmd/flowr/util.go: implementation
  - cmd/flowr/validate.go: validation
  - cmd/flowr/interpolate.go: implementation
  - cmd/flowr/expand.go: implementation
  - cmd/flowr/main.go: CLI entry point
  - cmd/flowr/types.go: implementation
Prior components this round may touch:
  - R1 graceful cancellation (SIGTERM/500ms/SIGKILL) now also drives per-step timeout path
  - R1 step scheduling/run loop must enforce per-attempt deadline timer
  - R1 report.json step record gains timed_out field and 'timeout' error string
  - R1 report.json top-level gains timeouts_summary
  - R1 events.ndjson gains step_timeout record kind
  - R1 meta.json per-step gains timed_out field

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================