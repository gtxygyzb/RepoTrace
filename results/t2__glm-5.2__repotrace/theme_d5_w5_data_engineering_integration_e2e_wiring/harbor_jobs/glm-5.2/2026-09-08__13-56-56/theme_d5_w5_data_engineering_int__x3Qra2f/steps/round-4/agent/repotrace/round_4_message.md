========================================================================
[RepoTrace] Repository guidance for the current request (round 4)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/config/config.go is depended on by 8 files (e.g. internal/stage/group.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/join.go); changing it ripples widely.
  - internal/record/record.go is depended on by 6 files (e.g. internal/stage/group.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/join.go); changing it ripples widely.
  - internal/stage/group.go is depended on by 5 files (e.g. internal/config/config.go, internal/stage/stage.go, internal/input/sqlite.go, internal/stage/join.go); changing it ripples widely.
  - internal/input/sqlite.go is depended on by 4 files (e.g. internal/stage/group.go, internal/stage/join.go, internal/input/input.go, internal/pipeline/pipeline.go); changing it ripples widely.
  - internal/stage/stage.go is depended on by 4 files (e.g. internal/config/config.go, internal/stage/group.go, internal/stage/join.go, internal/pipeline/pipeline.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/config/config.go: implementation
  - internal/record/record.go: implementation
  - internal/stage/group.go: implementation
  - internal/input/sqlite.go: implementation
  - internal/stage/stage.go: implementation
  - internal/input/input.go: implementation
  - internal/stage/join.go: implementation
  - internal/output/output.go: implementation
New in this round (to be created):
  - internal/stage/dedup.go
Prior components this round may touch:
  - sort stage in internal/stage/stage.go, especially buildSort/compareFloats missing numeric key handling
  - stage Build dispatch and StageConfig parsing for stage types

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================