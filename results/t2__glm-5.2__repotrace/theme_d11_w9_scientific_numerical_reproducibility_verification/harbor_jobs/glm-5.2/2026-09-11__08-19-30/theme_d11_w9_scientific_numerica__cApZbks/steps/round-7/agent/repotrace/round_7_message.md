========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - engine/engine.go is depended on by 7 files (e.g. engine/montecarlo.go, engine/stats.go, engine/ode.go, engine/matrix.go); changing it ripples widely.
  - engine/matrix.go is depended on by 4 files (e.g. engine/engine.go, storage/storage.go, config/config.go, main.go); changing it ripples widely.
  - engine/montecarlo.go is depended on by 4 files (e.g. engine/engine.go, storage/storage.go, config/config.go, main.go); changing it ripples widely.
  - engine/ode.go is depended on by 4 files (e.g. engine/engine.go, storage/storage.go, config/config.go, main.go); changing it ripples widely.
  - engine/stats.go is depended on by 4 files (e.g. engine/engine.go, storage/storage.go, config/config.go, main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - engine/engine.go: implementation
  - engine/matrix.go: implementation
  - engine/montecarlo.go: implementation
  - engine/ode.go: implementation
  - engine/stats.go: implementation
  - storage/storage.go: implementation
  - compare/compare.go: comparison
  - config/config.go: implementation
Prior components this round may touch:
  - cmdAudit
  - cmdAuditAll
  - auditStoredResult
  - cmdExport

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================