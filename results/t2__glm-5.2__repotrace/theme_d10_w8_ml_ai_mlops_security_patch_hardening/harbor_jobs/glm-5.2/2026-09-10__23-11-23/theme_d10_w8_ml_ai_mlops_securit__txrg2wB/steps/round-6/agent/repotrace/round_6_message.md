========================================================================
[RepoTrace] Repository guidance for the current request (round 6)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/store/store.go is depended on by 8 files (e.g. internal/registry/registry.go, internal/metrics/metrics.go, internal/inference/inference.go, internal/audit/audit.go); changing it ripples widely.
  - internal/registry/registry.go is depended on by 6 files (e.g. internal/store/store.go, internal/inference/inference.go, internal/server/handlers.go, internal/auth/auth.go); changing it ripples widely.
  - internal/audit/audit.go is depended on by 5 files (e.g. internal/store/store.go, internal/server/handlers.go, internal/auth/auth.go, internal/webhooks/webhooks.go); changing it ripples widely.
  - internal/inference/inference.go is depended on by 5 files (e.g. internal/store/store.go, internal/server/handlers.go, internal/auth/auth.go, internal/webhooks/webhooks.go); changing it ripples widely.
  - internal/metrics/metrics.go is depended on by 5 files (e.g. internal/store/store.go, internal/server/handlers.go, internal/auth/auth.go, internal/webhooks/webhooks.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/store/store.go: implementation
  - internal/registry/registry.go: implementation
  - internal/audit/audit.go: implementation
  - internal/inference/inference.go: implementation
  - internal/metrics/metrics.go: implementation
  - internal/auth/auth.go: implementation
  - internal/registry/validate.go: validation
  - internal/server/handlers.go: implementation
New in this round (to be created):
  - internal/server/ratelimit.go
Prior components this round may touch:
  - Login
  - RegisterUser
  - Routes
  - clientIP

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================