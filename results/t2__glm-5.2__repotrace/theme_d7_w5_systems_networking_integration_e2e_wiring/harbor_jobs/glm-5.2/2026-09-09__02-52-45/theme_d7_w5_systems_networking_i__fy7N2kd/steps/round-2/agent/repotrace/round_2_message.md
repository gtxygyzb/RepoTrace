========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/circuit/breaker.go is depended on by 6 files (e.g. internal/state/state.go, internal/state/routing.go, internal/state/json.go, internal/ipc/server.go); changing it ripples widely.
  - internal/state/state.go is depended on by 6 files (e.g. internal/state/routing.go, internal/state/json.go, internal/ipc/server.go, internal/router/router.go); changing it ripples widely.
  - internal/state/routing.go is depended on by 5 files (e.g. internal/state/json.go, internal/ipc/server.go, internal/router/router.go, internal/health/monitor.go); changing it ripples widely.
  - internal/config/config.go is depended on by 4 files (e.g. internal/state/state.go, internal/ipc/server.go, internal/health/monitor.go, cmd/meshd/main.go); changing it ripples widely.
  - internal/state/json.go is depended on by 4 files (e.g. internal/ipc/server.go, internal/router/router.go, internal/health/monitor.go, cmd/meshd/main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/circuit/breaker.go: implementation
  - internal/state/state.go: state management
  - internal/state/routing.go: implementation
  - internal/config/config.go: implementation
  - internal/state/json.go: implementation
  - internal/stats/stats.go: implementation
  - internal/ipc/server.go: implementation
  - internal/router/router.go: implementation
Prior components this round may touch:
  - internal/config/config.go (ServiceConfig struct)
  - internal/state/state.go (ApplyConfig, applyConfigLocked, newServiceState)
  - internal/state/routing.go (SelectEndpoint — rate limit gate before selection)
  - internal/router/router.go (forward, startService — retry loop and rate limit hook)
  - internal/ipc/server.go (dispatch, handleLine — new commands)
  - internal/stats/stats.go (Snapshot, RecordRejection — new counters)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================