========================================================================
[RepoTrace] Repository guidance for the current request (round 3)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/circuit/breaker.go is depended on by 6 files (e.g. internal/state/state.go, internal/ipc/server.go, internal/router/router.go, internal/state/routing.go); changing it ripples widely.
  - internal/state/state.go is depended on by 6 files (e.g. internal/ipc/server.go, internal/router/router.go, internal/state/routing.go, internal/health/monitor.go); changing it ripples widely.
  - internal/state/ratelimit.go is depended on by 5 files (e.g. internal/state/state.go, internal/ipc/server.go, internal/router/router.go, internal/health/monitor.go); changing it ripples widely.
  - internal/state/routing.go is depended on by 5 files (e.g. internal/ipc/server.go, internal/router/router.go, internal/health/monitor.go, internal/state/json.go); changing it ripples widely.
  - internal/config/config.go is depended on by 4 files (e.g. internal/state/state.go, internal/ipc/server.go, internal/health/monitor.go, cmd/meshd/main.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/circuit/breaker.go: implementation
  - internal/state/state.go: state management
  - internal/state/ratelimit.go: implementation
  - internal/state/routing.go: implementation
  - internal/config/config.go: implementation
  - internal/ipc/server.go: implementation
  - internal/router/router.go: implementation
  - internal/state/json.go: implementation

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================