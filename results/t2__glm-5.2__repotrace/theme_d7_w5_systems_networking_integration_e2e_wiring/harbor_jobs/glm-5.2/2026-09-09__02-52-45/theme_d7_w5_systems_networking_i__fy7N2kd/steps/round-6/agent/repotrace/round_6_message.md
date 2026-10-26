========================================================================
[RepoTrace] Repository guidance for the current request (round 6)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/circuit/breaker.go is depended on by 8 files (e.g. internal/health/monitor.go, internal/state/state.go, internal/state/routing.go, internal/ipc/server.go); changing it ripples widely.
  - internal/accesslog/logger.go is depended on by 6 files (e.g. internal/health/monitor.go, internal/state/state.go, internal/state/ratelimit.go, internal/ipc/server.go); changing it ripples widely.
  - internal/state/state.go is depended on by 6 files (e.g. internal/health/monitor.go, internal/state/routing.go, internal/ipc/server.go, internal/router/router.go); changing it ripples widely.
  - internal/health/monitor.go is depended on by 5 files (e.g. internal/accesslog/logger.go, internal/state/ratelimit.go, internal/ipc/server.go, internal/router/router.go); changing it ripples widely.
  - internal/state/ratelimit.go is depended on by 5 files (e.g. internal/health/monitor.go, internal/state/state.go, internal/ipc/server.go, internal/router/router.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/circuit/breaker.go: implementation
  - internal/accesslog/logger.go: implementation
  - internal/state/state.go: state management
  - internal/health/monitor.go: implementation
  - internal/state/ratelimit.go: implementation
  - internal/state/routing.go: implementation
  - internal/stats/stats.go: implementation
  - internal/config/config.go: implementation
Prior components this round may touch:
  - Round 2 rate-limit queueing and stats (AcquireRateLimitToken, RecordQueueTimeout, RecordRateLimited)
  - Round 5 access log entry structure and query response (Log, ReadEntries, forward, copyConn)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================