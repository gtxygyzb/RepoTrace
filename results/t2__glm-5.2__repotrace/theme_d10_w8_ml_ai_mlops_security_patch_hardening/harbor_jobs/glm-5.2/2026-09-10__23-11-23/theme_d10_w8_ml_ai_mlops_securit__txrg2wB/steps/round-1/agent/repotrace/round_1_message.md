========================================================================
[RepoTrace] Repository guidance for the current request (round 1)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  (no file is depended on by multiple others)

## Cross-round state
Already present (from prior rounds):
New in this round (to be created):
  - main.go
  - go.mod
  - internal/config/config.go
  - internal/store/store.go
  - internal/auth/auth.go
  - internal/registry/registry.go
  - internal/inference/inference.go
  - internal/metrics/metrics.go
  - internal/audit/audit.go
  - internal/webhooks/webhooks.go
  - internal/server/router.go
  - internal/server/handlers.go

## Verification
  - Build and run tests after modification.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================