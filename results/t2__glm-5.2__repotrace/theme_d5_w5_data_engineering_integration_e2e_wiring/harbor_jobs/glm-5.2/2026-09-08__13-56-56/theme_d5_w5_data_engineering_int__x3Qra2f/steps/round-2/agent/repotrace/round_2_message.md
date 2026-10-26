========================================================================
[RepoTrace] Repository guidance for the current request (round 2)
The notes below summarize structural centrality and cross-round state.
They are supplemental context — use your own judgment to implement.
========================================================================

## Structural centrality
  - internal/config/config.go is depended on by 5 files (e.g. internal/stage/stage.go, internal/pipeline/pipeline.go, internal/input/input.go, internal/output/output.go); changing it ripples widely.
  - internal/record/record.go is depended on by 3 files (e.g. internal/stage/stage.go, internal/input/input.go, internal/output/output.go); changing it ripples widely.
  - internal/stage/stage.go is depended on by 2 files (e.g. internal/config/config.go, internal/pipeline/pipeline.go); changing it ripples widely.

## Cross-round state
Already present (from prior rounds):
  - internal/config/config.go: implementation
  - internal/record/record.go: implementation
  - internal/stage/stage.go: implementation
  - internal/input/input.go: implementation
  - internal/output/output.go: implementation
  - internal/pipeline/pipeline.go: pipeline logic
  - cmd/flowctl/main.go: CLI entry point
Prior components this round may touch:
  - Read input dispatch and CSV/NDJSON readers must remain unchanged while adding sqlite support
  - Build/Apply stage dispatch and existing filter/project/sort/limit stages must remain unchanged while adding group support
  - Run pipeline record numbering, stage execution order, and summary counting must remain stable when a group barrier is inserted
  - InputConfig/StageConfig config parsing and validation must accept new sqlite/group fields without altering existing configs

## Verification
  - Build and run tests after modification, e.g. `go build ./...`.

## Practical note
  The terminal can hang on very large heredocs. Write files in several smaller pieces.
========================================================================