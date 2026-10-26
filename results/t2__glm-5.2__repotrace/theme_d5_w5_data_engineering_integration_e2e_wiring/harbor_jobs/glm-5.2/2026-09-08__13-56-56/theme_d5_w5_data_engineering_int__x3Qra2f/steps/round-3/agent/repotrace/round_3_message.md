========================================================================
[RepoTrace] Repository guidance for the current request (round 3)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/config/config.go is depended on by 7 files (e.g. internal/stage/group.go, internal/stage/stage.go, internal/input/sqlite.go, internal/pipeline/pipeline.go); changing it ripples widely.
  - internal/record/record.go is depended on by 5 files (e.g. internal/stage/group.go, internal/stage/stage.go, internal/input/sqlite.go, internal/input/input.go); changing it ripples widely.
  - internal/stage/group.go is depended on by 4 files (e.g. internal/config/config.go, internal/stage/stage.go, internal/input/sqlite.go, internal/pipeline/pipeline.go); changing it ripples widely.
  - internal/input/sqlite.go is depended on by 3 files (e.g. internal/stage/group.go, internal/pipeline/pipeline.go, internal/input/input.go); changing it ripples widely.
  - internal/stage/stage.go is depended on by 3 files (e.g. internal/config/config.go, internal/stage/group.go, internal/pipeline/pipeline.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/config/config.go: implementation
  - internal/record/record.go: implementation
  - internal/stage/group.go: implementation
  - internal/input/sqlite.go: implementation
  - internal/stage/stage.go: implementation
  - internal/input/input.go: implementation
  - internal/output/output.go: implementation
  - internal/pipeline/pipeline.go: pipeline logic
New in this round (to be created):
  - internal/stage/join.go
Prior components this round may touch:
  - internal/stage/stage.go (Build/Apply stage dispatch needs new 'join' case)
  - internal/input/input.go (Read reused to load right.input)
  - internal/config/config.go (StageConfig/parsing must recognize join block)
  - internal/pipeline/pipeline.go (per-input row numbering must survive join row expansion)
  - internal/record/record.go (Set/Copy used to splice right fields onto left record)

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================