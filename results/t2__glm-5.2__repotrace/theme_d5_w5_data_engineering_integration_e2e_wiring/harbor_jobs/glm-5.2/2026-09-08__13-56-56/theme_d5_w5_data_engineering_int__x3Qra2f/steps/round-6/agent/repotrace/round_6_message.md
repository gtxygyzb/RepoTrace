========================================================================
[RepoTrace] Repository guidance for the current request (round 6)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/config/config.go is depended on by 9 files (e.g. internal/stage/group.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/join.go); changing it ripples widely.
  - internal/record/record.go is depended on by 7 files (e.g. internal/stage/group.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/join.go); changing it ripples widely.
  - internal/stage/group.go is depended on by 6 files (e.g. internal/config/config.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/join.go); changing it ripples widely.
  - internal/stage/stage.go is depended on by 5 files (e.g. internal/stage/group.go, internal/config/config.go, internal/stage/join.go, internal/stage/dedup.go); changing it ripples widely.
  - internal/input/sqlite.go is depended on by 4 files (e.g. internal/stage/group.go, internal/stage/join.go, internal/input/input.go, internal/pipeline/pipeline.go); changing it ripples widely.

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
  - internal/stage/pivot.go
Prior components this round may touch:
  - group stage (round 2): missing `by` columns handling relaxed from hard error to empty-string grouping
  - group stage (round 2): numeric aggregate contribution rule for records missing the aggregate column

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================