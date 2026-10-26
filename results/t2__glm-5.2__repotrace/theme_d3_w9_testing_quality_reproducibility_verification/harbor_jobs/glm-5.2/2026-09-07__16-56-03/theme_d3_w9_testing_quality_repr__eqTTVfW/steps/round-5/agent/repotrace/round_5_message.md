========================================================================
[RepoTrace] Repository guidance for the current request (round 5)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - cmd/repro-verify/util.go is depended on by 5 files (e.g. cmd/repro-verify/graph.go, cmd/repro-verify/fingerprint.go, cmd/repro-verify/trend.go, cmd/repro-verify/verify.go); changing it ripples widely.
  - cmd/repro-verify/graph.go is depended on by 3 files (e.g. cmd/repro-verify/manifest.go, cmd/repro-verify/verify.go, cmd/repro-verify/main.go); changing it ripples widely.
  - cmd/repro-verify/fingerprint.go is depended on by 2 files (e.g. cmd/repro-verify/verify.go, cmd/repro-verify/main.go); changing it ripples widely.
  - cmd/repro-verify/manifest.go is depended on by 2 files (e.g. cmd/repro-verify/graph.go, cmd/repro-verify/verify.go); changing it ripples widely.
  - cmd/repro-verify/policy.go is depended on by 2 files (e.g. cmd/repro-verify/manifest.go, cmd/repro-verify/verify.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - cmd/repro-verify/util.go: implementation
  - cmd/repro-verify/graph.go: implementation
  - cmd/repro-verify/fingerprint.go: implementation
  - cmd/repro-verify/manifest.go: implementation
  - cmd/repro-verify/policy.go: implementation
  - cmd/repro-verify/diff.go: implementation
  - cmd/repro-verify/summary.go: implementation
  - cmd/repro-verify/trend.go: implementation
New in this round (to be created):
  - cmd/repro-verify/slice.go
  - docs/spec_v5.md
Prior components this round may touch:
  - trend subcommand (round 4) — statusRank change alters classification of FAIL/TIMEOUT/ERROR transitions
  - diff subcommand (round 2) — must be verified NOT to share trend's statusRank so its behavior stays unchanged
  - main.go subcommand registration (rounds 1-4) — must register new slice subcommand

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================