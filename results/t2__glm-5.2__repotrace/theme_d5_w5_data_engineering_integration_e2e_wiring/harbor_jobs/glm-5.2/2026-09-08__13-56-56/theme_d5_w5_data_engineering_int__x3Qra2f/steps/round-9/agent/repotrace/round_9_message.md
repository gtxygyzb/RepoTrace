========================================================================
[RepoTrace] Repository guidance for the current request (round 9)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/config/config.go is depended on by 12 files (e.g. internal/stage/group.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/unpivot.go); changing it ripples widely.
  - internal/record/record.go is depended on by 10 files (e.g. internal/stage/group.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/unpivot.go); changing it ripples widely.
  - internal/stage/group.go is depended on by 9 files (e.g. internal/config/config.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/unpivot.go); changing it ripples widely.
  - internal/stage/stage.go is depended on by 8 files (e.g. internal/stage/group.go, internal/config/config.go, internal/stage/unpivot.go, internal/stage/bucket.go); changing it ripples widely.
  - internal/input/sqlite.go is depended on by 7 files (e.g. internal/stage/group.go, internal/stage/unpivot.go, internal/stage/bucket.go, internal/stage/join.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/config/config.go: implementation
  - internal/record/record.go: implementation
  - internal/stage/group.go: implementation
  - internal/stage/stage.go: implementation
  - internal/input/sqlite.go: implementation
  - internal/input/input.go: implementation
  - internal/stage/bucket.go: implementation
  - internal/stage/dedup.go: implementation
New in this round (to be created):
  - internal/stage/rank.go
  - internal/stage/window.go
Prior components this round may touch:
  - rank stage (round 5) — percent formula change is retroactive for any pipeline using method:percent

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================