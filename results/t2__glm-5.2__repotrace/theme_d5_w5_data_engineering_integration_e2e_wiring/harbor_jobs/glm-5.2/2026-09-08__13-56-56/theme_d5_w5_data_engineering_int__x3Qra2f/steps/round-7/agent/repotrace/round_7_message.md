========================================================================
[RepoTrace] Repository guidance for the current request (round 7)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/config/config.go is depended on by 10 files (e.g. internal/stage/group.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/join.go); changing it ripples widely.
  - internal/record/record.go is depended on by 8 files (e.g. internal/stage/group.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/join.go); changing it ripples widely.
  - internal/stage/group.go is depended on by 7 files (e.g. internal/config/config.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/join.go); changing it ripples widely.
  - internal/stage/stage.go is depended on by 6 files (e.g. internal/stage/group.go, internal/config/config.go, internal/stage/join.go, internal/stage/pivot.go); changing it ripples widely.
  - internal/input/sqlite.go is depended on by 5 files (e.g. internal/stage/group.go, internal/stage/join.go, internal/stage/pivot.go, internal/input/input.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/config/config.go: implementation
  - internal/record/record.go: implementation
  - internal/stage/group.go: implementation
  - internal/stage/stage.go: implementation
  - internal/input/sqlite.go: implementation
  - internal/input/input.go: implementation
  - internal/stage/dedup.go: implementation
  - internal/stage/join.go: implementation
New in this round (to be created):
  - internal/stage/unpivot.go
Prior components this round may touch:
  - Build in internal/stage/stage.go (must dispatch new unpivot type)
  - StageConfig in internal/config/config.go (must carry unpivot configuration)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================